from .camera import Camera


class CameraHandler(object):
    def __init__(self):
        self.inCamera = Camera(index=0, showFace=True)
        self.outCamera = Camera(index=1, showFace=True)
        self.enteredNames = {}

    def getInCameraFrame(self):
        return self.inCamera.getCameraFrame()

    def getOutCameraFrame(self):
        return self.outCamera.getCameraFrame()

    def inCameraRecognizeFace(self):
        ret = self.inCamera.recognizeFace()
        if ret.get('error'):
            return ret

        userName = ret.get('userName')
        if not userName:
            return ret

        if self.enteredNames.get(userName):
            ret['doublePass'] = True
            ret['doubleDirection'] = True
            return ret

        self.enteredNames[userName] = True
        return ret

    def outCameraRecognizeFace(self):
        ret = self.outCamera.recognizeFace()
        if ret.get('error'):
            return ret

        userName = ret.get('userName')
        if not userName:
            return ret

        if self.enteredNames.get(userName) == False:
            ret['doublePass'] = True
            ret['doubleDirection'] = False
            return ret

        self.enteredNames[userName] = False
        return ret

    def inCameraSaveFace(self):
        return self.inCamera.saveFace()
