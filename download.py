import csv
import sqlite3

def download_as_csv():
    db_name = 'well_map.db'

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    with open('well_map_result.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Wells', 'Location'])

    for (well, location) in c.execute('SELECT * from result'):
        print(well, location)

        with open('well_map_result.csv', 'a+', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([well, location])
    
    conn.close()

if (__name__ == '__main__'):
    download_as_csv()