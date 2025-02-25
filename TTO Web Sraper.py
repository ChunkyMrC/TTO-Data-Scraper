import csv
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import requests
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys 
import itertools
from difflib import SequenceMatcher
import urllib.request, json
import re
from googlesearch import search
import googlesearch
import os
import shutil
import glob, os

###################### TTO USERNAME & PASSWORD ####################

while True:
    username = input("Enter your the email address you use for TTO: ")
    reg = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(reg, username):
        print("Valid email.")
        break
    else:
        print("Invalid email.")

while True:
    password = input("Enter your TTO password: ")
    if isinstance(password, str) and len(password) >= 4:
        print("Valid password.")
        break
    else:
        print("Invalid password.")

######################  Start and End Dates #####################

while True:
    start_dt = input("Enter the start date (DD/MM/YY): ")
    try:
        input_date = datetime.strptime(start_dt, "%d/%m/%y")
        print("Start date valid")
        start_dt = input_date.date()
        break
    except ValueError:
        print("Start date invalid")

while True:
    end_dt = input("Enter the end date (DD/MM/YY): ")
    try:
        input_date = datetime.strptime(end_dt, "%d/%m/%y")
        print("End date valid")
        end_dt = input_date.date()
        break
    except ValueError:
        print("End date invalid")

delta = timedelta(days=1)
dates_to_search = set()
dates_to_search.add(end_dt)

while start_dt <= end_dt:
    dates_to_search.add(start_dt)
    start_dt += delta

####################### GET TTO DATA ##########################
all_data = set()
url = "https://tilttheodds.co.uk/profile-page"
header = {'Accept' : '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',}
content = requests.get(url, headers = header)
options = webdriver.ChromeOptions()
options.set_capability('goog:loggingPrefs', {"performance": "ALL", "browser": "ALL"})
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
driver.set_page_load_timeout(10)
try:
    driver.get(url)
except:
    pass
sleep(2)
username_box = driver.find_element(By.XPATH, "//input[@name='username']")
username_box.click()
username_box.send_keys(username)
password_box = driver.find_element(By.XPATH, "//input[@name='password']")
password_box.click()
password_box.send_keys(password)
password_box.send_keys(Keys.RETURN)

sleep(5)

def get_horse_data(date):
    html_source_code = driver.execute_script("return document.body.innerHTML;")
    soup: BeautifulSoup = BeautifulSoup(html_source_code, 'html.parser')
    cards = soup.find_all("div", {"class": "card custom-card card-pointer card"})
    for card in cards:
        card_rows = card.find_all("div", {"class": "row"})
        for row in card_rows:
            relevant_row = row.find_all("div", {"class": "bet-card-p race-padding-lg d-none d-sm-block text-left row"})
            if len(relevant_row) > 0:
                racetrack = row.find_all("div", {"class": "bet-card-p race-padding-lg d-none d-sm-block text-left row"})[0].text.split(":")[1][3::].strip()
                t = row.find_all("div", {"class": "bet-card-p race-padding-lg d-none d-sm-block text-left row"})[0].text.split(" ")[1].strip()
                runner = row.find_all("p", {"class": "text-fix-small"})[0].text.split("(")[0].strip()
                qs = row.find_all("p", {"class": "text-fix-small"})[0].text.split("(")[1].split("qs")[0].strip()
                odds = row.find_all("p", {"class": "text-fix-small"})[0].text.split("@")[1].strip()
                percentage = row.find_all("p", {"class": "text-fix-small"})[0].text.split("%")[0].split(":")[1].strip()
                if len(row.find_all("i", {"class": "betcard-icon-win now-ui-icons sport_trophy"})) > 0:
                    win_lose = 1
                elif len(row.find_all("i", {"class": "now-ui-icons ui-1_simple-remove betcard-icon-lose"})) > 0:
                    win_lose = 0
                else:
                    win_lose = "NR"
                bet_type = card.find_all("div", {"class": "custom-card-header card-header"})[0].text.split("~")[0].strip()
                all_data.add((date, t, racetrack, runner, qs, odds, percentage, win_lose, bet_type))

def click_through_pages(date):
    driver.execute_script("window.scrollTo(0, 500)")
    sleep(5)
    get_horse_data(date)
    for i in range(2,10):
        try:
            driver.find_element(By.XPATH, "//button[text()=" + str(i)+"]").click()
            get_horse_data(date)
            sleep(5)
        except Exception as e:
            break

for date in dates_to_search:
    date = date.strftime("%Y-%m-%d")
    print("Now searching", date)
    url = "https://tilttheodds.co.uk/profile-page/bets/" + date
    try:
        driver.get(url)
        sleep(5)
        click_through_pages(date)
    except:
        pass

driver.quit()

print(all_data)