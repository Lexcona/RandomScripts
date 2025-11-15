import os
import json
import time
import datetime
import calendar
import argparse
import threading

import requests

max_threads = 250
threads = []

outputdir = "output/nyts/"

funny_urls = [
    {
        "name": "wordle",
        "url": "https://www.nytimes.com/svc/wordle/v2/",
        "funny_stuff": {
            "year": 2021,
            "month": 6,
            "day": 19
        }
    },
    {
        "name": "connections",
        "url": "https://www.nytimes.com/svc/connections/v2/",
        "funny_stuff": {
            "year": 2023,
            "month": 6,
            "day": 12
        }
    }
]

full_data = {}

failed_count = 0
fail_check = False

def funny(url:str, output:str, name:str):
    global fail_check, failed_count
    if failed_count >= 365:
        fail_check = True
        return
    output = outputdir+output

    mmmmmm = output.split("/")

    mmmmmm.pop(-1)
    
    os.makedirs('/'.join(mmmmmm), exist_ok=True)

    print(f"Grabbing: {output}")
    res = requests.get(url)
    
    if res.status_code == 404 or res.json().get("errors"):
        print(f"Failed: {output}")
        failed_count += 1
        return

    if not full_data.get(name):
        full_data[name] = []
    failed_count = 0
    with open(output, "w+") as f:
        json.dump(res.json(), f, indent=4)
        full_data[name].append(res.json())
        print(f"Grabbed: {output}\nData: {res.json()}")

def find_last_wordle():
    now = datetime.datetime.now()
    scanning_year = 0
    fuuu = requests.get(f"https://www.nytimes.com/svc/wordle/v2/{now.year+1}-01-01.json")
    print(f"fuuu: {fuuu.json()}")
    if fuuu.status_code != 404:
        scanning_year = now.year+1
    else:
        scanning_year = now.year

    scanning_month = 0
    funnyeeee_month = ""
    if scanning_year == now.year:
        for month in range(12-now.month):
            print(f"Month Check: {month+1}")
            funnyeeee_month = str(month+1+now.month)
            if month+1+now.month < 10:
                funnyeeee_month = "0"+funnyeeee_month
            feeeeee = requests.get(f"https://www.nytimes.com/svc/wordle/v2/{scanning_year}-{funnyeeee_month}-01.json")
            print(f"feeeeee: {feeeeee.json()}")
            if feeeeee.status_code != 404:
                scanning_month = month+now.month
                break
    else:
        for month in range(12):
            print(f"Month Check: {month+1}")
            funnyeeee_month = str(month+1)
            if month+1 < 10:
                funnyeeee_month = "0"+funnyeeee_month
            foooooo = requests.get(f"https://www.nytimes.com/svc/wordle/v2/{scanning_year}-{funnyeeee_month}-01.json")
            print(f"foooooo: {foooooo.json()}")
            if foooooo.status_code != 404:
                scanning_month = month
                break
    funnyeeee_month = str(scanning_month)

    scanning_day = 0
    funnyeeee_day = ""
    if scanning_month == now.month:
        for day in range(calendar.monthrange(scanning_year, scanning_month)[1]-now.day):
            print(f"Day Check: {day+1}")
            funnyeeee_day = str(day+1+now.day)
            if day+1+now.day < 10:
                funnyeeee_day = "0"+funnyeeee_day
            fahhhhhhhh = requests.get(f"https://www.nytimes.com/svc/wordle/v2/{scanning_year}-{funnyeeee_month}-{funnyeeee_day}.json")
            print(f"fahhhhhhhh: {fahhhhhhhh.json()}")

            if fahhhhhhhh.status_code != 404:
                scanning_day = day+now.day
                break
    else:
        for day in range(calendar.monthrange(scanning_year, scanning_month)[1]):
            print(f"Day Check: {day+1}")
            funnyeeee_day = str(day+1)
            if day+1 < 10:
                funnyeeee_day = "0"+funnyeeee_day
            fummmmmm = requests.get(f"https://www.nytimes.com/svc/wordle/v2/{scanning_year}-{funnyeeee_month}-{funnyeeee_day}.json")
            print(f"fummmmmm: {fummmmmm.json()}")

            if fummmmmm.status_code != 404:
                scanning_day = day
                break
    
    #print(f"Year: {scanning_year}\nMonth: {scanning_month}\nDay: {scanning_day}")
    print(f"Last Wordle: {scanning_month}/{scanning_day}/{scanning_year}")
    
    return {
        "day": scanning_day,
        "month": scanning_month,
        "year": scanning_year
    }

for thing in funny_urls:
    print(f"Grabbing {thing["name"].capitalize()}")
    failed_count = 0
    fail_check = False
    #funnies = find_last_wordle()

    # I am way too lazy to fix the system.
    funnies = {"day": 31, "month": 12, "year": 9999}

    for month in range(thing["funny_stuff"]["month"]):
        if fail_check == True:
            break
        stuff = calendar.monthrange(funnies["year"]+thing["funny_stuff"]["year"], month+1)[1]
        if funnies["year"] == funnies["year"] and month == funnies["month"]:
            stuff -= funnies["day"]
        for day in range(stuff):
            if fail_check == True:
                break
            funnyeeee_day = str(day+1)
            if day+1 < 10:
                funnyeeee_day = "0"+funnyeeee_day
            funnyeeee_month = str(month+1)
            if month+1 < 10:
                funnyeeee_month = "0"+funnyeeee_month
            res = requests.get(f"{thing["url"]}{thing["funny_stuff"]["year"]}-{funnyeeee_month}-{funnyeeee_day}.json")
            if res.status_code != 404:
                while True:
                    if len(threads) <= max_threads:
                        thread = threading.Thread(target=funny, args=(f"{thing["url"]}{thing["funny_stuff"]["year"]}-{funnyeeee_month}-{funnyeeee_day}.json", f"{thing["name"]}/{thing["funny_stuff"]["year"]}-{funnyeeee_month}-{funnyeeee_day}.json", thing["name"], ))
                        thread.start()
                        threads.append(thread)
                        break
                    else:
                        for thread in threads:
                            thread.join()
                        threads = []

    for year in range(funnies["year"]-thing["funny_stuff"]["year"]):
        if fail_check == True:
            break
        for month in range(funnies["month"]):
            if fail_check == True:
                break
            stuff = calendar.monthrange(year+thing["funny_stuff"]["year"], month+1)[1]
            if year == funnies["year"] and month == funnies["month"]:
                stuff -= funnies["day"]
            for day in range(stuff):
                if fail_check == True:
                    break
                funnyeeee_day = str(day+1)
                if day+1 < 10:
                    funnyeeee_day = "0"+funnyeeee_day
                funnyeeee_month = str(month+1)
                if month+1 < 10:
                    funnyeeee_month = "0"+funnyeeee_month
                
                while True:
                    if len(threads) <= max_threads:
                        thread = threading.Thread(target=funny, args=(f"{thing["url"]}{year+thing["funny_stuff"]["year"]}-{funnyeeee_month}-{funnyeeee_day}.json", f"{thing["name"]}/{year+thing["funny_stuff"]["year"]}-{funnyeeee_month}-{funnyeeee_day}.json", thing["name"],))
                        thread.start()
                        threads.append(thread)
                        break
                    else:
                        for thread in threads:
                            thread.join()
                        threads = []

    for thread in threads:
        thread.join()
    threads = []

with open(f"{outputdir}/full_dump.json", "w+") as f:
    json.dump(full_data, f, indent=4)