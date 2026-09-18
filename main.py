import sys
import random
import string
import json
from urllib.parse import urlparse

if len(sys.argv) < 2:
    print("Please enter a command: shorten, resolve, or list")
    sys.exit()

command = sys.argv[1]

if command == "shorten":
    if len(sys.argv) < 3:
        print("Please provide a URL.")
        sys.exit()

    url = sys.argv[2]
    alias = None

    if len(sys.argv) >= 5 and sys.argv[3] == "--alias":
        alias = sys.argv[4]
    
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        print("Invalid URL.")
        sys.exit()

    with open("data.json", "r") as file:
      data = json.load(file)
    
    for code, saved_url in data.items():
      if saved_url == url:
        print("URL already shortened.")
        print("Short code:", code)
        sys.exit()
    if alias:
        code = alias
    else:
        characters = string.ascii_letters + string.digits
        code = ""

        for i in range(6):
            code = code + random.choice(characters)

    with open("data.json", "r") as file:
        data = json.load(file)

    if alias and alias in data:
        print("Alias already exists.")
        sys.exit()    

    data[code] = url

    with open("data.json", "w") as file:
        json.dump(data, file)

    print("Your short code is:", code)


elif command == "resolve":
    if len(sys.argv) < 3:
        print("Please provide a short code.")
        sys.exit()

    code = sys.argv[2]

    with open("data.json", "r") as file:
        data = json.load(file)

    if code in data:
        print("Your original URL is:", data[code])
    else:
        print("Short code not found.")

elif command == "list":
    with open("data.json", "r") as file:
        data = json.load(file)

    for code, url in data.items():
        print(code, "->", url)
else:
    print("Unknown command. Use shorten, resolve, or list.")
