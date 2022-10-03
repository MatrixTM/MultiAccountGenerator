from contextlib import suppress
from random import choice
from string import ascii_letters
from threading import Thread
from dhooks.client import Webhook
import colorama
from httpx import get
from json import load

colorama.init()
config: dict = load(open('config.json'))


class Main(Thread):
    def __init__(self):
        self.randstr = lambda length: ''.join(choice(ascii_letters) for _ in range(length))
        super().__init__(daemon=True)

    def run(self):
        while True:
            string = self.randstr(10)
            request = get(f"http://bin.shortbin.eu:8080/raw/{string}", timeout=5)
            if request.status_code != 200:
                print(
                    f"{colorama.Fore.RED}[-] Bad | http://bin.shortbin.eu:8080/raw/{string} - {request.status_code} \n")
                continue

            print(
                f"{colorama.Fore.LIGHTGREEN_EX}[+] Hit | http://bin.shortbin.eu:8080/raw/{string} - {request.text} \n")

            if len(config['webhook']) > 100:
                with suppress(Exception):
                    Webhook(config['webhook']).send(f'{str(config["webhook_content"]).replace("<acc>", request.text)}')
            open(config["accountFilePath"], "a+").write(request.text + "\n")


if __name__ == '__main__':
    for _ in range(config['thread']):
        Main().start()
    while True:
        input()
