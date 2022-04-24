import time
import csv

from bs4 import BeautifulSoup
from selenium import webdriver


class Website_Scraper:
    def __init__(self, given_url):
        # Loading the website
        chromedriver_path = "/usr/local/bin/chromedriver"
        driver = webdriver.Chrome(chromedriver_path)
        url = given_url
        driver.get(url)

        # Getting the HTML data from the website
        time.sleep(1)
        page_source = driver.page_source
        self.soup = BeautifulSoup(page_source, 'html.parser')
        self.years = -1

    def get_season_stats(self, table_rows, table_columns):
        # Finding the table columns
        header = ["RANKING", "TEAM"]
        unformatted_header = self.soup.find_all(
            "th", attrs={"data-dir": "-1"}
        )
        for header_title in unformatted_header:
            header.append(header_title.text.strip())

        # Getting the stats itself from an individual season
        teams = self.soup.find_all(
            "td"
        )
        read_stats = [] * table_rows
        read_stats.append(header)
        for i in range(table_rows):
            row = []
            for j in range(len(header)):
                row.append(teams[i * table_columns + j].text.strip())
            read_stats.append(row)

    def get_years(self, num_years):
        self.years = num_years
        years = [] * num_years
        unformatted_years = self.soup.find_all(
            "option"
        )
        for i in range(num_years):
            years.append(unformatted_years[i].text.strip())
        return years

    def write_csv(self, all_stats):
        # Writing the stats to the CSV file
        f = open('nba_stats.csv', 'w')
        writer = csv.writer(f)
        for stats in all_stats:
            writer.writerow(stats)
        f.close()


def main():
    website_scraper = Website_Scraper(
        "https://www.nba.com/stats/teams/traditional/?sort=W_PCT&dir=-1&Season=2021-22&SeasonType=Regular%20Season")
    years = website_scraper.get_years(26)
    for year in years:




if __name__ == "__main__":
    main()
