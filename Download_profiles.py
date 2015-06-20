import os
from Internet import Internet
from vk import Vk


vk_dir = 'D:\\Graphics\\vk\\'
need_reload_file = 'D:\\Graphics\\vk\\need_reload.txt'
downloaded_users_file = 'D:\\Graphics\\vk\\downloaded_users.txt'

def check_in_file(uid, lst):
    founded = False
    for el in lst:
        if el.startswith(uid):
            founded = True
            break
    return founded


def get_profile_photos(id_, start_dir):
    dir_of_photos = os.path.join(start_dir, id_)
    if not os.path.exists(dir_of_photos):
        os.makedirs(dir_of_photos)
    images = Vk.get_profile_photos(id_)
    Internet.load_images(images, dir_of_photos, need_reload_file)
    with open(downloaded_users_file, 'a+') as downloaded_users:
        downloaded_users.seek(0)
        lines = downloaded_users.readlines()
        if not check_in_file(id_, lines):
            downloaded_users.write(id_ + '\n')


def download_users(age_from, age_to, city_id):
    months = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
              7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    with open(downloaded_users_file, 'r') as downloaded_users:
        downloaded_users_list = downloaded_users.readlines()
    for age in range(age_from, age_to+1):
        for month in months.keys():
            for day in range(1, months[month]+1):
                print('''processed: day = {}, month = {}, age = {}'''.format(day, month, age))
                uids = Vk.get_uids(age, month, day, city_id)
                for uid in uids:
                    if check_in_file(uid, downloaded_users_list):
                        print('We have this user!')
                    else:
                        get_profile_photos(uid, vk_dir)

download_users(19, 24, 10)


