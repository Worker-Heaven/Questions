from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html
import requests

import sqlite3

import time
import re

import string

# NOTE: Share chrome drive across the whole code base
chrome_options = webdriver.ChromeOptions()
chromedriver_path = "E:/Utilities/chromedriver.exe"


driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
driver.implicitly_wait(300)

base_link = 'http://www.ogsrlibrary.com/wellcards/result.php?q=&wt=Natural%20Gas%20Well&wm=Active%20Well&btn=Advanced%20Search&lng=-&rad=10000&s='

db_name = 'well_map.db'

def init_db(table_name):
    print(type(table_name))

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("CREATE TABLE if not exists '{}' (well, location)".format(table_name))

    conn.commit()
    conn.close()


def store_to_db(table_name, well, location):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO '{}' VALUES (?,?)".format(table_name), (
        well,
        location,
    ))

    conn.commit()
    conn.close()

def start_scraping():
    table_name = 'result'

    init_db(table_name)

    for index in range(0, 1151, 10):
        driver.get(base_link + str(index))
        time.sleep(5)

        # response = requests.get(base_link + str(0))
        # page = html.fromstring(response.text)

        page = html.fromstring(driver.page_source)

        #NOTE: main content
        data = page.xpath('//table//tr[@height="30"]')

        for record in data:
            height = record.xpath('.//@height')[0]

            location = record.xpath('.//td[1]//a[@target="_blank"]//@href')[0]
            well = record.xpath('.//td[2]//a/text()')[0]

            print(well)

            store_to_db(table_name, well, location)

        


if __name__ == '__main__':
    start_scraping()