import os
from Internet import Internet
from vk import Vk


vk_dir = 'F:\\vk\\'
need_reload_file = 'F:\\vk\\need_reload.txt'
downloaded_users_file = 'F:\\vk\\downloaded_users.txt'
users_info_file = 'F:\\vk\\downloaded_users_info.txt'


def check_in_file(uid, lst):
    founded = False
    for el in lst:
        if el.startswith(uid):
            founded = True
            break
    return founded


def get_profile_photos(id_, start_dir, age):
    dir_of_photos = os.path.join(start_dir, age.__str__())
    dir_of_photos = os.path.join(dir_of_photos, id_)
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
    with open(users_info_file, 'r',  encoding='utf-8') as users_info:
        users_info_lines = users_info.readlines()
    for age in range(age_from, age_to+1):
        for month in months.keys():
            for day in range(1, months[month]+1):
                print('''processed: day = {}, month = {}, age = {}'''.format(day, month, age))
                users = Vk.get_uids(age, month, day, city_id)
                need_to_write_users = list()
                for user in users:
                    if not check_in_file(user.uid, downloaded_users_list):
                        get_profile_photos(user.uid, vk_dir, age)
                    if check_in_file(user.uid, users_info_lines):
                        print('We have this user in info too! ' + user.name + ' ' + user.last_name)
                    else:
                        print('added info ' + user.name + ' ' + user.last_name)
                        need_to_write_users.append(user)
                with open(users_info_file, 'a+',  encoding='utf-8') as users_info:
                    for user in need_to_write_users:
                        users_info.write(user.__str__() + '\n')


download_users(19, 20, 10)


