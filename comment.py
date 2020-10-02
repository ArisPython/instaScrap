import requests, json, time, csv

#data request URL pada tab Headers>General
url = 'https://www.instagram.com/graphql/query'

end_cursor = ''
short_code = "CFxNnqRjqi0"
count = 0
counter_file = 1
jumlah_per_file = 100

# variabel pengextract csv
writer = csv.writer(open('hasil_comment/{} {}.csv'.format(short_code, counter_file),  'w', newline='', encoding='utf-8')) #extract dalam csv dengan nama sesuai dengan short_code, method 'w' = write
headers = ['User name', 'Text']
writer.writerow(headers)
#versi input - jika short_code menggunakan input
#short_code = input('masukkan short code:')
#variables_a = {"shortcode":short_code,"include_reel":True,"first":24}

while 1:
    variables_a = {"shortcode": short_code,"include_reel":True,"first":50, "after": end_cursor} #Headers>General>>query string parameter>variables
    params = {
        'query_hash': 'bc3296d1ce80a24b1b6e40b1e72903f5', #Headers>General>>query string parameter>query hash
        'variables': json.dumps(variables_a) #mengambil data variables_a
    }
    # mengambil file json dari url dengan parameter tertentu diatas
    r = requests.get(url, params=params).json()

    #print(r)
    try:
        users = r['data']['shortcode_media']['edge_media_to_parent_comment']['edges']
    except:
        print('tunggu 20 detik')
        time.sleep(20)  # diberi jeda 20 detik, untuk like dengan jumlah puluhan ribu. karena if not, dianggap spam
        continue
    #print(users)
    count = 0
    for user in users:
        if count % jumlah_per_file == 0 and count !=0:
            counter_file += 1
            writer = csv.writer(open('hasil_comment/{} {}.csv'.format(short_code, counter_file), 'w', newline='', encoding='utf-8'))
            headers = ['User name', 'Text']
            writer.writerow(headers)

        username = user['node']['owner']['username']
        text = user['node']['text']

        count +=1
        print(text)
        writer = csv.writer(open('hasil_comment/{} {}.csv'.format(short_code, counter_file), 'a', newline='',
                                 encoding='utf-8'))  # extract dalam csv dengan nama sesuai dengan short_code
        data = [username, text]
        writer.writerow(data)

    end_cursor = r['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']
    has_next_page = r['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']
    if has_next_page == False: break
    time.sleep(2)
#
# count = 0
# for u in users:
#     username = u['node']['username']
#     full_name = u['node']['full_name']
#     profile_pic = u['node']['profile_pic_url']
#     print(username, full_name, profile_pic)
#     count +=1
#     print(count)
