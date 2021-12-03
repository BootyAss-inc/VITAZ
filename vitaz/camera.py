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



haar = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'


class Camera(object):
    camera = cv2.VideoCapture(0)

    model = Sequential()            # Emots
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    faceCascade = cv2.CascadeClassifier(haar)
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    datasetsDir = 'datasets'
    datasetSize = 30
    imgSize = (150, 150)
    showFace = True

    def __init__(self):
        if not os.path.isdir(self.datasetsDir):
            os.mkdir(self.datasetsDir)
        self.loadmodel()

    def __del__(self):
        self.camera.release()

    def loadmodel(self):
        self.model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
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
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = self.model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            cv2.putText(frame, self.emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

        return frame

    def saveFace(self, Name):
        ret = False
        path = os.path.join(self.datasetsDir, Name)
        if not os.path.isdir(path):
            os.mkdir(path)

        for c in range(self.datasetSize):
            frame = self.readFrame()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, 1.3, 4)
            if not len(faces):
                shutil.rmtree(path)
                ret = True
                break
            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                faceResized = cv2.resize(face, self.imgSize)
                cv2.imwrite(f'{path}/{c}.jpeg', faceResized)
            key = cv2.waitKey(10)

        return ret

    def recognizeFace(self):
        frame = self.readFrame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.3, 4)
        if not len(faces):
            return True, False, None

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
            return True, False, None

        (images, labels) = [np.array(lis) for lis in [images, labels]]
        self.recognizer.train(images, labels)

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            faceResized = cv2.resize(face, self.imgSize)
            id, conf = self.recognizer.predict(faceResized)
            # print(name, conf) - надо бы подкрутить логирование
            if conf > 40 and conf < 80:
                return False, True, names[id]
            else:
                return False, False, None