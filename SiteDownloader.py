import os
import random
import time
from urllib import request
import Internet
import __setup_photo__ as setup
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, HTTPError
from abc import ABCMeta, abstractmethod
import requests


class SiteDownloader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_image_url(self, id_, base_url):
        """Here must be parser of site url witch return link on image"""
    @abstractmethod
    def download_all_images(self, dir_, ids_file, base_url,  need_reload_file):
        """method which must download all images from site"""


class DownloaderAllImages:
    @staticmethod
    def download_all_images(dir_, ids_file_name, base_url, need_reload_file, site_downloader):
        curr_id = 0
        count404 = 0
        abs_ids_file = os.path.join(dir_, ids_file_name)
        if os.path.exists(abs_ids_file):
            with open(abs_ids_file) as ids_file:
                lines = ids_file.readlines()
                ids = map(int, [el[:-1] for el in lines if len(el[:-1])])
                curr_id = max(ids)
        while True:
            image_url = site_downloader.get_image_url(curr_id, base_url)
            print(image_url)
            if image_url.__str__() == 'None':
                print('Error while retrieving photos')
                count404 += 1
                time.sleep(1)
            else:
                print('Download photo...')
                count404 = 0
                Internet.Internet.load_images([image_url], dir_, os.path.join(dir_, need_reload_file), delay=300)
            with open(abs_ids_file, 'a+') as ids_file:
                ids_file.write(curr_id.__str__() + '\n')
            print('processing {} photo'.format(curr_id))
            if count404 >= 1000:
                print('more or equal 1000 404 errors, curr id is ' + curr_id.__str__())
                break
            curr_id += 1


class PexelsDownloader(SiteDownloader):

    def get_image_url(self, id_, base_url='http://www.pexels.com/photo/'):
        url = base_url + id_.__str__()
        user_agent = random.choice(setup.user_agents)
        try:
            req = Request(url, headers={'User-Agent': user_agent})
            print('Try to get image from ' + url)
            soup = BeautifulSoup(urlopen(req).read())
        except HTTPError as e:
            print("Error in opening " + e.code.__str__())
            return 'None'
        else:
            for link in soup.find_all('a'):
                if type(link.get('class')) == list:
                    if 'js-download' in link.get('class'):
                        return link.get('href')

    def download_all_images(self,
                            dir_,
                            ids_file='pexels_ids.txt',
                            base_url='http://www.pexels.com/photo/',
                            need_reload_file='need_reload.txt'):
        DownloaderAllImages.download_all_images(dir_, ids_file, base_url, need_reload_file, self)


class SplashbaseDownloader(SiteDownloader):
    def get_image_url(self, id_, base_url='http://www.splashbase.co/images/'):
        url = base_url + id_.__str__()
        user_agent = random.choice(setup.user_agents)
        try:
            req = Request(url, headers={'User-Agent': user_agent})
            print('Try to get image from ' + url)
            soup = BeautifulSoup(urlopen(req).read())
        except HTTPError as e:
            print("Error in opening " + e.code.__str__())
            return 'None'
        else:
            for link in soup.find_all('img'):
                return link.get('src')

    def download_all_images(self,
                            dir_,
                            ids_file='splashbase_ids.txt',
                            base_url='http://www.splashbase.co/images/',
                            need_reload_file='need_reload.txt'):
        DownloaderAllImages.download_all_images(dir_, ids_file, base_url, need_reload_file, self)


class MotaRuDownloader(SiteDownloader):
    def get_image_url(self, id_, base_url='http://www.mota.ru/wallpapers/source/id/'):
        url = base_url + id_.__str__()
        user_agent = random.choice(setup.user_agents)
        try:
            req = Request(url, headers={'User-Agent': user_agent})
            print('Try to get image from ' + url)
            soup = BeautifulSoup(urlopen(req).read())
        except HTTPError as e:
            print("Error in opening " + e.code.__str__())
            return 'None'
        else:
            for link in soup.find_all('img'):
                if 'wallpaper' in link.get('class'):
                    return link.get('src')

    def download_all_images(self,
                            dir_,
                            ids_file='mota_ids.txt',
                            base_url='http://www.mota.ru/wallpapers/source/id/',
                            need_reload_file='need_reload.txt'):
        DownloaderAllImages.download_all_images(dir_, ids_file, base_url, need_reload_file, self)


class AlphacodersComDownloader(SiteDownloader):
    def get_image_url(self, id_, base_url='http://art.alphacoders.com/arts/view/'):
        url = base_url + id_.__str__()
        user_agent = random.choice(setup.user_agents)
        try:
            req = Request(url, headers={'User-Agent': user_agent})
            print('Try to get image from ' + url)
            soup = BeautifulSoup(urlopen(req).read())
            redirect = getattr(req, 'redirect_dict', '')
            if redirect:
                print("Error in opening: redirect")
                return 'None'
        except HTTPError as e:
            print("Error in opening " + e.code.__str__())
            return 'None'
        else:
            links = soup.find_all('img')
            for link in links:
                if 'main_wallpaper' in link.get('id'):
                    return link.get('src')

    def download_all_images(self,
                            dir_,
                            ids_file='alphacoders_ids.txt',
                            base_url='http://art.alphacoders.com/arts/view/',
                            need_reload_file='need_reload.txt'):
        DownloaderAllImages.download_all_images(dir_, ids_file, base_url, need_reload_file, self)


class FreephotosbankComDownloader(SiteDownloader):
    def get_image_url(self, id_, base_url='http://www.freephotosbank.com/download.php?type=image&pic='):
        url = base_url + id_.__str__()
        user_agent = random.choice(setup.user_agents)
        try:
            req = requests.get(url, headers={'User-Agent': user_agent}, stream=True)
            if req.history:
                print("Error in opening: redirect")
                return 'None'
        except HTTPError as e:
            print("Error in opening " + e.code.__str__())
            return 'None'
        else:
            return url

    def download_all_images(self,
                            dir_,
                            ids_file='freephotosbank_ids.txt',
                            base_url='http://www.freephotosbank.com/download.php?type=image&pic=',
                            need_reload_file='need_reload.txt'):
        DownloaderAllImages.download_all_images(dir_, ids_file, base_url, need_reload_file, self)

#TODO: http://morguefile.com/archive/display/10002