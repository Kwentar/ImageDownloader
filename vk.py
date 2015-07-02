import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen
import time
from datetime import date
from Profiler import Profiler
import __setup_photo__ as setup


class VkError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class VkUser:
    def __init__(self, uid, name, last_name, day_b, month_b, sex, age, city_id):
        self.uid = uid
        self.name = name
        self.last_name = last_name
        self.day_b = day_b
        self.month_b = month_b
        year_b = date.today().year - age
        if month_b < date.today().month or month_b == date.today().month and day_b < date.today().day:
            year_b - 1
        self.year_b = year_b
        self.sex = sex
        self.city_id = city_id

    def __str__(self):
        return ";".join([self.uid, self.name, self.last_name, self.day_b.__str__(),
                         self.month_b.__str__(), self.year_b.__str__(), self.sex.__str__(), self.city_id.__str__()])

    def get_age(self):
        return date.today().year - self.year_b


class Vk:
    tokens = setup.tokens
    curr_token = ''
    p = Profiler()

    @staticmethod
    def check_time(value=0.5):
        if Vk.p.get_time() < value:
            time.sleep(value)
        Vk.p.start()

    @staticmethod
    def set_token(token):
        Vk.tokens.clear()
        Vk.tokens.append(token)

    @staticmethod
    def get_token():
        for el in Vk.tokens:
            if el != Vk.curr_token:
                test_url = 'https://api.vk.com/method/getProfiles?uid=66748&access_token=' + el
                Vk.check_time(10)
                response = urlopen(test_url).read()
                result = json.loads(response.decode('utf-8'))
                if 'response' in result.keys():
                    print('now I use the ' + el + ' token')
                    Vk.curr_token = el
                    return el
        raise VkError('all tokens are invalid: ' + result['error']['error_msg'].__str__())

    @staticmethod
    def call_api(method, params):
        Vk.check_time()
        while not Vk.curr_token:
            Vk.get_token()
        if isinstance(params, list):
            params_list = params[:]
        elif isinstance(params, dict):
            params_list = params.items()
        else:
            params_list = [params]

        params_list += [('access_token', Vk.curr_token)]
        url = 'https://api.vk.com/method/%s?%s' % (method, urlencode(params_list))
        try:
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
        except URLError as err:
            print('URLError: ' + err.errno.__str__() + ", " + err.reason.__str__())

        return list()

    @staticmethod
    def get_uids(age, month, day, city_id, fields='sex'):
        search_q = list()
        search_q.append(('offset', '0'))
        search_q.append(('count', '1000'))
        search_q.append(('city', city_id))
        search_q.append(('fields', fields))
        search_q.append(('age_from', age))
        search_q.append(('age_to', age))
        search_q.append(('has_photo', '1'))
        search_q.append(('birth_day', day))
        search_q.append(('birth_month', month))
        r = Vk.call_api('users.search', search_q)
        count = 0
        users = list()
        for el in r:
            if count and 'uid' in el.keys():
                user = VkUser(uid=el['uid'].__str__(), name=el['first_name'].__str__(),
                              last_name=el['last_name'].__str__(), sex=el['sex'].__str__(),
                              day_b=day, month_b=month, age=age, city_id=city_id)
                users.append(user)
            else:
                count = el
        if count > 1000:
            Vk.warning('''Count more than 1000, count = {}, age = {},
                        month = {}, day = {}'''.format(count, age, month, day))
        return users

    @staticmethod
    def get_friends(uid, fields='city,bdate,sex'):
        search_q = list()
        search_q.append(('user_id', uid))
        search_q.append(('offset', '0'))
        search_q.append(('count', '1000'))
        search_q.append(('fields', fields))
        r = Vk.call_api('friends.get', search_q)
        count = len(r)
        users = list()
        for el in r:
            if 'user_id' in el.keys():
                if 'deactivated' in el.keys():
                    continue
                uid = el['user_id'].__str__()
                last_name = 'None'
                sex = 'None'
                name = 'None'
                city_id = 'None'
                day, month, age = [0, 0, 0]
                if 'last_name' in el.keys():
                    last_name = el['last_name'].__str__()
                if 'first_name' in el.keys():
                    name = el['first_name'].__str__()
                if 'sex' in el.keys():
                    sex = el['sex'].__str__()
                if 'city' in el.keys():
                    city_id = el['city'].__str__()
                if 'bdate' in el.keys():
                    bdate = el['bdate'].__str__().split('.')
                    if len(bdate) > 2:
                        day, month, age = map(int, bdate)
                        age = date.today().year - age
                    else:
                        day, month = map(int, bdate)

                user = VkUser(uid=uid, name=name, last_name=last_name, sex=sex, day_b=day,
                              month_b=month, age=age, city_id=city_id)
                users.append(user)
        if count > 1000:
            Vk.warning('Count more than 1000')
        return users

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