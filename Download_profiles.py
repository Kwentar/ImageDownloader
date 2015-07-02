import os
from Internet import Internet
from vk import Vk


vk_dir = 'F:\\vk\\'
need_reload_file = 'F:\\vk\\need_reload.txt'
#downloaded_users_file = 'F:\\vk\\downloaded_users.txt'
users_info_file = 'F:\\vk\\downloaded_users_info.txt'


def check_in_file(uid, lst):
    founded = False
    for el in lst:
        if el.startswith(uid):
            founded = True
            break
    return founded


def get_profile_photos(id_, start_dir, downloaded_users_file):
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


def write_users_to_file(need_to_write_users, users_info_file_friends):
    with open(users_info_file_friends, 'a+', encoding='utf-8') as users_info:
        for user in need_to_write_users:
            users_info.write(user.__str__() + '\n')


def get_lists_from_file(file_name):
    with open(file_name, 'a+') as downloaded_users:
        downloaded_users.seek(0)
        return downloaded_users.readlines()


def write_users_in_file(file_name, users, open_mode='a+'):
    with open(file_name, open_mode,  encoding='utf-8') as users_info_fr:
        for user in users:
            users_info_fr.write(user.__str__() + '\n')


def download_users(age_from, age_to, city_id, downloaded_users_file):
    months = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
              7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    downloaded_users_list = get_lists_from_file(downloaded_users_file)
    users_info_list = get_lists_from_file(users_info_file)
    for age in range(age_from, age_to+1):
        for month in months.keys():
            for day in range(1, months[month]+1):
                print('''processed: day = {}, month = {}, age = {}'''.format(day, month, age))
                while True:
                    users = Vk.get_uids(age, month, day, city_id)
                    if users:
                        break
                    Vk.get_token()
                need_to_write_users = list()
                for user in users:
                    if not check_in_file(user.uid, downloaded_users_list):
                        dir_of_photos = os.path.join(vk_dir, age.__str__())
                        get_profile_photos(user.uid, dir_of_photos, downloaded_users_file)
                    if check_in_file(user.uid, users_info_list):
                        print('We have this user in info too! ' + user.name + ' ' + user.last_name)
                    else:
                        print('added info ' + user.name + ' ' + user.last_name)
                        need_to_write_users.append(user)
                write_users_to_file(need_to_write_users, users_info_file)


def downloaded_friends(start_id, dir_, deep=1):
    downloaded_users_file_friends = os.path.join(dir_, 'downloaded_users.txt')
    users_info_file_friends = os.path.join(dir_, 'user_info.txt')
    downloaded_users_list = get_lists_from_file(downloaded_users_file_friends)
    users_info_list = get_lists_from_file(users_info_file_friends)
    while True:
        users = Vk.get_friends(start_id)
        if users:
            break
        Vk.get_token()
    if not check_in_file(start_id, downloaded_users_list):
        get_profile_photos(start_id, dir_, downloaded_users_file_friends)
    need_to_write_users = list()
    write_users_in_file(os.path.join(dir_, start_id + '\\friends.txt'), users, open_mode='w')
    count = 0
    for user in users:
        count += 1
        if not check_in_file(user.uid, downloaded_users_list):
            get_profile_photos(user.uid, dir_,  downloaded_users_file_friends)
        if check_in_file(user.uid, users_info_list):
            print('We have this user in info too! ' + user.name + ' ' + user.last_name)
        else:
            print('added info ' + user.name + ' ' + user.last_name + ' (friend of ' + start_id.__str__() + '), '
                  + count.__str__() + '\\' + len(users).__str__())
            need_to_write_users.append(user)
        while True:
            user_fr = Vk.get_friends(user.uid)
            if user_fr:
                break
            Vk.get_token()
        write_users_in_file(os.path.join(dir_, user.uid + '\\friends.txt'), user_fr, open_mode='w')
        if deep:
            downloaded_friends(user.uid, dir_, deep-1)
    write_users_to_file(need_to_write_users, users_info_file_friends)


downloaded_friends('11152217', 'F:\\vk\\friends\\')
# download_users(23, 23, 10, 'F:\\vk\\downloaded_users.txt')


