import time
import csv

from bs4 import BeautifulSoup
from selenium import webdriver


def get_season_stats(given_url, table_rows, table_columns):
    # Loading the website
    chromedriver_path = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chromedriver_path)
    url = given_url
    driver.get(url)

    # Getting the HTML data from the website
    time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Finding the table columns
    header = ["RANKING", "TEAM"]
    unformatted_header = soup.find_all(
        "th", attrs={"data-dir": "-1"}
    )
    for header_title in unformatted_header:
        header.append(header_title.text.strip())

    # Getting the stats itself from an individual season
    teams = soup.find_all(
        "td"
    )
    read_stats = [] * table_rows
    read_stats.append(header)
    for i in range(table_rows):
        row = []
        for j in range(len(header)):
            row.append(teams[i * table_columns + j].text.strip())
        read_stats.append(row)

    # Writing the stats to the CSV file
    f = open('nba_stats.csv', 'w')
    writer = csv.writer(f)
    for stats in read_stats:
        writer.writerow(stats)
    f.close()


get_season_stats(
    "https://www.nba.com/stats/teams/traditional/?sort=W&dir=-1&Season=2021-22&SeasonType=Regular%20Season", 30, 28)
