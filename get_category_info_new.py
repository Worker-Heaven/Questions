import requests
from lxml import html
import sqlite3

db_name = 'windows_interview.db'
table_name = 'category_list'

site_url = 'https://www.globalguideline.com/interview_questions/'


def get_category_info():
    response = requests.get(site_url)
    page = html.fromstring(response.text)

    contents = page.xpath('//div[@id="main-page-content"]//article')

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists {} (label, link)'''.format(table_name))

    for item in contents:
        link = item.xpath('.//h3/a/@href')[0]
        label = item.xpath('.//h3/a/text()')[0]

        print(label, site_url+link)
        c.execute("INSERT INTO {} VALUES (?,?)".format(table_name), (label[:-1], site_url+link))

    conn.commit()
    conn.close()

if (__name__ == '__main__'):
    get_category_info()