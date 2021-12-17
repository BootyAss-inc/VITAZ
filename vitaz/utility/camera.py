import cv2
import os
import shutil
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator


from . import logger


class Camera(object):
    emotDict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    haar = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(haar)
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    datasetsDir = 'datasets'
    datasetSize = 30
    imgSize = (150, 150)

    confidence = (30, 90)

    def __init__(self, index=0, showFace=True):
        self.index = index
        self.camera = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
        self.model = Sequential(name=f'model{index}')
        self.showFace = showFace
        if not os.path.isdir(self.datasetsDir):
            os.mkdir(self.datasetsDir)
        self.loadmodel()

    def __del__(self):
        self.camera.release()

    def loadmodel(self):
        self.model.add(Conv2D(32, kernel_size=(3, 3),
                       activation='relu', input_shape=(48, 48, 1)))
        self.model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        self.model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        self.model.add(Flatten())
        self.model.add(Dense(1024, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(7, activation='softmax'))

        self.model.load_weights('model.h5')
        logger.saveInfo(f'camera {self.index} loaded')

    def readFrame(self):
        ret, frame = self.camera.read()
        return ret, frame

    def getCameraFrame(self):
        while True:
            ret, frame = self.readFrame()
            if not ret:
                continue
            if self.showFace:
                frame = self.detectFace(frame)
            _, jpeg = cv2.imencode('.jpeg', frame)
            yield (b'--frame\r\n'
                   b'content-type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    def detectFace(self, frame):
        UI_COLOR = (0, 150, 0)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), UI_COLOR, 1)
            ROI = gray[y:y + h, x:x + w]
            croppedImg = np.expand_dims(
                np.expand_dims(cv2.resize(ROI, (48, 48)), -1),
                0
            )
            emotPredictions = self.model.predict(croppedImg)
            emotMaxIndex = int(np.argmax(emotPredictions))
            cv2.putText(
                frame, self.emotDict[emotMaxIndex], (x+20, y-60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, UI_COLOR, 1, cv2.LINE_AA
            )
        return frame

    def saveFace(self, Name):
        path = os.path.join(self.datasetsDir, Name)
        if not os.path.isdir(path):
            os.mkdir(path)

        c = 0
        while c < self.datasetSize:
            ret, frame = self.readFrame()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, 1.3, 4)
            if len(faces) == 0:
                shutil.rmtree(path)
                logger.saveError(f'Camera {self.index}: no face detected')
                return {
                    'error': True,
                    'noFaceDetected': True
                }
            if len(faces) > 1:
                shutil.rmtree(path)
                logger.saveError(
                    f'Camera {self.index}: multiple faces detected')
                return {
                    'error': True,
                    'multipleFaces': True
                }

            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                faceResized = cv2.resize(face, self.imgSize)
                cv2.imwrite(f'{path}/{c}.jpeg', faceResized)
            key = cv2.waitKey(10)
            c += 1
        logger.saveInfo(f'Camera {self.index}: "{Name}" saved')
        return {
            'error': False
        }

    def recognizeFace(self):
        ret, frame = self.readFrame()
        if not ret:
            logger.saveError(f'Camera {self.index}: no frame detected')
            return {
                'error': True,
                'noFaceDetected': True
            }
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.3, 4)
        if len(faces) == 0:
            logger.saveError(f'Camera {self.index}: no face detected')
            return {
                'error': True,
                'noFaceDetected': True
            }
        if len(faces) > 1:
            logger.saveError(f'Camera {self.index}: multiple faces detected')
            return {
                'error': True,
                'multipleFaces': True
            }

        images, labels, names, id = [], [], {}, 0
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
            logger.saveError(f'Camera {self.index}: no datasets found')
            return {
                'showAccess': True,
                'accessGranted': False,
                'userName': None
            }

        (images, labels) = [np.array(lis) for lis in [images, labels]]
        self.recognizer.train(images, labels)

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            faceResized = cv2.resize(face, self.imgSize)
            id, conf = self.recognizer.predict(faceResized)

            if conf > self.confidence[0] and conf < self.confidence[1]:
                userName = names[id]
                return {
                    'showAccess': True,
                    'accessGranted': True,
                    'userName': userName
                }
            else:
                logger.saveInfo(f'Camera {self.index}: access denied')
                return {
                    'showAccess': True,
                    'accessGranted': False,
                    'userName': None
                }
