import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

iban_result = requests.get(url)

iban_soup = BeautifulSoup(iban_result.text, 'html.parser')

table = iban_soup.table

trs = table.find_all('tr')

print("Hello! Please choose select a country by number: ")

country_list=[]

def index(country_number):
    try:
        res = country_list[country_number-1]
        country = res['country']
        code = res['code']
        print(f"You chose {country}")
        print(f"The currency code is {code}")
    except:
        print("Choose a number from the list.")
        req()

def req():
    try:
        country_number = int(input("#: "))
        index(country_number)
    except:
        print("That's not a number.")
        req()

for idx, tr in enumerate(trs): 
    if idx > 0:
        tds = tr.find_all('td')
        country = tds[0].text.strip()
        country = str(country).capitalize()
        currency = tds[1].text.strip()
        code = tds[2].text.strip()
        number = tds[3].text.strip()

        country_list.append({
            "idx":idx, 
            "country": country,
            "code": code,
            })

        print("#", idx,country)

req()