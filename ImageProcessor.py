import cv2
import os
from Profiler import Profiler
import __setup_photo__ as setup


class Face:
    def __init__(self,  uid, file_name, rect):
        self.file_name = file_name
        self.rect = rect
        self.uid = uid

    def __str__(self):
        return ';'.join([self.uid, self.file_name, ";".join(map(str, self.rect))])

    def __repr__(self):
        return ';'.join([self.uid, self.file_name, ";".join(map(str, self.rect))])


def get_faces_from_dir(files, faces_dir, cascade):
    faces = list()
    for f in files:
        print('processing ' + f)
        (dir_, filename) = os.path.split(f)
        img = cv2.imread(f)
        res = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=3, flags=0, minSize=(40, 40))
        if len(res):
            for (x, y, w, h) in res:
                face = Face(os.path.split(dir_)[-1], filename, (x, y, w, h))
                faces.append(face)
                image_name = os.path.join(faces_dir, face.__str__() + '.png')
                cv2.imwrite(image_name, img[y:y+h, x:x+w])
    with open(os.path.join(faces_dir, 'faces.txt', ), 'w') as faces_file:
        for face in faces:
            faces_file.write(face.__str__() + os.linesep)


def get_count_faces(dir_):
    count = 0
    count_of_person = 0
    for (root_dir, folders, files) in os.walk(dir_):
        if os.path.split(root_dir)[-1] == 'faces':
            cur_count = len([f for f in os.listdir(root_dir) if 'txt' not in f])
            count += cur_count
            count_of_person += 1
            if count_of_person % 100 == 0:
                print('now I get ' + count_of_person.__str__() + ' people, current I get ' + count + 'faces')
    return count


def get_faces(dir_):
    cascade = cv2.CascadeClassifier(setup.cascade_path)
    image_exts = ['.jpeg', '.jpg', '.png', '.gif', '.jpeg']
    count = 0
    p = Profiler()
    dirs = list()
    count_dir = 0
    for (root_dir, folders, files) in os.walk(dir_):
        if ('faces' in folders and len(folders) == 1 or not len(folders)) and os.path.split(root_dir)[-1] != 'faces':
            faces_txt_path = os.path.join(root_dir, 'faces', 'faces.txt')
            if os.path.exists(faces_txt_path):
                # print('this user has been processed ' + root_dir)
                continue
            count_dir += 1
            if count_dir % 100 == 0:
                print('now I get ' + count_dir.__str__() + ' folders')
            dirs.append(root_dir)
    count_person = len(dirs)
    p.start()
    for curr_dir in dirs:
        image_files = list()
        files = os.listdir(curr_dir)
        for el in files:
            if os.path.splitext(el)[-1] in image_exts:
                image_files.append(os.path.join(curr_dir, el))
        faces_dir = os.path.join(curr_dir, 'faces')
        if not os.path.exists(faces_dir):
            os.mkdir(faces_dir)
        get_faces_from_dir(image_files, faces_dir, cascade)
        count += 1
        print('Processed {} person ({}%), current time is {}, expected time is {} min'.
              format(count,
                     round(count / count_person * 100, 3),
                     round(p.get_time() / 60, 3),
                     round(p.get_time() * count_person / count / 60, 3)))
    print('all time is ' + round(p.get_time() / 60, 3).__str__())