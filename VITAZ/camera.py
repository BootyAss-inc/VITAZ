import cv2
import numpy as np


class VITAZSuperFace():
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('train.yml')
        self.__id__ = -1

    def getLastID(self):
        return self.__id__

    def detectFaces(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.1, 1)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 1)
            
            ROI = gray[y:y+h, x:x+w]
            id, conf = self.recognizer.predict(ROI)
            if id and conf >= 50 and conf <= 80:
                self.__id__ = id
            else:
                self.__id__ = -1
            print(self.__id__, conf)
            break

        _, jpeg = cv2.imencode('.jpeg', img)
        return jpeg.tobytes()


class WebCam(object):
    def __init__(self):
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.VITAZFaces = VITAZSuperFace()

    def __del__(self):
        self.camera.release()

    def getFrame(self):
        _, frame = self.camera.read()
        return frame

    def getCameraFrame(self):
        while True:
            frame = self.getFrame()
            faceFrame = self.VITAZFaces.detectFaces(frame)
            yield ( b'--frame\r\n'
                    b'content-type: image/jpeg\r\n\r\n' + faceFrame + b'\r\n\r\n')

    def getLastID(self):
        return self.VITAZFaces.getLastID()