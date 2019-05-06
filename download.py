import csv
import sqlite3

def download_as_csv():
    db_name = 'well_map.db'
    base_path = 'D:\\maps\\'

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    with open('well_map_result_local.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Wells', 'Location'])

    for (well, location) in c.execute('SELECT * from result'):
        # print(well, location)
        filtered_well_name = ''.join([x for x in well if not x in '/"'])

        path = base_path + filtered_well_name.strip() + '\\' + 'index.html'

        with open('well_map_result_local.csv', 'a+', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([well, path])
    
    conn.close()

if (__name__ == '__main__'):
    download_as_csv()


    can you see `http://` or `https://` in 