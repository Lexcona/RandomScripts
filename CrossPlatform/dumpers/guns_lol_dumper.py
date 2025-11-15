import re
import os
import json
import shutil
import argparse

import cloudscraper
import requests

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()

parser.add_argument("username")
parser.add_argument("-o", "--output")

args = parser.parse_args()

if args.username.startswith("https://") or args.username.startswith("http://") or "guns.lol" in args.username:
    funny = args.username.split("/")

    for i in funny[::]:
        if i.replace(" ", "") == "":
            funny.remove(i)
    
    username = funny[-1]
else:
    username = args.username

if args.output:
    output = args.output
else:
    output = f"output/guns.lol/{username}"

scraper = cloudscraper.create_scraper()

mpres = scraper.get(f"https://guns.lol/{username}")

mpsoup = BeautifulSoup(mpres.content, "html.parser")

if os.path.exists(output):
    shutil.rmtree(output)

def undothedoer(mexico:str):
    funny = mexico.split(".push(")[-1].split(")")
    funny.pop(-1)
    funny = ')'.join(funny)
    try:
        cool = json.loads(funny)
    except Exception:
        return
    try:
        json.dumps(cool[-1])
        funny = cool[-1]
    except Exception as e:
        print(f"\n\n\n\n\n\n\n\nERROR: {e}\n{cool[-1]}\n\n\n\n\n\n\n\n")
        return

    try:
        int(funny)
        return
    except Exception:
        funny = str(funny)

        hhhhh = funny.split(":{")
        hhhhh.pop(0)
        funny = "{"+":{".join(hhhhh).replace("}}]", "}")

        if funny == "{":
            return

        return str(funny)

jsoners = []

scriptInterval = 0
for script in mpsoup.find_all("script"):
    didFailParse = False
    scripterown = str(script.text)
    if scripterown.replace(" ", "") != "":
        scriptInterval += 1
        os.makedirs(f"{output}/debug/json_objects", exist_ok=True)
        os.makedirs(f"{output}/debug/raw_scripts", exist_ok=True)
        os.makedirs(f"{output}/debug/parsed_scripts", exist_ok=True)
        
        with open(f"{output}/debug/raw_scripts/{scriptInterval}.js", "w+") as f:
            f.write(scripterown)
        print(f"Found script: {scripterown}")
        try:
            json.loads(scripterown)
            print(f"Script Passed JSON test: {scripterown}")
        except Exception:
            print(f"Parsing: {scripterown}")
            scripterown = undothedoer(scripterown)
            if scripterown:
                with open(f"{output}/debug/parsed_scripts/{scriptInterval}.js", "w+") as f:
                    f.write(scripterown)
                print(f"Parsed: {scripterown}")
                try:
                    json.loads(scripterown)
                    print(f"Script Passed JSON test: {scripterown}")
                except Exception:
                    print(f"Script Failed JSON test: {scripterown}")
                    didFailParse = True
            else:
                didFailParse = True
        if didFailParse == False:
            with open(f"{output}/debug/json_objects/{scriptInterval}.json", "w+") as f:
                jsoners.append(scripterown)
                json.dump(json.loads(scripterown), f, indent=4)

funny_data = {}

for funny in jsoners:
    if funny.get("@context"):
        funny_data["guns_metadata"] = funny
    elif funny.get("_id"):
        funny_data["page_data"] = funny
    elif funny.get("metadata"):
        funny_data["page_metadata"] = funny
    else:
        if not funny_data.get("unknown"):
            funny_data["unknown"] = []
        funny_data["unknown"].append(funny)