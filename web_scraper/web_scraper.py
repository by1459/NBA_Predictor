import time
import csv

from bs4 import BeautifulSoup
from selenium import webdriver


class WebsiteScraper:
    def __init__(self, given_url, champs_url, year, time_span):
        # Loading the website
        chromedriver_path = "/usr/local/bin/chromedriver"
        driver1 = webdriver.Chrome(chromedriver_path)
        driver2 = webdriver.Chrome(chromedriver_path)
        url1 = given_url
        driver1.get(url1)
        url2 = champs_url
        driver2.get(url2)

        # Getting the HTML data from the website
        time.sleep(1)
        page_source1 = driver1.page_source
        page_source2 = driver2.page_source
        self.soup = BeautifulSoup(page_source1, 'html.parser')
        self.soup_champs = BeautifulSoup(page_source2, 'html.parser')
        self.year = year
        self.time_span = time_span

    def get_season_stats(self, table_rows, table_columns, header):
        # Getting the stats itself from an individual season
        teams = self.soup.find_all(
            "td"
        )
        read_stats = [] * table_rows
        for i in range(table_rows):
            row = []
            for j in range(len(header)):
                row.append(teams[i * table_columns + j].text.strip())
            read_stats.append(row)
        return read_stats

    def get_headers(self, preset_headers):
        # Finding the table columns
        header = preset_headers
        unformatted_header = self.soup.find_all(
            "th", attrs={"data-dir": "-1"}
        )
        for header_title in unformatted_header:
            header.append(header_title.text.strip())
        return header

    def get_champs(self):
        unformatted_champs = self.soup_champs.find_all(
            "td", attrs={"data-stat": "champion"}
        )
        unformatted_champs.pop(0)
        champs = []
        for i in range(self.time_span):
            champs.append(unformatted_champs[i].text.strip())
        return champs

    def get_years(self, num_years):
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
    TIME_SPAN = 26
    website_scraper = WebsiteScraper(
        "https://www.nba.com/stats/teams/traditional/?sort=W_PCT&dir=-1&Season=2021-22&SeasonType=Regular%20Season",
    "https://www.basketball-reference.com/playoffs/", 2022, TIME_SPAN)
    website_scraper.get_champs()
    years = website_scraper.get_years(26)
    dataset = [website_scraper.get_headers(["WINNER", "RANKING", "TEAM"])]
    print(dataset)
    #for year in years:
    #    print(year)


if __name__ == "__main__":
    main()
