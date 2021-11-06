import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")

url = "https://www.iban.com/currency-codes"

iban_result = requests.get(url)

iban_soup = BeautifulSoup(iban_result.text, 'html.parser')

table = iban_soup.table

trs = table.find_all('tr')

print("Hello! Please choose select a country by number: ")

country_list=[]

country_from=[]

country_to=[]

def exchange():
    try:
        code_from = country_from[0]['code'].lower()
        code_from_upper = code_from.upper()
        code_to = country_to[0]['code'].lower()
        code_to_upper = code_to.upper()
        print(f"\nHow many {code_from_upper} do you want to convert to {code_to_upper}?")
        amount=int(input("\n#: "))
        exchange_url = f"https://wise.com/gb/currency-converter/{code_from}-to-{code_to}-rate?amount={amount}"
        exchange_result = requests.get(exchange_url)
        exchange_soup = BeautifulSoup(exchange_result.text, 'html.parser')
        calculator = exchange_soup.find("div", id="calculator")
        convert_from = int(calculator.find("input", id="cc-amount-from")['value'])
        convert_from_format = format_currency(convert_from, code_from_upper, locale='en_US')
        convert_ratio = float(calculator.find("span","text-success").text)
        convert_to = convert_from*convert_ratio
        convert_to_fromat = format_currency(convert_to, code_to_upper, locale='en_US')
        print(f"\n{convert_from_format} is {convert_to_fromat}")
    except:
        print("\nSorry, we don't have data for does currencies.")

def index(country_number, where):
    if where == 'from':
        try:
            res = country_list[country_number-1]
            country = res['country']
            code = res['code']
            currency = res['currency']
            country_from.append({
                "country":country,
                "code":code,
                "currency":currency
                })            
            ask_to()
        except:
            print("\nChoose a number from the list.")
            ask_from()
    elif where == 'to':
        try:
            res = country_list[country_number-1]
            country = res['country']
            code = res['code']
            currency = res['currency']
            country_to.append({
                "country":country,
                "code":code,
                "currency":currency
                })
            exchange()
        except:
            return

def ask_from():
    try:
        print("\nWhere are you from? Choose a country by number.")
        where_from = int(input("\n#: "))
        index(where_from, "from")
    except:
        print("\nThat's not a number.")
        ask_from()

def ask_to():
    try:
        print("\nNow choose another country.")
        country_to = int(input("\n#: "))
        index(country_to, "to")
    except:
        print("\nThat's not a number.")
        ask_to()

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
            "currency":currency,
            })
        print("#", idx,country, code)

ask_from()