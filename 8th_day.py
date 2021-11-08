import os
import csv
import requests
from bs4 import BeautifulSoup
import math

os.system("clear")

alba_url = "http://www.alba.co.kr"


def get_soup(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    return soup


def make_file(brand_name):
    try:
        file = open(f"{brand_name}.csv", mode="w")
        writer = csv.writer(file)
        writer.writerow(["위치", "지점", "근무시간", "급여", "작성시간"])
    except:
        brand_name = brand_name.replace("/", ",")
        file = open(f"{brand_name}.csv", mode="w")
        writer = csv.writer(file)
        writer.writerow(["위치", "지점", "근무시간", "급여", "작성시간"])


def save_file(brand_name, location, branch, time, pay, timestamp):
    try:
        file = open(f"{brand_name}.csv", mode="a")
        writer = csv.writer(file)
        writer.writerow([location, branch, time, pay, timestamp])
    except:
        brand_name = brand_name.replace("/", ",")
        file = open(f"{brand_name}.csv", mode="a")
        writer = csv.writer(file)
        writer.writerow([location, branch, time, pay, timestamp])


def extract_jobs(brand_name, url):
    brand_soup = get_soup(url)
    contents = brand_soup.find("div", id="NormalInfo")
    job_num = contents.find("strong").text

    if job_num.find(",") == True:
        job_num = job_num.replace(",", "")
        job_num = int(job_num)
    elif int(job_num) == 0:
        pass
    else:
        job_num = int(job_num)

    page_num = math.ceil(job_num / 50)

    for idx, page in enumerate(range(page_num)):
        try:
            idx += 1
            # 브랜드 디테일 수프
            soup = get_soup((url + f"job/brand/?page={idx}&pagesize=50"))
            normal_info = soup.find("div", id="NormalInfo")
            table = normal_info.find("table")
            tbody = table.find("tbody")
            print("Now Crawling :", url + f"job/brand/?page={idx}&pagesize=50")
            for tr in tbody:
                # 구인 태그 거르기
                try:
                    if len(tr["class"]) == 0:
                        location = tr.find("td", "local first").text
                        branch = tr.find("span").text
                        time = tr.find("td", "data").text
                        pay = tr.find("td", "pay").text
                        timestamp = tr.find("td", "regDate last").text
                        save_file(brand_name, location, branch, time, pay, timestamp)
                except:
                    pass
        except:
            pass


alba_soup = get_soup(alba_url)

super_brand = alba_soup.find("div", id="MainSuperBrand")

brands = super_brand.find("ul", "goodsBox")

brands = brands.find_all("li", class_="impact")


for brand in brands:
    brand_detail = brand.find("a", "goodsBox-info")
    brand_name = brand_detail.find("span", "company").text
    brand_url = brand_detail["href"]
    make_file(brand_name)
    extract_jobs(brand_name, brand_url)

print("----------Crawling is done----------")
