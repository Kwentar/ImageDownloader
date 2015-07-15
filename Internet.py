import os
import shutil
from threading import Thread
import urllib
import requests


class Internet:
    @staticmethod
    def write_to_need_reload(file_name, image, need_reload_file):
        with open(need_reload_file, 'a+') as need_reload:
            need_reload.seek(0)
            lines = need_reload.readlines()
            founded = False
            for line in lines:
                if line.startswith(image):
                    print('File is here')
                    founded = True
                    break
            if not founded:
                need_reload.write(image + "," + file_name + '\n')

    @staticmethod
    def load_image_chunk(image, file_name, need_reload_file):
        r = requests.get(image, stream=True)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            print(r)

    @staticmethod
    def load_image2(image, file_name, need_reload_file):
        r = requests.get(image, stream=True)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            print(r)

    @staticmethod
    def load_image(image, file_name, need_reload_file):
        try:
            urllib.request.urlretrieve(image, file_name)
            print("".join(['downloaded ', image]))
        except urllib.error.ContentTooShortError as err_:
            print("".join(['ERROR ', err_.__str__()]))
            if need_reload_file is not None:
                Internet.write_to_need_reload(file_name, image, need_reload_file)
        except urllib.error.URLError as err_:
            print("".join(['ERROR ', err_.__str__()]))
            if need_reload_file is not None:
                Internet.write_to_need_reload(file_name, image, need_reload_file)

    @staticmethod
    def load_images(images, dir_, need_reload_file, delay=5, load_image_func=load_image_chunk):
        abs_need_reload_file = os.path.join(dir_, need_reload_file)
        if not os.path.exists(abs_need_reload_file):
            f = open(abs_need_reload_file, 'w')
            f.close()
        for image in images:
            f = os.path.join(dir_, image.split('/')[-1])
            t = Thread(target=Internet.load_image_chunk, args=(image, f, need_reload_file))
            t.start()
            t.join(delay)
            if t.isAlive():
                print('Bad, bad thread!')
                if need_reload_file is not None:
                    Internet.write_to_need_reload(f, image, need_reload_file)