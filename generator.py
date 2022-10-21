import sys
from contextlib import suppress
from json import load
from random import choice
from re import findall
from threading import Thread

import colorama
from PyTerm import Console
from bs4 import BeautifulSoup
from httpx import post, Response

colorama.init()


class Generator:
    def __init__(self):
        self.config: dict = load(open('config.json'))

    @staticmethod
    def banner():
        Console.clear()
        print("""
          __  __       _   _ _  _____            
         |  \/  |     | | | (_)/ ____|           
         | \  / |_   _| |_| |_| |  __  ___ _ __  
         | |\/| | | | | __| | | | |_ |/ _ \ '_ \ 
         | |  | | |_| | |_| | | |__| |  __/ | | |
         |_|  |_|\__,_|\__|_|_|\_____|\___|_| |_|                                         
                        #MahsaAmini\n\n""")

    def run(self):
        self.banner()
        for i in range(len(self.config["services"])):
            print(f"{i} - {self.config['services'][i]}")
        print("69 - exit\n")
        tmpinp = int(input("Select service to scrape url >> "))
        inp = tmpinp
        sys.exit(1) if tmpinp == "69" else inp  # Exit if exit selected
        if inp <= len(self.config['services']):
            inp = self.config['services'][inp]  # Change number to Name
            self.banner()
        else:
            input("Select valid Item\nPress Enter to Exit")
            sys.exit(1)
        for _ in range(self.config["thread"]):
            self.Generate(self.config['url'][inp], self.config['selector'][inp] or inp, self.config).start()
        while True:
            try:
                input()
            except KeyboardInterrupt:
                sys.exit(1)

    class Generate(Thread):
        def __init__(self, url: str, selector: str, config: dict):
            self.request, self.url, self.selector, self.config, self.output, self.outUrl = Response, url, selector, config, open(
                config["output"], "a+"), str
            super().__init__(daemon=True)

        def run(self):
            while True:
                with suppress(Exception):
                    self.request = post(choice(self.url), data={"gen": ""}, timeout=self.config["request-timeout"] or 5)
                    self.outUrl = \
                        findall("http://.*", str(BeautifulSoup(self.request.text, "html.parser").select(self.selector)))[0]
                    self.output.write(self.outUrl)
                    print(f"{colorama.Fore.LIGHTGREEN_EX}[+] {self.outUrl}")


if __name__ == '__main__':
    Generator().run()
