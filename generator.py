import socket as dsocket
from asyncio import sleep, new_event_loop, run, gather, create_task, set_event_loop
from contextlib import suppress
from dataclasses import dataclass
from json import load
from os import path, getcwd, listdir, chdir, remove, system, mkdir
from os.path import exists
from random import choice, randrange
from re import findall
from shutil import copytree, rmtree, copyfile
from ssl import create_default_context
from sys import exit
from typing import IO
from urllib.parse import urlparse
from zipfile import ZipFile

from aioconsole import aprint, ainput
from aiofiles import open as openfile
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from colorama import Fore, init
from requests import get

init()


class AutoUpdater:
    def __init__(self, version):
        self.version = version
        self.latest = self.get_latest()
        self.this = getcwd()
        self.file = "temp/latest.zip"
        self.folder = f"temp/latest_{randrange(1_000_000, 999_999_999)}"

    @dataclass
    class latest_data:
        version: str
        zip_url: str

    def get_latest(self):
        rjson = get("https://api.github.com/repos/MatrixTM/MultiAccountGenerator/tags").json()
        return self.latest_data(version=rjson[0]["name"], zip_url=get(rjson[0]["zipball_url"]).url)

    @staticmethod
    def download(host, dPath, filename):
        with dsocket.socket(dsocket.AF_INET, dsocket.SOCK_STREAM) as sock:
            context = create_default_context()
            with context.wrap_socket(sock, server_hostname="api.github.com") as wrapped_socket:
                wrapped_socket.connect((dsocket.gethostbyname(host), 443))
                wrapped_socket.send(
                    f"GET {dPath} HTTP/1.1\r\nHost:{host}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,file/avif,file/webp,file/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n\r\n".encode())

                resp = b""
                while resp[-4:-1] != b"\r\n\r":
                    resp += wrapped_socket.recv(1)
                else:
                    resp = resp.decode()
                    content_length = int(
                        "".join([tag.split(" ")[1] for tag in resp.split("\r\n") if "content-length" in tag.lower()]))
                    _file = b""
                    while content_length > 0:
                        data = wrapped_socket.recv(2048)
                        if not data:
                            print("EOF")
                            break
                        _file += data
                        content_length -= len(data)
                    with open(filename, "wb") as file:
                        file.write(_file)

    def update(self):
        if not self.version == self.latest.version:
            rmtree("temp") if exists("temp") else ""
            mkdir("temp")
            print("Updating Script...")
            parsed = urlparse(self.latest.zip_url)
            self.download(parsed.hostname, parsed.path, self.file)
            ZipFile(self.file).extractall(self.folder)
            print(exists(self.folder))
            print(exists(listdir(self.folder)[0]))
            chdir("{}/{}".format(self.folder, listdir(self.folder)[0]))
            for files in listdir():
                if path.isdir(files):
                    with suppress(FileNotFoundError):
                        rmtree("{}/{}".format(self.this, files))
                    copytree(files, "{}/{}".format(self.this, files))
                else:
                    with suppress(FileNotFoundError):
                        remove("{}/{}".format(self.this, files))
                    copyfile(files, "{}/{}".format(self.this, files))
            rmtree("../../../temp")
            exit("Run Script Again!")
            return
        print("Script is up to date!")


class Generator:
    def __init__(self):
        self.version = "v1.1"
        AutoUpdater(self.version).update()
        self.config: dict = load(open('config.json'))
        self.output: IO = open(self.config["output"], "a+")
        self.tasks: list = []
        self.colors: list = [
            Fore.LIGHTGREEN_EX,
            Fore.LIGHTBLACK_EX,
            Fore.LIGHTMAGENTA_EX,
            Fore.LIGHTBLUE_EX,
            Fore.LIGHTCYAN_EX,
            Fore.LIGHTRED_EX,
            Fore.LIGHTYELLOW_EX,
            Fore.CYAN
        ]

    async def make_beautiful(self, text: str, reset=True) -> str:
        tmp = ["%s%s" % (choice(self.colors), char) for char in text]

        return "".join(tmp) if not reset else "".join(tmp) + Fore.RESET

    async def banner(self) -> None:
        system('cls||clear')
        print(await self.make_beautiful("""
          __  __       _   _ _  _____            
         |  \/  |     | | | (_)/ ____|           
         | \  / |_   _| |_| |_| |  __  ___ _ __  
         | |\/| | | | | __| | | | |_ |/ _ \ '_ \ 
         | |  | | |_| | |_| | | |__| |  __/ | | |
         |_|  |_|\__,_|\__|_|_|\_____|\___|_| |_|                                         
                        #MATRIX\n\n""", False))

    async def run(self) -> None:
        await self.banner()
        for i in range(len(self.config["services"])):
            await aprint(f"{i} - {self.config['services'][i]}")
        await aprint("69 - exit\n")
        inp = await ainput("Select service to scrape url >> ")
        exit(1) if inp == "69" else inp  # Exit if exit selected
        if int(inp) <= len(self.config['services']):
            inp = self.config['services'][int(inp)]  # Change number to Name
            await self.banner()
        else:
            await ainput("Select valid Item\nPress Enter to Exit")
            exit(1)
        await aprint("Creating tasks")
        for i in range(self.config["thread"]):
            self.tasks.append(
                create_task(self.generate(i, self.config['url'][inp], self.config['selector'][inp] or inp)))
            await aprint("%s Task Created!" % i, end="\r")
            await sleep(.1)
        print()

        await gather(*self.tasks)

    async def generate(self, worker, url: str, selector: str) -> None:
        while True:
            with suppress(Exception):
                async with openfile(self.config["output"], "a+") as file:
                    async with ClientSession() as session:
                        request = await session.post(choice(url), data={"gen": ""},
                                                     timeout=self.config["request-timeout"] or 5)
                        outUrl = \
                            findall("http://.*",
                                    str(BeautifulSoup(await request.text(), "html.parser").select(selector)))[
                                0]
                        await aprint("%s[%s] " % (Fore.LIGHTCYAN_EX, worker) + await self.make_beautiful(outUrl))
                        await file.write("%s" % outUrl)


if __name__ == '__main__':
    loop = new_event_loop()
    set_event_loop(loop)
    try:
        run(Generator().run())
    except KeyboardInterrupt:
        pass
