import requests, json

#data request URL pada tab Headers>General
url = 'https://www.instagram.com/graphql/query'

#versi input - jika short_code menggunakan input
#short_code = input('masukkan short code:')
#variables_a = {"shortcode":short_code,"include_reel":True,"first":24}


variables_a = {"shortcode":"CEqXCJ7FiJ1","include_reel":True,"first":24} #Headers>General>>query string parameter>variables
params = {
    'query_hash': 'd5d763b1e2acf209d62d22d184488e57', #Headers>General>>query string parameter>query hash
    'variables': json.dumps(variables_a) #mengambil data variables_a
}
# mengambil file json dari url dengan parameter tertentu diatas
r = requests.get(url, params=params).json()

users = r['data']['shortcode_media']['edge_liked_by']['edges']

count = 0
for u in users:
    username = u['node']['username']
    full_name = u['node']['full_name']
    profile_pic = u['node']['profile_pic_url']
    print(username, full_name, profile_pic)
    count +=1
    print(count)
