import sqlite3
import re
import os
from shutil import copy

db_name = 'well_map.db'

base_path = './maps'

def extract_lat_lang():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for (well, location) in c.execute('SELECT * FROM result'):
        filtered_well_name = ''.join([x for x in well if not x in '/"'])

        path = base_path + '/' + filtered_well_name.strip()
        os.mkdir(path)
        copy('./index.html', path)


        lat = re.search('ll=(-?[\d\.]*)', location)
        lang = re.search('ll=[-?\d\.]*\,([-?\d\.]*)', location)
        
        info = {
            'lat': lat.group(1),
            'lng': lang.group(1),
        }

        location_info = 'data = ' + str(info)

        with open(path+'/location.js', 'w') as outfile:
            outfile.write(location_info)

        print(lat.group(1), lang.group(1))

    conn.close()


if __name__ == '__main__':
    os.mkdir(base_path)

    extract_lat_lang()