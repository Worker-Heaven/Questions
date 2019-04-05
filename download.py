import csv
import sqlite3

def download_as_csv():
    db_name = 'answers.db'

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # c.execute('''CREATE TABLE if not exists account_executive
    #              (question, answer, category, category_link, sub_category, sub_category_link, multi_choice)''')

    with open('result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Question', 'Answer', 'Category', 'Category Link', 'Sub Category', 'Sub Category Link', 'Multi Choice'])

    for (question, answer, category, category_link, sub_category, sub_category_link, multi_choice) in c.execute('SELECT * from account_executive'):
        print(question, answer, category, category_link, sub_category, sub_category_link, multi_choice)

        with open('result.csv', 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([question, answer, category, category_link, sub_category, sub_category_link, multi_choice])
    
    conn.close()

if (__name__ == '__main__'):
    download_as_csv()