import requests
from lxml import html
import sqlite3

from config import site_lists


db_name = 'answers.db'

category = 'Accounting'
category_link = 'https://interviewquestionsanswers.org/Accounting'


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


def init_db():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists account_executive
                 (question, answer, category, category_link, sub_category, sub_category_link, multi_choice)''')
    
    conn.commit()
    conn.close()


def store_to_db(question, answer, category, category_link, sub_category, sub_category_link, multi_choice):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO account_executive VALUES (?,?,?,?,?,?,?)", (
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


def start_scraping():
    table_name = 'account_executive'
    scid = 2113

    sub_category = 'Account Executive Interview'
    sub_category_link = 'https://interviewquestionsanswers.org/_Account-Executive'

    initial_response = requests.get(sub_category_link)
    initial_page = html.fromstring(initial_response.text)

    contents = initial_page.xpath('//div[@class="main-content"]//div[@class="answer"]')

    for item in contents:
        question = item.xpath('.//p[1]//a/text()')[0]
        answer = item.xpath('.//p[2]/text()')[0]

        print('---------------------------')
        print(''.join(answer))

        store_to_db(
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
        params = {
            'action': 'get',
            'last_qid': (str)(last_index),
            'scid': str(scid),
        }

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

                print('---------------------------')
                print(''.join(answer))

                store_to_db(
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
    init_db()
    start_scraping()