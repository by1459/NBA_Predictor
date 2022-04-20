import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

chromedriver_path = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chromedriver_path)
url = "https://www.nba.com/stats/teams/traditional/?sort=W_PCT&dir=-1&Season=2021-22&SeasonType=Regular%20Season"
stats = []

driver.get(url)
time.sleep(1)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
#print(soup)
teams = soup.find_all(
    "td"
)
for team in teams:
    print(team.text.strip())
    """
    stat = team.next
    if stat.name == "a":
        stats.append(stat.name)
    else:
        stats.append(team.next)
    """
#for stat in stats:
 #   print(stat)

