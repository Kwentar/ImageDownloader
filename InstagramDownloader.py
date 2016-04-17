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


def download_photos_by_tag(instagram_api, tag, dir_, max_photos=0):
    """
    Download all photos with this tag
    :param instagram_api: instagram api by python-instagram package
    :param tag: tag for search
    :param dir_: dir for photos
    :return: None
    """
    (response, next_) = instagram_api.tag_recent_media(tag_name=tag, count=100)
    image_list = list()
    max_id_str = 'max_tag_id='
    while True:
        image_list += [el.images['standard_resolution'].url for el in response]
        print('current count is {}'.format(len(image_list)))
        if max_photos and len(image_list) >= max_photos:
            break
        if next_ is not None and max_id_str in next_:
            max_index = next_.find(max_id_str) + len(max_id_str)
            max_id = next_[max_index:]
        else:
            break
        (response, next_) = instagram_api.tag_recent_media(tag_name=tag, count=100, max_tag_id=max_id)
    print("count of images for downloading: {}".format(len(image_list)))
    dir_ = os.path.join(dir_, tag)
    if not os.path.exists(dir_):
        os.mkdir(dir_)
    Internet.load_images(image_list, dir_, failed_image_urls_file="need_reload.txt", delay=300)


def download_user_photos(instagram_api, user_name, dir_, tag=''):
    """
    download all photos of instagram user to dir_/user_name folder
    :param instagram_api: instagram api by python-instagram package
    :param user_name: instagram user name
    :param dir_: dir for photos
    :param tag: download user photos with this tag, if empty - all photos
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
        for el in response:
            if tag:
                for t in el.tags:
                    if tag == t.name:
                        image_list.append(el.images['standard_resolution'].url)
            else:
                image_list.append(el.images['standard_resolution'].url)
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
download_user_photos(api, 'staceyalexx', 'D:\\Graphics\\Download\\instagram', tag='')
# download_photos_by_tag(api, 'nopeople', 'D:\\Graphics\\Download\\instagram')
# (response, next_) = instagram_api.tag_recent_media(tag_name='tag', count=100, max_tag_id=max_id)
