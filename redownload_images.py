from Internet import Internet
import os


def redownload_images(images: dict):
    counter = 1
    len_images = len(images).__str__()
    for url_, name_ in images.items():
        Internet.load_image_chunk(url_, name_, 'D:\\')
        print("downloaded ", name_, counter.__str__(), '/', len_images)
        counter += 1


def redownload_file(file_name: str, source_dir: str):
    images = {}
    with open(file_name) as f:
        lines = map(str.strip, f.readlines())
    for line in lines:
        url_, name_ = line.split(',')
        images[url_] = os.path.join( source_dir, os.path.split(name_)[0].split('\\')[-1], os.path.split(name_)[1])
    redownload_images(images)

redownload_file("H:\\vk\\need_reload.txt", "H:\\vk\\")