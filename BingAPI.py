import os
import urllib.request as urllib2
import urllib
import __setup_photo__ as setup


def get_images_from_request(req, count):
    quoted_query = "%27" + req + "%27"
    quoted_query = quoted_query.replace(' ', '%20')
    res = []
    for i in range(0, count, 50):
        root_url = "https://api.datamarket.azure.com/Bing/Search/v1/"
        search_url = root_url + "Image?$format=json&Query=" + quoted_query
        search_url += "&$skip="+i.__str__()
        #change it on your acc_key
        acc_key = setup.bing_acc_key
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, search_url, acc_key, acc_key)

        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        readURL = urllib2.urlopen(search_url).read()
        tmp = str(readURL).split(',')

        for a in tmp:
            if 'MediaUrl' in a:
                b = a[a.find("http"):]
                if '.jpg' in b[-5:] or '.jpeg' in b[-5:] or '.png' in b[-5:]:
                    res.append(b[:-1])
    return res

# key words for bing
key_words = ['beautiful girl', 'cute girl']
count_for_each = 300
# dir for images
dir_ = "D:\\Graphics\\Download\\"
for word in key_words:
    res = get_images_from_request(word, count_for_each)
    for a in res:
        try:
            d = dir_ + word + '\\'
            try:
                os.stat(d)
            except:
                os.mkdir(d)
            f = d + a.split('/')[-1]
            urllib.request.urlretrieve(a, f)
            print(a)

        except:
            print('- ' + a)

    print(len(res))