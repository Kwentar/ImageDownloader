import json
from urllib.parse import urlencode
from urllib.request import urlopen
import time
from Profiler import Profiler
import __setup_photo__ as setup


class VkError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Vk:
    tokens = setup.tokens
    curr_token = ''
    p = Profiler()

    @staticmethod
    def check_time():
        if Vk.p.get_time() < 0.5:
            time.sleep(0.5)
        Vk.p.start()

    @staticmethod
    def set_token(token):
        Vk.tokens.clear()
        Vk.tokens.append(token)

    @staticmethod
    def get_token():
        for el in Vk.tokens:
            test_url = 'https://api.vk.com/method/getProfiles?uid=66748&access_token=' + el
            Vk.check_time()
            response = urlopen(test_url).read()
            result = json.loads(response.decode('utf-8'))
            if 'response' in result.keys():
                print('now I use the ' + el + ' token')
                return el
        raise VkError('all tokens are invalid: ' + result['error']['error_msg'].__str__())

    @staticmethod
    def call_api(method, params):
        if not Vk.curr_token:
            Vk.curr_token = Vk.get_token()
        if isinstance(params, list):
            params_list = params[:]
        elif isinstance(params, dict):
            params_list = params.items()
        else:
            params_list = [params]

        params_list += [('access_token', Vk.curr_token)]
        url = 'https://api.vk.com/method/%s?%s' % (method, urlencode(params_list))

        response = urlopen(url).read()
        result = json.loads(response.decode('utf-8'))
        try:
            if 'response' in result.keys():
                return result['response']
            else:
                raise VkError('no response on answer: ' + result['error']['error_msg'].__str__())
        except VkError as err:
            print(err.value)
            Vk.curr_token = Vk.get_token()
            Vk.call_api(method, params)
            return list()

    @staticmethod
    def get_user_info(id_, fields='sex'):
        pass

    @staticmethod
    def get_uids(age, month, day, city_id):
        search_q = list()
        search_q.append(('offset', '0'))
        search_q.append(('count', '1000'))
        search_q.append(('city', city_id))
        search_q.append(('age_from', age))
        search_q.append(('age_to', age))
        search_q.append(('has_photo', '1'))
        search_q.append(('birth_day', day))
        search_q.append(('birth_month', month))
        r = Vk.call_api('users.search', search_q)
        count = 0
        uids = list()
        for el in r:
            if count and 'uid' in el.keys():
                uid = el['uid'].__str__()
                uids.append(uid)
            else:
                count = el
        if count > 1000:
            Vk.warning('''Count more than 1000, count = {}, age = {},
                        month = {}, day = {}'''.format(count, age, month, day))
        return uids

    @staticmethod
    def get_profile_photos(id_):
        q = list()
        q.append(('owner_id', id_))
        q.append(('album_id', 'profile'))
        q.append(('rev', '1'))
        q.append(('extended', '1'))
        q.append(('photos_size', '1'))
        r = Vk.call_api('photos.get', q,)
        images = list()
        for i in r:
            url_of_image = ''
            if 'src_xxxbig' in i.keys():
                url_of_image = i['src_xxxbig']
            elif 'src_xxbig' in i.keys():
                url_of_image = i['src_xxbig']
            elif 'src_xbig' in i.keys():
                url_of_image = i['src_xbig']
            elif 'src_big' in i.keys():
                url_of_image = i['src_big']
            if url_of_image:
                images.append(url_of_image)
                print("".join(['added ', url_of_image]))
        return images

    @staticmethod
    def warning(msg):
        print(msg)