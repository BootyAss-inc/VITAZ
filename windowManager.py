import cv2
import numpy as np


class WindowManager(object):
    def __init__(self):
        self.windows = dict()

    def createWin(self, idx, winType) -> None:
        winName = f'{winType} {idx}'
        cv2.namedWindow(winName, flags=cv2.WINDOW_AUTOSIZE)
        self.windows[idx] = winName

    def destroyWin(self, idx) -> None:
        cv2.destroyWindow(self.windows[idx])

    def showResult(self, idx, access, frame=None):
        color = (0, 255, 0) if access else (0, 0, 255)
        if frame is None:
            result = np.zeros((300, 300, 3), np.uint8)
            result[:] = color
        else:
            result = cv2.rectangle(frame, (0, 0), (80, 80), color, -1)

        cv2.imshow(self.windows[idx], result)
