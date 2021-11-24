import cv2
import numpy as np


class VITAZSuperFace():
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def detectFaces(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.1, 1)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 1)
        
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

