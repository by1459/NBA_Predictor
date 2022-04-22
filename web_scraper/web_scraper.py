import time
import csv

from bs4 import BeautifulSoup
from selenium import webdriver


class Web_Scraper:
    def __init__(self, given_url, table_rows, table_columns):
        self.TABLE_COLUMNS = table_columns
        self.TABLE_ROWS = table_rows
        chromedriver_path = "/usr/local/bin/chromedriver"
        driver = webdriver.Chrome(chromedriver_path)
        url = given_url
        header = ["RANKING", "TEAM"]
        driver.get(url)
        time.sleep(1)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        unformatted_header = soup.find_all(
            "th", attrs={"data-dir": "-1"}
        )
        for header_title in unformatted_header:
            header.append(header_title.text.strip())
        teams = soup.find_all(
            "td"
        )
        read_stats = [] * self.TABLE_ROWS
        read_stats.append(header)
        for i in range(self.TABLE_ROWS):
            row = []
            for j in range(len(header)):
                row.append(teams[i * self.TABLE_COLUMNS + j].text.strip())
            read_stats.append(row)
        f = open('nba_stats.csv', 'w')
        writer = csv.writer(f)
        for stats in read_stats:
            writer.writerow(stats)

        f.close()

test = Web_Scraper("https://www.nba.com/stats/teams/traditional/?sort=W&dir=-1&Season=2021-22&SeasonType=Regular%20Season", 30, 28)