import csv
import sqlite3

db_name = 'all_answers.db'

def download_to_csv():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for name, in c.execute('SELECT name FROM sqlite_master WHERE type ="table" AND name NOT LIKE "sqlite_%" '):
        print(name)

    conn.close()


if __name__ == '__main__':
    download_to_csv()