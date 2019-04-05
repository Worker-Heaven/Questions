import requests
from lxml import html
import sqlite3

from config import site_lists



db_name = 'answers.db'

url = 'https://interviewquestionsanswers.org/getPageDataV2.php'
headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'content-length': '0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://interviewquestionsanswers.org',
    'referer': 'https://interviewquestionsanswers.org/_Account-Executive',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


def init_db(site_info):
    table_name = site_info.get('table_name')

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists {}
                 (question, answer, category, category_link, sub_category, sub_category_link, multi_choice)'''.format(table_name))
    
    conn.commit()
    conn.close()


def store_to_db(table_name, question, answer, category, category_link, sub_category, sub_category_link, multi_choice):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO {} VALUES (?,?,?,?,?,?,?)".format(table_name), (
        question,
        answer,
        category,
        category_link,
        sub_category,
        sub_category_link,
        multi_choice,
    ))

    conn.commit()
    conn.close()


def start_scraping(site_info):
    # NOTE: Get site info
    table_name = site_info.get('table_name')
    scid = site_info.get('scid')

    category = site_info.get('category')
    category_link = site_info.get('category_url')

    sub_category = site_info.get('sub_category')
    sub_category_link = site_info.get('sub_category_link')

    # NOTE: actually start the scraping
    initial_response = requests.get(sub_category_link)
    initial_page = html.fromstring(initial_response.text)

    contents = initial_page.xpath('//div[@class="main-content"]//div[@class="answer"]')

    for item in contents:
        question = item.xpath('.//p[1]//a/text()')[0]
        answer = item.xpath('.//p[2]/text()')[0]

        # print('---------------------------')
        # print(''.join(answer))

        store_to_db(
            table_name,
            question[question.find('.')+1:],
            ''.join(answer),
            category,
            category_link,
            sub_category,
            sub_category_link,
            '-', 
        )

    string_ids = initial_page.xpath('//div[@class="main-content"]//div[@class="answer"]/@id')
    ids = [int(id[id.find('_')+1:]) for id in string_ids]

    last_index = ids[-1]

    while(True):
        # if last_index < 39739 and last_index >= 16746:
        #     last_index = 16746
        # if last_index < 5134 and last_index >= 4172:
        #     last_index = 4172       
        # if last_index < 16741: break

        params = {
            'action': 'get',
            'last_qid': (str)(last_index),
            'scid': str(scid),
        }

        print(last_index)

        response = requests.post(url, headers=headers, params=params)
        
        # print('status code', response.status_code)
        # print('response text', len(response.text))

        if (len(response.text) == 0): break

        if (response.status_code == 200):
            page = html.fromstring(response.text)
            main_content = page.xpath('//div[@class="answer"]')

            for item in main_content:
                question = item.xpath('.//p[1]//a/text()')[0]
                answer = item.xpath('.//p[2]/text()')

                store_to_db(
                    table_name,
                    question[question.find('.')+1:],
                    ''.join(answer),
                    category,
                    category_link,
                    sub_category,
                    sub_category_link,
                    '-',
                )
        
        last_index -= 5
    
    print('Completed!')


if (__name__ == '__main__'):
    for site_info in site_lists:
        init_db(site_info)
        start_scraping(site_info)