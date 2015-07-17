import os
import ImageProcessor
from Internet import Internet
from SiteDownloader import PexelsDownloader, AlphacodersComDownloader, MotaRuDownloader
from vk import Vk, VkUser
from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    vk_dir = '/media/kwent/A278648A78645F53/vk'
    need_reload_file = '/media/kwent/A278648A78645F53/vk/need_reload.txt'
    users_info_file = '/media/kwent/A278648A78645F53/vk/downloaded_users_info.txt'
    friends_dir = '/media/kwent/A278648A78645F53/vk/friends'

elif _platform == "win32":
    vk_dir = 'F:\\vk\\'
    need_reload_file = 'F:\\vk\\need_reload.txt'
    #downloaded_users_file = 'F:\\vk\\downloaded_users.txt'
    users_info_file = 'F:\\vk\\downloaded_users_info.txt'
    friends_dir = 'F:\\vk\\friends\\'


def check_in_file(uid, lst):
    founded = False
    for el in lst:
        if el.startswith(uid):
            founded = True
            break
    return founded


def get_user_info_from_list(uid, lst):
    user = None
    for el in lst:
        if el.startswith(uid):
            try:
                uid, name, last_name, day_b, month_b, sex, year_b, city_id = el[:-1].split(';')
                user = VkUser(uid, name, last_name, int(day_b), int(month_b), sex, city_id, year_b=int(year_b))
                break
            except:
                print('except ' + el)

    return user


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
    try:
        with open(file_name, 'a+', encoding='utf-8') as downloaded_users:
            downloaded_users.seek(0)
            return downloaded_users.readlines()
    except FileNotFoundError as err_:
        print(err_.strerror)
        return list()


def get_users_from_file(file_name):
    users = list()
    lst = get_lists_from_file(file_name)
    for el in lst:
        try:
            uid, name, last_name, day_b, month_b, sex, year_b, city_id = el[:-1].split(';')
            user = VkUser(uid, name, last_name, int(day_b), int(month_b), sex, city_id, year_b=int(year_b))
            users.append(user)
        except ValueError as err:
            print('except ' + err.__str__() + ' ' + el)
    return users


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


def downloaded_friends(user_ids, dir_, deep=2):
    downloaded_users_file_friends = os.path.join(dir_, 'downloaded_users.txt')
    users_info_file_friends = os.path.join(dir_, 'user_info.txt')
    downloaded_users_list = get_lists_from_file(downloaded_users_file_friends)
    users_info_list = get_lists_from_file(users_info_file_friends)
    count = 0
    next_iter_uids = set()
    for uid in user_ids:
        count += 1
        if not check_in_file(uid, downloaded_users_list):
            get_profile_photos(uid, dir_, downloaded_users_file_friends)
        user = get_user_info_from_list(uid, users_info_list)
        if user is not None:
            print('We have this user in info too! ' + user.name + ' ' + user.last_name + ' (id ' +
                  user.uid.__str__() + '), ' + count.__str__() + '\\' + len(user_ids).__str__())
            user_friends_file = os.path.join(dir_, uid)
            user_friends_file = os.path.join(user_friends_file, 'friends.txt')
            users = get_users_from_file(user_friends_file)
        else:
            user = Vk.get_user_info(uid)
            if user is not None:
                print('added info ' + user.name + ' ' + user.last_name + ' (id ' + user.uid.__str__() + '), '
                      + count.__str__() + '\\' + len(user_ids).__str__())
                write_users_to_file([user], users_info_file_friends)
                for i in range(3):
                    users = Vk.get_friends(uid)
                    if users:
                        break
                    Vk.get_token()
                path_to_write = os.path.join(dir_, uid)
                path_to_write = os.path.join(path_to_write, 'friends.txt')
                write_users_in_file(path_to_write, users, open_mode='w')
        if deep > 0:
            next_iter_uids = next_iter_uids | set([user.uid for user in users])

    if next_iter_uids:
        downloaded_friends(next_iter_uids, dir_, deep-1)



# downloaded_friends(['11152217'], friends_dir, deep=3)
# print('I really did it oO')

# ImageProcessor.get_faces('E:\\vk\\friends')
# print(ImageProcessor.get_count_faces('E:\\vk\\'))
s = PexelsDownloader()
print(s.download_all_images(dir_='E:\\Graphics\\negatives\\pexels', ids_file='ids.txt'))


# download_users(23, 23, 10, 'F:\\vk\\downloaded_users.txt')