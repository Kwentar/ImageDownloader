from Internet import Internet
import __setup_photo__ as setup
import flickrapi


def download_photos_by_text(search_text, dir_, failed_image_urls_file='failed_image_urls.txt'):
    """
    Download all photo from flickr by text request search_text (for example: 'nature')
    :param search_text: text request for flickr
    :param dir_: dir for downloaded photos
    :param failed_image_urls_file: text file with downloading which failed
    :return: None
    """

    flickr = flickrapi.FlickrAPI(api_key=setup.flickr_key, secret=setup.flickr_secret, format='parsed-json')
    count_pages = 2
    curr_page = 1
    count_urls = 0
    while curr_page < count_pages:
        try:
            photos = flickr.photos.search(text=search_text,
                                          per_page='10',
                                          content_type='1',
                                          media='photos',
                                          page=curr_page,
                                          privacy_filter='1')
            if photos['stat'] == 'ok':
                count_pages = photos['photos']['pages']
                photos_list = photos['photos']['photo']
                url_list = list()
                for item in photos_list:
                    urls = flickr.do_flickr_call('flickr.photos.getSizes', photo_id=item['id'])
                    if urls['stat'] == 'ok':
                        url_list.append(urls['sizes']['size'][-1]['source'])
                    else:
                        print('Error: failed to get sizes of image ' + urls['stat'])
                curr_page += 1
                count_urls += len(url_list)
                print("processing {}-{} photos".format(count_urls-len(url_list), count_urls))
                Internet.load_images(url_list, dir_, failed_image_urls_file, delay=60)
            else:
                print('Error: failed to get images ' + photos['stat'])
        except TypeError as _err:
            print("error: ", _err)


download_photos_by_text('empty city', '/home/kwent/Downloads/flickr/emptycity')
