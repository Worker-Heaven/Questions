from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from lxml import html
import sqlite3

import time

# NOTE: Share chrome drive across the whole code base
chrome_options = webdriver.ChromeOptions()
chromedriver_path = "E:/Utilities/chromedriver.exe"

driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
driver.implicitly_wait(300)

base_link = 'https://interviewquestionsanswers.org/'

db_name = 'all_answers.db'

def init_db(table_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists {}
                 (question, answer, category, category_link, sub_category, sub_category_link)'''.format(table_name))
    
    conn.commit()
    conn.close()



def store_to_db(table_name, question, answer, category, category_link, sub_category, sub_category_link):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO {} VALUES (?,?,?,?,?,?)".format(table_name), (
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
        main_content = driver.find_elements_by_xpath('//div[@class="main-content"]//div[@class="answer"]')

        if (saved_size == len(main_content)): break

        saved_size = len(main_content)
        
        # NOTE: Scroll down to the end of the page
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(3)


def start_scraping(category_info):
    category_url = category_info.get('link')

    driver.get(category_url)
    time.sleep(5)

    page = html.fromstring(driver.page_source)
    subcategory_elems = page.xpath('//div[@id="leftmenuinnerinner"]//a[@target="_top"]')

    for subcategory_elem in subcategory_elems:
        subcategory_label = subcategory_elem.xpath('.//text()')[0]
        subcategory_link = base_link + subcategory_elem.xpath('.//@href')[0]

        # NOTE: GO TO END OF THE PAGE
        goto_end_page(subcategory_link)

        table_name = '_'.join(subcategory_label.lower().split(' '))
        init_db(table_name)

        subcategory_page = html.fromstring(driver.page_source)
        contents = subcategory_page.xpath('//div[@class="main-content"]//div[@class="answer"]')

        for item in contents:
            question = item.xpath('.//p[1]//a/text()')[0]
            answer = item.xpath('.//p[2]/text()')

            print('---------------------------')
            print(''.join(answer))

            store_to_db(
                table_name,
                question[question.find('.')+1:],
                ''.join(answer),
                category_info.get('label'),
                category_info.get('link'),
                subcategory_label,
                subcategory_link,
            )



if (__name__ == '__main__'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for (label, link) in c.execute('SELECT * from category_list'):
        category_info = {
            'label': label,
            'link': link,
        }

        # category_info = {
        #     'label': 'Adobe',
        #     'link': 'https://interviewquestionsanswers.org/Adobe',
        # }

        start_scraping(category_info)