import re
import os
import json
import shutil
import argparse
import datetime

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
        #print(f"\n\n\n\n\n\n\n\nERROR: {e}\n{cool[-1]}\n\n\n\n\n\n\n\n")
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
        #print(f"Found script: {scripterown}")
        try:
            json.loads(scripterown)
            #print(f"Script Passed JSON test: {scripterown}")
        except Exception:
            #print(f"Parsing: {scripterown}")
            scripterown = undothedoer(scripterown)
            if scripterown:
                with open(f"{output}/debug/parsed_scripts/{scriptInterval}.js", "w+") as f:
                    f.write(scripterown)
                #print(f"Parsed: {scripterown}")
                try:
                    json.loads(scripterown)
                    #print(f"Script Passed JSON test: {scripterown}")
                except Exception:
                    #print(f"Script Failed JSON test: {scripterown}")
                    didFailParse = True
            else:
                didFailParse = True
        if didFailParse == False:
            with open(f"{output}/debug/json_objects/{scriptInterval}.json", "w+") as f:
                jsoners.append(json.loads(scripterown))
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

with open(f"{output}/Account Info.txt", "w+") as f:
    text = f"""================
  Account Info
================
Display Name: {funny_data['page_data']['config']['display_name']}
Username: {funny_data['page_data']['username']}
Alias: {funny_data['page_data']['alias']}
Description: {funny_data['page_data']['config']['description']}
Location: {funny_data['page_data']['config']['location']}
ID: {funny_data['page_data']['_id']}
UID: {funny_data['page_data']['uid']}
Date Created: {datetime.datetime.fromtimestamp(funny_data['page_data']['account_created']).strftime("%m/%d/%Y, %H:%M:%S")}
Verified: {funny_data['page_data']['verified']}
Premium: {funny_data['page_data']['premium']}

=============
    Stats
=============
Page Views: {funny_data['page_data']['config']['page_views']}

===============
    Images
===============
Avatar: {funny_data['page_data']['config']['avatar']}
Banner: {funny_data['page_data']['config']['url']}
Custom Cursor: {funny_data['page_data']['config']['custom_cursor']}

===============
    Colors
===============
Base Color: {funny_data['page_data']['config']['color']}
Text Color: {funny_data['page_data']['config']['text_color']}
Background Color: {funny_data['page_data']['config']['bg_color']}
Icon Color: {funny_data['page_data']['config']['icon_color']}
Gradient 1: {funny_data['page_data']['config']['gradient_1']}
Gradient 2: {funny_data['page_data']['config']['gradient_2']}
Gradient 2: {funny_data['page_data']['config']['gradient_2']}
Swap Colors: {funny_data['page_data']['config']['swap_colors']}

===============
    Effects
===============
Background Effect: {funny_data['page_data']['config']['background_effects']}
Username Effect: {funny_data['page_data']['config']['username_effects']}
Social Glow: {funny_data['page_data']['config']['social_glow']}
Badge Glow: {funny_data['page_data']['config']['badge_glow']}
Username Glow: {funny_data['page_data']['config']['username_glow']}
Blur: {funny_data['page_data']['config']['blur']}
Opacity: {funny_data['page_data']['config']['opacity']}
Opacity: {funny_data['page_data']['config']['opacity']}

===============
    Options
===============
Profile Gradient: {funny_data['page_data']['config']['profile_gradient']}
Presence: {funny_data['page_data']['config']['presence']}
Animated Title: {funny_data['page_data']['config']['animated_title']}
Monochrome: {funny_data['page_data']['config']['monochrome']}
Volume Control: {funny_data['page_data']['config']['volume_control']}
Use Discord Account: {funny_data['page_data']['config']['use_discord_avatar']}
Discord Avatar Decoration: {funny_data['page_data']['config']['discord_avatar_decoration']}

"""

    if funny_data['page_data']['config']['user_badges'] != []:
        text += """==============
    Badges
==============
"""
        for badge in funny_data['page_data']['config']['user_badges']:
            if isinstance(badge, dict):
                text += f"""Name: {badge['name']}
Enabled: {badge['enabled']}

"""
            else:
                text += badge + "\n"

    if funny_data['page_data']['config']['custom_badges'] != []:
        text += """=====================
Custom Badges
====================="""

        for badge in funny_data['page_data']['config']['custom_badges']:
            if isinstance(badge, dict):
                text += f"""Name: {badge['name']}
Icon: {badge['icon']}
ID: {badge['id']}
Enabled: {badge['enabled']}

"""
            else:
                text += badge + "\n"
    
    if funny_data['page_data']['config']['socials'] != []:
        text += """===============
    Socials
===============
"""
        for social in funny_data['page_data']['config']['socials']:
            if isinstance(social, dict):
                text += f"""Name: {social['social'].capitalize()}
URL: {social['value']}
ID: {social['id']}
"""
                if social.get("mode"):
                    text += f"Mode: {social['mode']}\n"
                text += "\n"
            else:
                text += badge + "\n"
    if isinstance(funny_data['page_data']['config']['audio'], list):
        text += """==============
    Audios
==============
"""
        for audio in funny_data['page_data']['config']['audio']:
            text += f"""Name: {audio['title']}
URL: {audio['url']}
Duration: {audio['duration']}
Selected: {audio['selected']}
ID: {audio['id']}

"""
    if funny_data['page_data']['premium'] == True:
        text += f"""===============
    Premium
===============

======================
    Premium Colors
======================
Effects Color: {funny_data['page_data']['config']['premium']['effects_color']}
Badge Color: {funny_data['page_data']['config']['premium']['badge_color']}
Border Color: {funny_data['page_data']['config']['premium']['border_color']}

=======================
    Premium Effects
=======================
Cursor Effects: {funny_data['page_data']['config']['premium']['cursor_effects']}
Badge Color: {funny_data['page_data']['config']['premium']['badge_color']}
Border Color: {funny_data['page_data']['config']['premium']['border_color']}
Animation: {funny_data['page_data']['config']['premium']['animation']}

=======================
    Premium Boarder
=======================
Border Enabled: {funny_data['page_data']['config']['premium']['border_enabled']}
Border Width: {funny_data['page_data']['config']['premium']['border_width']}
Border Radius: {funny_data['page_data']['config']['premium']['border_radius']}

======================
    Premium Button
======================
Button Shadow: {funny_data['page_data']['config']['premium']['button_shadow']}
Button Border Radius: {funny_data['page_data']['config']['premium']['button_border_radius']}
Buttons:
"""
        if funny_data['page_data']['config']['premium']['buttons'] != []:
            for button in funny_data['page_data']['config']['premium']['buttons']:
                text += button + "\n"
        text += f"""
==========================
    Premium Typewriter
==========================
Typewriter Enabled: {funny_data['page_data']['config']['premium']['typewriter_enabled']}
Typewriter Text:
"""
        for thing in funny_data['page_data']['config']['premium']['typewriter']:
            text += f"{thing}\n"

        text += f"""
    
=======================
    Premium Options
=======================
Font: {funny_data['page_data']['config']['premium']['font']}
Typewriter Enabled: {funny_data['page_data']['config']['premium']['typewriter_enabled']}
Typewriter: 
Hide Views: {funny_data['page_data']['config']['premium']['hide_views']}
Hide Join Date: {funny_data['page_data']['config']['premium']['hide_join_date']}
Second Tab Enabled: {funny_data['page_data']['config']['premium']['second_tab_enabled']}
Second Tab (Too lazy to format): {funny_data['page_data']['config']['premium']['second_tab']}
Parallax Animation: {funny_data['page_data']['config']['premium']['parallax_animation']}
Monochrome Animation: {funny_data['page_data']['config']['premium']['monochrome_badges']}
Page Enter Text: {funny_data['page_data']['config']['premium']['page_enter_text']}
Layout: {funny_data['page_data']['config']['premium']['layout']}
Banner: {funny_data['page_data']['config']['premium']['banner']}
Show URL: {funny_data['page_data']['config']['premium']['show_url']}
Text Align: {funny_data['page_data']['config']['premium']['text_align']}

========================
    Metadata Options
========================
Title: {funny_data['page_data']['config']['premium']['metadata']['title']}
Description: {funny_data['page_data']['config']['premium']['metadata']['description']}
Image: {funny_data['page_data']['config']['premium']['metadata']['image']}
Favicon: {funny_data['page_data']['config']['premium']['metadata']['favicon']}
Information Overlay: {funny_data['page_data']['config']['premium']['metadata']['information_overlay']}
"""
    f.write(text)

os.makedirs(output+"/media/", exist_ok=True)
os.makedirs(output+"/media/audios", exist_ok=True)
with open(output+"/media/avatar."+funny_data['page_data']['config']['avatar'].split(".")[-1], "wb") as f:
    f.write(requests.get(funny_data['page_data']['config']['avatar']).content)
with open(output+"/media/banner."+funny_data['page_data']['config']['url'].split(".")[-1], "wb") as f:
    f.write(requests.get(funny_data['page_data']['config']['url']).content)
if funny_data['page_data']['config']['custom_cursor'] != "":
    with open(output+"/media/cursor."+funny_data['page_data']['config']['custom_cursor'].split(".")[-1], "wb") as f:
        f.write(requests.get(funny_data['page_data']['config']['custom_cursor']).content)

for audio in funny_data['page_data']['config']['audio']:
    with open(output+"/media/audios/"+audio['title'], "wb") as f:
        f.write(requests.get(audio['url']).content)
print("Dumped done")