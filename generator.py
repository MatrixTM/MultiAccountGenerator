import asyncio
import sys
from contextlib import suppress
from json import load
from random import choice
from re import findall
import os

import aiohttp
import colorama
from colorama import Fore
from aioconsole import aprint, ainput
from bs4 import BeautifulSoup

colorama.init()


class Generator:
    def __init__(self):
        self.config: dict = load(open('config.json'))
        self.output = open(self.config["output"], "a+")
        self.tasks = []
        self.useless_value = 0
        self.colors = [
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

    async def banner(self):
        os.system('cls||clear')
        print(await self.make_beautiful("""
          __  __       _   _ _  _____            
         |  \/  |     | | | (_)/ ____|           
         | \  / |_   _| |_| |_| |  __  ___ _ __  
         | |\/| | | | | __| | | | |_ |/ _ \ '_ \ 
         | |  | | |_| | |_| | | |__| |  __/ | | |
         |_|  |_|\__,_|\__|_|_|\_____|\___|_| |_|                                         
                        #MahsaAmini\n\n""", False))

    async def run(self):
        await self.banner()
        for i in range(len(self.config["services"])):
            await aprint(f"{i} - {self.config['services'][i]}")
        await aprint("69 - exit\n")
        inp = await ainput("Select service to scrape url >> ")
        sys.exit(1) if inp == "69" else inp  # Exit if exit selected
        if int(inp) <= len(self.config['services']):
            inp = self.config['services'][int(inp)]  # Change number to Name
            await self.banner()
        else:
            await ainput("Select valid Item\nPress Enter to Exit")
            sys.exit(1)
        await aprint("Creating tasks")
        for _ in range(self.config["thread"]):
            self.tasks.append(
                asyncio.create_task(self.generate(self.config['url'][inp], self.config['selector'][inp] or inp)))
            self.useless_value += 1
            await aprint("%s Task Created!" % self.useless_value, end="\r")
            await asyncio.sleep(.1)

        await asyncio.gather(*self.tasks)

    async def generate(self, url: str, selector: str) -> None:
        while True:
            with suppress(Exception):
                session = aiohttp.ClientSession()
                request = await session.post(choice(url), data={"gen": ""}, timeout=self.config["request-timeout"] or 5)
                await session.close()
                outUrl = \
                    findall("http://.*", str(BeautifulSoup(await request.text(), "html.parser").select(selector)))[0]
                await aprint(await self.make_beautiful(outUrl))
                self.output.write("%s\n" % outUrl)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(Generator().run())
    except KeyboardInterrupt:
        pass
