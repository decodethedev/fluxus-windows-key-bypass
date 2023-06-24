import requests
import re
import os

linkvertise = "https://linkvertise.com/"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x66) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

link = input("Enter Key Link: ")

match = re.search(r"HWID=([a-f0-9]+)", link)
if match:
    hwid = match.group(1)
else:
    print("Invalid link, exiting...")
    os.exit(1)

print(f"Got HWID: {hwid}")

key_regex = r'let content = \("([^"]+)"\);'
endpoints =  [
    # {
    #     "url": f"https://flux.li/windows/start.php?HWID={hwid}",
    #     "referer": ""
    # }, You can skip these links, they are not needed
    {
        "url": f"https://flux.li/windows/start.php?cf331c115dc1fda3067c0e3d3a8bda76=true&HWID={hwid}",
        "referer": f"https://flux.li/windows/start.php?HWID={hwid}"
    },
    # {
    #     "url": "https://fluxteam.net/windows/checkpoint/check1.php",
    #     "referer": linkvertise
    # }, You can skip these links, they are not needed
    # {
    #     "url": "https://fluxteam.net/windows/checkpoint/check2.php",
    #     "referer": linkvertise
    # }, You can skip these links, they are not needed
    {
        "url": "https://fluxteam.net/windows/checkpoint/main.php",
        "referer": linkvertise
    },
]

for i in range (len(endpoints)):
    url = endpoints[i]["url"]
    referer = endpoints[i]["referer"]

    headers["referer"] = referer
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        with open("bypass.html", "w") as f:
            f.write(response.text)
        print(f"[{i}] Failed to bypass | Status code: {response.status_code}| Response content has been written to bypass.html for debugging purposes.")

    print(f"[{i}] Response: {response.status_code}")

    if i == len(endpoints)-1: # End of the bypass
        match = re.search(key_regex, response.text)
        if match:
            content = match.group(1)
            print(f"Bypassed successfully! Code: {content}")
        else:
            with open("bypass.html", "w") as f:
                f.write(response.text)
            print("Bypassed not successfully! Code: None, response content has been written to bypass.html for debugging purposes.")