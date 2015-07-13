import cv2
import os


class Face:
    def __init__(self, file_name, rect):
        self.file_name = file_name
        self.rect = rect

    def __str__(self):
        return ';'.join(self.file_name, self.rect)

    def __repr__(self):
        return ';'.join(self.file_name, self.rect)


def get_faces_from_dir(files, faces_dir, cascade):
    faces = list()
    for f in files:
        print('processing ' + f)
        (dir_, filename) = os.path.split(f)
        img = cv2.imread(f)
        res = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=3, flags=0)
        if len(res):
            for (x, y, w, h) in res:
                faces.append(Face(filename, (x, y, w, h)))
                image_name = os.path.join(faces_dir, ';'.join([filename, ";".join(map(str, (x, y, w, h)))]) + '.png')
                cv2.imwrite(image_name, img[y:y+h, x:x+w])
    with open(os.path.join(faces_dir, 'faces.txt'))


def get_faces(dir_):
    cascade = cv2.CascadeClassifier("D:\\Install\\opencv\\sources\\data\\lbpcascades\\Twenty-thirdRelease.xml")
    files = [os.path.join(dir_, f) for f in os.listdir(dir_) if os.path.isfile(os.path.join(dir_, f))]
    image_exts = ['.jpeg', '.jpg', '.png', '.gif', '.jpeg']
    faces_dir = os.path.join(dir_, 'faces')
    if not os.path.exists(faces_dir):
        os.mkdir(faces_dir)
    get_faces_from_dir([f for f in files if os.path.splitext(f)[-1] in image_exts], faces_dir, cascade)