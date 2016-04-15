from vk import Vk, VkUser
import os
import Download_profiles
import Internet


def get_profile_photos(id_, start_dir, downloaded_users_file, need_reload_file):
    dir_of_photos = os.path.join(start_dir, id_.__str__())

    images = Vk.get_profile_photos(id_.__str__())
    if 9 < len(images) < 1000:
        if not os.path.exists(dir_of_photos):
            os.makedirs(dir_of_photos)
        Internet.Internet.load_images(images.keys(), dir_of_photos, need_reload_file)
        with open(os.path.join(dir_of_photos, id_.__str__() + '.txt'), 'w+', encoding='utf-8') as info:
            for image, likes in images.items():
                f = image.split('/')[-1]
                info.write(f + ',' + likes.__str__() + '\n')
    with open(downloaded_users_file, 'a+') as downloaded_users:
        downloaded_users.seek(0)
        lines = downloaded_users.readlines()
        if not Download_profiles.check_in_file(id_.__str__(), lines):
            downloaded_users.write(id_.__str__() + '\n')
    print('LOADED id = ' + id_.__str__())

max_id = 360553663
vk_dir = "D:\\Graphics\\vk"
file_downloaded = "downloaded_users.txt"
file_need_reload = "need_reload.txt"
id_ = 1

ready_users = Download_profiles.get_lists_from_file(os.path.join(vk_dir, file_downloaded))
ready_ids = list(map(int, map(str.strip, ready_users)))
id_ = 1 if not ready_ids else max(ready_ids) + 1

while id_ < max_id:
    get_profile_photos(id_, vk_dir, os.path.join(vk_dir, file_downloaded), os.path.join(vk_dir, file_need_reload))
    id_ += 1

