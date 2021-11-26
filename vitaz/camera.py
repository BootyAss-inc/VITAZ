import cv2
import os
import shutil
import numpy as np


haar = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'


class Camera(object):
    camera = cv2.VideoCapture(0)

    faceCascade = cv2.CascadeClassifier(haar)
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    datasetsDir = 'datasets'
    if not os.path.isdir(datasetsDir):
        os.mkdir(datasetsDir)
    datasetSize = 30
    imgSize = (150, 150)
    showFace = True

    def __del__(self):
        self.camera.release()

    def readFrame(self):
        _, frame = self.camera.read()
        return frame

    def getCameraFrame(self):
        while True:
            frame = self.readFrame()     
            if self.showFace: 
                frame = self.detectFace(frame)
            _, jpeg = cv2.imencode('.jpeg', frame)
            yield ( b'--frame\r\n'
                    b'content-type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    def detectFace(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)
        return frame

    def saveFace(self):
        ret = False
        id = len(next(os.walk(self.datasetsDir))[1])
        path = os.path.join(self.datasetsDir, str(id))
        if not os.path.isdir(path):
            os.mkdir(path)

        for c in range(self.datasetSize):
            frame = self.readFrame()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, 1.3, 4)
            if not len(faces):
                shutil.rmtree(path)
                ret = True
                print('NO FACE')
                break
            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                faceResized = cv2.resize(face, self.imgSize)
                cv2.imwrite(f'{path}/{c}.jpeg', faceResized)
            key = cv2.waitKey(10)

        print('Error?', ret)
        return ret

    def recognizeFace(self):
        frame = self.readFrame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.3, 4)
        if not len(faces):
            print('NO FACE')
            return True, False

        (images, labels, names, id) = ([], [], {}, 0)
        for (subdirs, dirs, files) in os.walk(self.datasetsDir):
            for subdir in dirs:
                names[id] = subdir
                subjectpath = os.path.join(self.datasetsDir, subdir)
                for filename in os.listdir(subjectpath):
                    path = subjectpath + '/' + filename
                    label = id
                    images.append(cv2.imread(path, 0))
                    labels.append(int(label))
                id += 1
        if not images or not labels:
            print('NO DATA')
            return True, False

        (images, labels) = [np.array(lis) for lis in [images, labels]]
        self.recognizer.train(images, labels)

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            faceResized = cv2.resize(face, self.imgSize)
            ID, conf = self.recognizer.predict(faceResized)
            print(ID, conf)
            if conf > 40 and conf < 80:
                return False, True
            else:
                return False, False