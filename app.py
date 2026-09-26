import threading
import pyperclip  # type: ignore
import time
import os
import asyncio
from typing import List
import os

from src.intro import Intro
from src.console import Console
from src.exceptions import NoContinueException
from src.client import Client

links = []
running = True
last_text = ""

def monitor_clipboard():
    global running, last_text

    while running:
        try:
            current_text = pyperclip.paste()

            if not current_text.startswith("https://t.me/"): raise NoContinueException()
            if not current_text.strip(): raise NoContinueException()
            if current_text == last_text: raise NoContinueException()
            if current_text in links: raise NoContinueException()

            last_text = current_text
            links.append(current_text)

            if len(links) == 1:
                Console.clear()
                Intro.create()
                print("\n   >> LINKS CATCHED <<\n")

            print(f"{len(links)}) {current_text}")
        
        except NoContinueException: ...
        except Exception as e: print(e)

        time.sleep(0.5)


async def main():
    global running, links, last_text

    client = Client()
    await client.start()

    Console.clear()
    Intro.create()

    clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
    clipboard_thread.start()

    while running:
        command = input("").strip().lower()

        if command == "":
            if not len(links):
                print("Huh? you didn't copy any telegram media link yet...")
                continue

            print("Starting to download medias...")

            await client.download_media(links)
            links = []
            pyperclip.copy("")
            last_text = ""

        elif command == "r":
            links = []
            pyperclip.copy("")
            last_text = ""

            Console.clear()
            Intro.create()

        elif command == "exit":
            print("Exiting...")
            running = False

        else:
            print("I have no idea what command is that...")


if __name__ == "__main__":
    asyncio.run(main())
