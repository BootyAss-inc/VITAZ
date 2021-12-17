from .camera import Camera
from . import logger


class CameraHandler(object):
    def __init__(self):
        logger.saveMsg('Camera setup started')
        self.inCamera = Camera(index=0, showFace=True)
        self.outCamera = Camera(index=1, showFace=True)
        self.enteredNames = {}
        logger.saveMsg('Server started')


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
            logger.saveMsg(f'Camera 0: {userName} already entered')
            return ret

        self.enteredNames[userName] = True
        logger.saveMsg(f'Camera 0: {userName} entered')
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
            logger.saveMsg(f'Camera 0: {userName} already left')
            return ret

        self.enteredNames[userName] = False
        logger.saveMsg(f'Camera 0: {userName} left')
        return ret

    def inCameraSaveFace(self):
        return self.inCamera.saveFace()
