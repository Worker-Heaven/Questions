from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html

import sqlite3

import time
import re

import string

from selenium.webdriver.chrome.options import Options

# NOTE: Share chrome drive across the whole code base
# chrome_options = webdriver.ChromeOptions()
chromedriver_path = "E:/Utilities/chromedriver.exe"
options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
driver.implicitly_wait(300)

base_link = 'https://www.globalguideline.com/interview_questions/'

db_name = 'windows_interview.db'


def init_db(table_name):
    print(type(table_name))

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("CREATE TABLE if not exists '{}' (question, answer, category, category_link, sub_category, sub_category_link)".format(table_name))

    conn.commit()
    conn.close()



def store_to_db(table_name, question, answer, category, category_link, sub_category, sub_category_link):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO '{}' VALUES (?,?,?,?,?,?)".format(table_name), (
        question,
        answer,
        category,
        category_link,
        sub_category,
        sub_category_link,
    ))

    conn.commit()
    conn.close()




def goto_end_page(site_url):
    driver.get(site_url)
    time.sleep(5)

    saved_size = 0

    while True:
        main_content = driver.find_elements_by_xpath('//div[@id="questions"]//div[@class="qa_box"]')

        if (saved_size == len(main_content)): break

        print('--->', len(main_content))

        saved_size = len(main_content)

        # NOTE: Scroll down to the end of the page
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(5)


def start_scraping(category_info):
    category_url = category_info.get('link')

    driver.get(category_url)
    time.sleep(5)

    page = html.fromstring(driver.page_source)
    subcategory_elems = page.xpath('//div[@id="main-page-content"]//article[@class="categoryDescr"]')

    for subcategory_elem in subcategory_elems:
        subcategory_label = subcategory_elem.xpath('.//h3//span/text()')[0]
        subcategory_link = base_link + subcategory_elem.xpath('.//a/@href')[0]

        table_name = ''.join([x for x in subcategory_label.lower() if not x in '\t\r\v\f::\n().,-/+&'])
        table_name = '_'.join(table_name.split(' '))


        print(subcategory_label, subcategory_link)
        print('table_name--->', table_name)

        # init_db(table_name)


        # NOTE: GO TO END OF THE PAGE
        goto_end_page(subcategory_link)


        subcategory_page = html.fromstring(driver.page_source)
        contents = subcategory_page.xpath('//div[@id="questions"]//div[@class="qa_box"]')

        for item in contents:
            raw_question = ''.join(item.xpath('.//h3[@class="question_box"]//a/text()'))
            raw_answer = ''.join(item.xpath('.//div[@class="answer_box"]/text()'))

            question = ''.join([x for x in raw_question if not x in '\t\r\v\f::\n'])
            answer = ''.join([x for x in raw_answer if not x in '\t\r\v\f'])

            print('---------------------------')
            print('question', question)
            print('answer', answer)

            # store_to_db(
            #     table_name,
            #     question,
            #     answer,
            #     category_info.get('label'),
            #     category_info.get('link'),
            #     subcategory_label,
            #     subcategory_link,
            # )



if (__name__ == '__main__'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('SELECT * from category_list')
    category_list = c.fetchall()

    conn.close()

    category_list.reverse()

    for (label, link) in category_list:
        category_info = {
            'label': label,
            'link': link,
        }

        print(label, link)

        start_scraping(category_info)