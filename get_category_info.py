import requests
from lxml import html
import sqlite3

db_name = 'all_answers.db'
table_name = 'category_list'

site_url = 'https://interviewquestionsanswers.org'


def get_category_info():
    response = requests.get(site_url)
    page = html.fromstring(response.text)

    contents = page.xpath('//div[@class="content"]//h2')

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists {} (label, link)'''.format(table_name))

    for item in contents:
        label = item.xpath('.//a/text()')[0]
        link = item.xpath('.//a/@href')[0]

        print(label, site_url+link)
        c.execute("INSERT INTO {} VALUES (?,?)".format(table_name), (label, site_url+link))

    conn.commit()
    conn.close()

if (__name__ == '__main__'):
    get_category_info()