import os
from instagram.client import InstagramAPI
from Internet import Internet
import __setup_photo__ as setup


def get_user_id_by_name(instagram_api, user_name):
    response = instagram_api.user_search(user_name)
    if response:
        try:
            return response[0].id
        except:
            return None
    else:
        return None


def download_user_photos(instagram_api, user_name, dir_):
    """
    download all photos of instagram user to dir_/user_name folder
    :param instagram_api: instagram api by python-instagram package
    :param user_name: instagram user name
    :param dir_: dir for photos
    :return: None
    """
    user_id = get_user_id_by_name(instagram_api, user_name)
    if user_id is None:
        print("Incorrect user id")
        return
    image_list = list()
    max_id_str = 'max_id='
    (response, next_) = instagram_api.user_recent_media(user_id=user_id, count=100)
    while True:
        image_list += [el.images['standard_resolution'].url for el in response]
        print('current count is {}'.format(len(image_list)))
        if next_ is not None and max_id_str in next_:
            max_index = next_.find(max_id_str) + len(max_id_str)
            max_id = next_[max_index:]
        else:
            break
        (response, next_) = instagram_api.user_recent_media(user_id=user_id, count=100, max_id=max_id)
    print("count of images for downloading: {}".format(len(image_list)))
    dir_ = os.path.join(dir_, user_name)
    if not os.path.exists(dir_):
        os.mkdir(dir_)
    Internet.load_images(image_list, dir_, failed_image_urls_file="need_reload.txt", delay=300)

access_token = setup.inst_access_token
api = InstagramAPI(access_token=setup.inst_access_token)
download_user_photos(api, 'tyulkina_j', '/home/instagram')
