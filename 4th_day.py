import os
import sys
import requests

path = os.path.abspath(__file__)
filename = os.path.basename(path)

def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)

def validation_fail(URL):
    print(f"{URL} is not a valid URL.")
    start_over()

def start_over():
    answer = input("Do you want to start over? y/n\n")
    if answer == "y":
        restart()
    elif answer == "n":
        print("k. bye!")
    else: 
        print("That's not valid answer.")
        start_over() 

def is_up(URL):
    try:
        res = requests.get(URL)
        if res.ok is True:
            print(f"{URL} is up!")
        elif res.ok is False:
            print(f"{URL} is down!")
    except:
        print(f"{URL} is down!")

print(f"Welcome to {filename}!")
URLs = input("Please write a URL or URLs you want to check. (separated by comma)\n")

URL_list = URLs.split(",")

for URL in URL_list:
    URL = URL.strip().lower()
    if URL.find(".") > 0:
        if URL[0:4] != "http":
            URL="http://"+URL
        is_up(URL)
    else:
        validation_fail(URL)

start_over()