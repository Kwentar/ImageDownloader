from Internet import Internet
import __setup_photo__ as setup
import flickrapi


def download_photos_by_text(search_text, dir_, failed_image_urls_file='failed_image_urls.txt'):
    flickr = flickrapi.FlickrAPI(api_key=setup.flickr_key, secret=setup.flickr_secret, format='parsed-json')
    count_pages = 2
    curr_page = 1
    while curr_page < count_pages:
        photos = flickr.photos.search(text=search_text,
                                      per_page='100',
                                      content_type='1',
                                      media='photos',
                                      page=curr_page,
                                      privacy_filter='1')
        if photos['stat'] == 'ok':
            count_pages = photos['photos']['pages']
            photos_list = photos['photos']['photo']
            for item in photos_list:
                urls = flickr.do_flickr_call('flickr.photos.getSizes', photo_id=item['id'])
                if urls['stat'] == 'ok':
                    url = ''
                    for s in urls['sizes']['size']:
                        if s['label'] == 'Original':
                            url = s['source']
                            Internet.load_images([url], dir_, failed_image_urls_file, delay=60)
                else:
                    print('Error: failed to get sizes of image ' + urls['stat'])
            curr_page += 1
        else:
            print('Error: failed to get images ' + photos['stat'])


download_photos_by_text('nature', '/home/kwent/Downloads/flickr/nature')
