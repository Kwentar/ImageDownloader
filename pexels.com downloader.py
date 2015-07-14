import os
import random
import time
import Internet
import __setup_photo__ as setup
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, HTTPError


def get_photo_from_pexels(photo_id):
    url = 'http://www.pexels.com/photo/' + photo_id.__str__()
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


pexels_dir = "D:\\Graphics\\pexels"
max_count_photos = 7455
curr_id = 0
if os.path.exists(os.path.join(pexels_dir, 'ids.txt')):
    with open(os.path.join(pexels_dir, 'ids.txt')) as ids_file:
        lines = ids_file.readlines()
        ids = map(int, [el[:-1] for el in lines if len(el[:-1])])
        curr_id = max(ids)
while curr_id < max_count_photos:
    image_url = get_photo_from_pexels(curr_id)
    if image_url == 'None':
        print('Error while retrieving photos')
        time.sleep(1)
    else:
        print('Download photo...')
        Internet.Internet.load_images([image_url], pexels_dir, None)
    with open(os.path.join(pexels_dir, 'ids.txt'), 'a+') as ids_file:
        ids_file.write(curr_id.__str__() + os.linesep)
    print('processing {} photo'.format(curr_id))
    curr_id += 1





