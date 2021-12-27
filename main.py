import cv2
import argparse
import threading
import numpy as np
from datetime import datetime
from camera import Camera


parser = argparse.ArgumentParser(description="Vitaz script")
parser.add_argument("-m", dest="mode", type=str,
                    default='admin', required=True)
parser.add_argument("-d", dest="drawSquare", type=int,
                    default=0)
args = parser.parse_args()

drawSquare = bool(args.drawSquare)
if args.mode == 'admin':
    cams = {i: Camera(index=i, drawSquareFace=drawSquare) for i in range(2)}
elif args.mode == 'in':
    cams = {0: Camera(index=0, drawSquareFace=drawSquare)}
elif args.mode == 'out':
    cams = {1: Camera(index=1, drawSquareFace=drawSquare)}
elif args.mode == 'save':
    cams = {0: Camera(index=0, drawSquareFace=drawSquare)}
else:
    print('Wrong mode')
    exit()


def drawAccessSquare(frame, color):
    frame = cv2.rectangle(frame, (0, 0), (80, 80), color, -1)
    return frame


def enterInfo():
    name = None
    while not name:
        name = input("NAME:")
        email = input("email:")
        date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    return name, email, date


def showCam(cam: Camera, mode: str) -> None:
    idx = cam.index
    windowName = f'Camera {idx}'
    cv2.namedWindow(windowName)
    info = ''
    while True:
        ret, frame = cam.readFrame()
        if not ret:
            print(f'Camera {idx}: no frame')
            break

        frame, faces = cam.detectFaces(frame)

        ret, name, txt = cam.recognizeFace(faces)
        if txt != info:
            info = txt
            print(info)

        frame = drawAccessSquare(
            frame, (0, 0, 255)) if ret else drawAccessSquare(frame, (0, 255, 0))

        cv2.imshow(windowName, frame)

        # Key logic
        pressedKey = cv2.waitKey(1)
        if pressedKey == ord('q'):
            print('q pressed')
            break
        elif pressedKey == ord('d'):
            print('d pressed')
            cam.toggleDrawSquare()
        elif mode == 'save' and pressedKey == ord('s'):
            print('s pressed')
            name, email, date = enterInfo()
            ret = cam.saveFace(name)
            print(ret) if ret else print(name, email, date)

    del cams[idx]
    cv2.destroyWindow(windowName)


def main(args) -> None:
    for i in range(len(cams)):
        thread = threading.Thread(target=showCam, args=(cams[i], args.mode))
        thread.start()


if __name__ == '__main__':
    main(args)
