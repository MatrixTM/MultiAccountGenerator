from random import choice
from string import ascii_letters
from threading import Thread
import os

try:
    from dhooks.client import Webhook
except:
    os.system("pip install dhooks")
try:
    import colorama
except:
    os.system("pip install colorama")
try:
    import requests
except:
    os.system("pip install requests")

colorama.init()
randString = lambda length: ''.join(choice(ascii_letters) for _ in range(length))
webhook = "Your Webhook" # If Your Dont Have Webhook Dont Change It
speed = 1 # Warning!

class Main(Thread):
    def __init__(self):
        super().__init__(daemon=True)

    def run(self) -> None:
        while True:
            st = randString(10)
            with requests.get(f"http://bin.shortbin.eu:8080/documents/{st}") as s:
                if s.status_code != 200:
                    print(f"{colorama.Fore.RED}[-]  {st}")
                    continue
                print(f"{colorama.Fore.LIGHTGREEN_EX}[+]  {s.url}")
                
                if webhook != "":
                    try:
                        surl = s.url
                        orgurl = surl.replace("documents/", "")
                        hook = Webhook(webhook)
                        hook.send(f"Original url: `{orgurl}`")
                    except:
                        pass
                else:
                    pass
                
                with open("Orginalurl.txt", "a+") as f:
                    f.write(orgurl + "\n")


for _ in range(speed):
    Main().start()
while True:
    input()
