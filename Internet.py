import os
from threading import Thread
import urllib


class Internet:
    @staticmethod
    def load_image(image, file_name, need_reload_file):
        try:
            urllib.request.urlretrieve(image, file_name)
            print("".join(['downloaded ', image]))
        except urllib.error.ContentTooShortError as err_:
            print("".join(['ERROR ', err_.__str__()]))
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
    def load_images(images, dir_, need_reload_file):
        for image in images:
            f = os.path.join(dir_, image.split('/')[-1])
            t = Thread(target=Internet.load_image, args=(image, f, need_reload_file))
            t.start()
            t.join(5)
            if t.isAlive():
                print('Bad, bad thread!')