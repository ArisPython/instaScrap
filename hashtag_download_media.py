import requests

count = 0
end_cursor = ''
while True:
    #url1 mengakses jumlah postingan hashtag beserta short code, untuk detail username dan gambar ada di url2
    url1 = 'https://www.instagram.com/explore/tags/baksokillermenjangan/?__a=1&max_id={}'.format(end_cursor)#$max_id untuk pagination
    r1 = requests.get(url1).json()
    short_codes = r1['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    for i in short_codes:
        short_code = i['node']['shortcode']
        #url2 membuka masing2 postingan berdasarkan short code url1
        url2 = 'https://www.instagram.com/p/{}/?__a=1'.format(short_code)
        r2 = requests.get(url2).json()
        username = r2['graphql']['shortcode_media']['owner']['username']
        print(username)
        count += 1

        #donload image dan video
        file_name_image = '{} {}.jpg'.format(count, username)
        file_name_video = '{} {}.mp4'.format(count, username)
        path_image =  'media_download/{}'.format(file_name_image)
        path_video = 'media_download/{}'.format(file_name_video)

        is_video = r2['graphql']['shortcode_media']['is_video']
        if is_video == True:
            url_media_video = r2['graphql']['shortcode_media']['video_url']
            r_url_media_video = requests.get(url_media_video).content
            open(path_video, 'wb').write(r_url_media_video)
        if is_video == False:
            url_media_image = r2['graphql']['shortcode_media']['display_url']
            r_url_media_image = requests.get(url_media_image).content
            open(path_image, 'wb').write(r_url_media_image)

        print(count, short_code)
    end_cursor = r1['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
    has_next_page = r1['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
    if has_next_page == False: break  # jika tidak punya hal terakhir maka berhenti