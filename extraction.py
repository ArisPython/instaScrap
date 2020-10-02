import json
import requests
import time
import csv

# data request URL pada tab Headers>General
url = 'https://www.instagram.com/graphql/query'

# ========================================
# versi input - jika short_code menggunakan input
# shortcode=CEqXCJ7FiJ1, end_cursor = QVFBODUwWl9XNU5NLU5vVXVON0p6QkpOWHRzYV9Tb09GSlNzMV9DYlJja0pCek5wV2xzSWVXbVJYU1dKOF9QS2hVWXFkbW1ZOGNOYlRKZncxcHFOdnhmSQ==

short_code = input('masukkan short code:')
end_cursor = ''
count = 0
counter_file = 1
jumlah_per_file = 50

# variabel pengextract csv
writer = csv.writer(open('hasil_extract/{} {}.csv'.format(short_code, counter_file),  'w', newline='', encoding='utf-8')) #extract dalam csv dengan nama sesuai dengan short_code, method 'w' = write
headers = ['User name', 'Full name', 'Profile pic']
writer.writerow(headers)

while 1:
    variables_a = {"shortcode": short_code, "include_reel": True, "first": 24, "after": end_cursor}
    # ======================================
    # variables_a = {"shortcode":"CEqXCJ7FiJ1","include_reel":True,"first":24} #Headers>General>>query string parameter>variables
    params = {
        'query_hash': 'd5d763b1e2acf209d62d22d184488e57',  # Headers>General>>query string parameter>query hash
        'variables': json.dumps(variables_a)  # mengambil data variables_a
    }
    # mengambil file json dari url dengan parameter tertentu diatas
    r = requests.get(url, params=params).json()

    try: users = r['data']['shortcode_media']['edge_liked_by']['edges']
    except:
        print('tunggu 20 detik')
        time.sleep(20) #diberi jeda 20 detik, untuk like dengan jumlah puluhan ribu. karena if not, dianggap spam
        continue
    # looping balik ke while disini dengan jeda 20 detik. 1-24, 25-49, dst

    # mencetak hasil ver users
    for u in users:
        if count % jumlah_per_file == 0 and count !=0:
            counter_file += 1
            writer = csv.writer(open('hasil_extract/{} {}.csv'.format(short_code, counter_file), 'w', newline='', encoding='utf-8'))
            headers = ['User name', 'Full name', 'Profile pic']
            writer.writerow(headers)
        username = u['node']['username']
        full_name = u['node']['full_name']
        profile_pic = u['node']['profile_pic_url']
        count += 1
        print(count, username, full_name, profile_pic)
        writer = csv.writer(open('hasil_extract/{} {}.csv'.format(short_code, counter_file), 'a', newline='', encoding='utf-8'))  # extract dalam csv dengan nama sesuai dengan short_code
        data = [username, full_name, profile_pic]
        writer.writerow(data)
    end_cursor = r['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']
    has_next_page = r['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']
    if has_next_page == False: break #jika tidak punya hal terakhir maka berhenti
    time.sleep(2)
