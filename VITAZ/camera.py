import time
import os 
import cv2
import numpy as np


class VITAZSuperFace():
    def __init__(self):

        self.fullBaseCheck()

        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # no known faces detected
        self.__id__ = -1
        self.shots = 5
        self.readAMOUNT()

        # Face recognition read data 
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.read = False
        try:
            self.recognizer.read('train.yml')
        except Exception as e:
            print('--------------------------------')
            print('no train.yml')
            print('--------------------------------')
        else:
            self.read = True

    def fullBaseCheck(self):
        print('CHECKING')
        if self.readAMOUNT() == 0:
            with open('train.yml', 'w') as file:
                file.write('')

            DIR = os.path.dirname(os.path.abspath(__file__))
            IMG_DIR = os.path.join(DIR, 'imgs')
            for root, dir, files in os.walk(IMG_DIR):
                for file in files:
                    if file.endswith('.jpeg'):
                        os.remove(os.path.join(IMG_DIR + '/' + file))
        print('CHECKED')


    def readAMOUNT(self):
        with open('VITAZ/AMOUNT.txt', 'r') as file:
            self.__AMOUNT__ = int(file.readline())
        return self.__AMOUNT__

    def getLastID(self):
        return self.__id__

    def detectFaces(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.1, 1)

        # run for only first face detected
        for (x, y, w, h) in faces:
            # draw rectangle on face
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 1)
            
            # Region Of Interest (face rectangle)
            ROI = gray[y:y+h, x:x+w]
            if self.read:
                self.recognizeFaces(ROI)
            break

        _, jpeg = cv2.imencode('.jpeg', img)
        return jpeg.tobytes()

    def recognizeFaces(self, ROI):
        # ID of face and confidence (%)
        id, conf = self.recognizer.predict(ROI)
        if id and conf >= 40 and conf <= 90:
            self.__id__ = id
        else:
            self.__id__ = -1
            
        # Debug Face's ID
        print(self.__id__, conf)

    def train(self):
        x_trains = []
        y_labels = []
        for i in range(self.__AMOUNT__):
            for _ in range(self.shots):
                y_labels.append(i+1)

        DIR = os.path.dirname(os.path.abspath(__file__))
        IMG_DIR = os.path.join(DIR, 'imgs')

        for root, dir, files in os.walk(IMG_DIR):
            for file in files:
                if file.endswith(".jpeg"):
                    print('--------------------------------')
                    print(file)
                    print('--------------------------------')
                    img = cv2.imread(IMG_DIR + '/' + file)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    array = np.array(gray, "uint8")
                    faces = self.faceCascade.detectMultiScale(gray, 1.5, 5)
                    # only 1 face acceptable
                    for (x,y,w,h) in faces:
                        ROIimg = array[y:y+h, x:x+w]
                        x_trains.append(ROIimg)
                        break

        self.recognizer.train(x_trains, np.array(y_labels))
        self.recognizer.save('train.yml')
        self.recognizer.read('train.yml')
        self.read = True

    def saveAMOUNT(self):
        with open('VITAZ/AMOUNT.txt', 'w') as file:
            file.write(str(self.__AMOUNT__))

class WebCam(object):
    def __init__(self):
        # 0 - index of camera, CAP_DSHOW fixes Windows warnings
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.VITAZFaces = VITAZSuperFace()

    def __del__(self):
        self.camera.release()

    def getFrame(self):
        _, frame = self.camera.read()
        return frame

    def getCameraFrame(self):
        while True:
            # Get current frame
            frame = self.getFrame()
            # Find and detect faces 
            
            faceFrame = self.VITAZFaces.detectFaces(frame)
            yield ( b'--frame\r\n'
                    b'content-type: image/jpeg\r\n\r\n' + faceFrame + b'\r\n\r\n')

    # Return Last detected ID
    def getLastID(self):
        return self.VITAZFaces.getLastID()


    def takeSomeShots(self):
        DIR = os.path.dirname(os.path.abspath(__file__))
        IMG_DIR = os.path.join(DIR, 'imgs')

        id = self.VITAZFaces.__AMOUNT__
        self.VITAZFaces.__AMOUNT__ += 1
        for i in range(self.VITAZFaces.shots):
            img = cv2.cvtColor(self.getFrame(), cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(IMG_DIR, f'{id}_{i}.jpeg'), img)
            time.sleep(0.4)


        self.VITAZFaces.saveAMOUNT()
        self.VITAZFaces.train()
