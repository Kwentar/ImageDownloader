import os
import shutil
from threading import Thread
import urllib
import requests


class Internet:
    @staticmethod
    def write_to_failed_image_urls_file(file_name, image_url, failed_image_urls_file):
        """
        Check image in file and write it if need
        :param file_name: image file name
        :param image_url: image URL
        :param failed_image_urls_file: name of file with fails
        :return: None
        """
        with open(failed_image_urls_file, 'a+') as need_reload:
            need_reload.seek(0)
            lines = need_reload.readlines()
            founded = False
            for line in lines:
                if line.startswith(image_url):
                    print('File is here')
                    founded = True
                    break
            if not founded:
                need_reload.write(image_url + "," + file_name + '\n')

    @staticmethod
    def write_response_to_file(response, file_name):
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=2048):
                f.write(chunk)

    @staticmethod
    def load_image_chunk(image_url, file_name, dir_):
        """
        Loading image by URL
        :param image_url: URL of image
        :param file_name: destination file name
        :param dir_: destination directory
        :return: None
        """
        r = requests.get(image_url, stream=True)
        if r.status_code == requests.codes.ok:
            try:
                Internet.write_response_to_file(r, file_name)
            except OSError as err_:
                print(err_.__str__(), 'try redownload...')
                file_name = os.path.join(dir_, file_name.split('=')[-1] + '.jpg')
                Internet.write_response_to_file(r, file_name)
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
                Internet.write_to_failed_image_urls_file(file_name, image, need_reload_file)
        except urllib.error.URLError as err_:
            print("".join(['ERROR ', err_.__str__()]))
            if need_reload_file is not None:
                Internet.write_to_failed_image_urls_file(file_name, image, need_reload_file)

    @staticmethod
    def load_images(image_url_list, dir_, failed_image_urls_file, delay=5):
        """
        loading list of images
        :param image_url_list: list of image urls
        :param dir_: destination dir
        :param failed_image_urls_file: name of file with unsuccessful urls
        :param delay: delay for thread
        :return:None
        """
        abs_failed_image_urls_file = os.path.join(dir_, failed_image_urls_file)
        if not os.path.exists(abs_failed_image_urls_file):
            with open(abs_failed_image_urls_file, 'w') as _:
                pass
        for image in image_url_list:
            f = os.path.join(dir_, image.split('/')[-1])
            t = Thread(target=Internet.load_image_chunk, args=(image, f, dir_))
            t.start()
            t.join(delay)
            if t.isAlive():
                print('Bad, bad thread!')
                if abs_failed_image_urls_file is not None:
                    Internet.write_to_failed_image_urls_file(f, image, abs_failed_image_urls_file)
