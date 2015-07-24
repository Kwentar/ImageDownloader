import os
from instagram.client import InstagramAPI
from Internet import Internet
import __setup_photo__ as setup


def get_user_id_by_name(api, user_name):
    response = api.user_search(user_name)
    if response:
        try:
            return response[0].id
        except:
            return None
    else:
        return None


def download_user_photos(api, user_name, dir_):
    """
    dwonload all photos of instagram user on dir_/user_name folder
    :param user_name: instagram user name
    :param dir_: dir for photos
    :return: None
    """
    user_id = get_user_id_by_name(api, user_name)
    if user_id is None:
        print("Incorrect user id")
        return
    next_ = '-1'
    image_list = list()
    max_id = None
    while next_:
        if max_id is None:
            response, next_ = api.user_recent_media(user_id=user_id, count=100)
        else:
            response, next_ = api.user_recent_media(user_id=user_id, count=100, max_id=max_id)
        for el in response:
            image_list.append(el.images['standard_resolution'].url)
        print('current count is {}'.format(len(image_list)))
        if next_:
            max_index = next_.find('max_id=')
            if max_index > 0:
                max_index += len('max_id=')
                max_id = next_[max_index:]
            else:
                next_ = None
    print("count of images for downloading: {}".format(len(image_list)))
    dir_ = os.path.join(dir_, user_name)
    if not os.path.exists(dir_):
        os.mkdir(dir_)
    Internet.load_images(image_list, dir_, failed_image_urls_file="need_reload.txt", delay=300)

access_token = setup.inst_access_token
client_secret = setup.inst_client_secret
api = InstagramAPI(access_token=setup.inst_access_token)
download_user_photos(api, 'natgeoru', '/home/instagram')