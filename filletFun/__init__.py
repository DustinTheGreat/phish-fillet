
#!/usr/bin/python3

import os
from sys import exit



try:
    import requests

except ModuleNotFoundError as e:
    print("\n[-] Error: {}".format(e))
    print("[-] You are missing a required dependency.")
    answer = input("\n[?] Do you wish to install the missing dependency? (y/n): ")
    answer = answer.lower().strip()
    if answer == "yes" or "y":
        print("[!] Using pip3 to install module")
        os.system("pip3 install requests")
    if answer == "no" or "n":
        print("[!] Please use pip3 to install module")

except KeyboardInterrupt:
        print("[!] Goodbye!")
        exit()

try:
    import argparse

except ModuleNotFoundError as e:
    print("\n[-] Error: {}".format(e))
    print("[-] You are missing a required dependency.")
    answer = input("\n[?] Do you wish to install the missing dependency? (y/n): ")
    answer = answer.lower().strip()
    if answer == "yes" or "y":
        print("[!] Using pip3 to install module")
        os.system("pip3 install argparse")
    if answer == "no" or "n":
        print("[!] Please use pip3 to install module")

except KeyboardInterrupt:
        print("[!] Goodbye!")
        exit()

try:
    from urllib.parse import urlparse

except ModuleNotFoundError as e:
    print("\n[-] Error: {}".format(e))
    print("[-] You are missing a required dependency.")
    answer = input("\n[?] Do you wish to install the missing dependency? (y/n): ")
    answer = answer.lower().strip()
    if answer == "yes" or "y":
        print("[!] Using pip3 to install module")
        os.system("pip3 install urllib")
    if answer == "no" or "n":
        print("[!] Please use pip3 to install module")

except KeyboardInterrupt:
        print("[!] Goodbye!")
        exit()

try:
    import re

except ModuleNotFoundError as e:
    print("\n[-] Error: {}".format(e))
    print("[-] You are missing a required dependency.")
    answer = input("\n[?] Do you wish to install the missing dependency? (y/n): ")
    answer = answer.lower().strip()
    if answer == "yes" or "y":
        print("[!] Using pip3 to install module")
        os.system("pip3 install re")
    if answer == "no" or "n":
        print("[!] Please use pip3 to install module")

except KeyboardInterrupt:
        print("[!] Goodbye!")
        exit()

try:
    from progress.bar import IncrementalBar

except ModuleNotFoundError as e:
    print("\n[-] Error: {}".format(e))
    print("[-] You are missing a required dependency.")
    answer = input("\n[?] Do you wish to install the missing dependency? (y/n): ")
    answer = answer.lower().strip()
    if answer == "yes" or "y":
        print("[!] Using pip3 to install module")
        os.system("pip3 install progress")
    if answer == "no" or "n":
        print("[!] Please use pip3 to install module")

except KeyboardInterrupt:
        print("[!] Goodbye!")
        exit()

try:
    from bs4 import BeautifulSoup

except ModuleNotFoundError as e:
    print("\n[-] Error: {}".format(e))
    print("[-] You are missing a required dependency.")
    answer = input("\n[?] Do you wish to install the missing dependency? (y/n): ")
    answer = answer.lower().strip()
    if answer == "yes" or "y":
        print("[!] Using pip3 to install module")
        os.system("pip3 install bs4")
    if answer == "no" or "n":
        print("[!] Please use pip3 to install module")

except KeyboardInterrupt:
        print("[!] Goodbye!")
        exit()

try:
    from ip2geotools.databases.noncommercial import DbIpCity

except ModuleNotFoundError as e:
    print("\n[-] Error: {}".format(e))
    print("[-] You are missing a required dependency.")
    answer = input("\n[?] Do you wish to install the missing dependency? (y/n): ")
    answer = answer.lower().strip()
    if answer == "yes" or "y":
        print("[!] Using pip3 to install module")
        os.system("pip3 install ip2geotools")
    if answer == "no" or "n":
        print("[!] Please use pip3 to install module")

except KeyboardInterrupt:
        print("[!] Goodbye!")
        exit()

