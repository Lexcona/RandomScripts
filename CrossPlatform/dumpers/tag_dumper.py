import os
import json
import argparse
import requests

from bs4 import BeautifulSoup
from rich.console import Console

parser = argparse.ArgumentParser()

parser.add_argument("url")
parser.add_argument("-o", "--output")

args = parser.parse_args()

url = args.url
if args.output:
    output = args.output
else:
    output = url.split("://")[-1].replace("/", "+")
tags = {}

res = requests.get(url)

for tag in BeautifulSoup(res.content, "html.parser").find_all():
    print("Getting "+tag.name)
    print(str(tag))
    funny = output+"/"+tag.name

    os.makedirs(funny, exist_ok=True)
    if not tags.get(tag.name):
        tags[tag.name] = []

    with open(funny+"/"+str(len(tags[tag.name]))+".html", "w+") as f:
        f.write(str(tag))
    
    tags[tag.name].append(str(tag))
    
with open(output+"/original.html", "w+") as f:
    f.write(res.text)

with open(output+"/tags.json", "w+") as f:
    json.dump(tags, f, indent=4)