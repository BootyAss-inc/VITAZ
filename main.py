import cv2
import argparse
import threading
from datetime import datetime
from camera import Camera
from windowManager import WindowManager


winMngr = WindowManager()


parser = argparse.ArgumentParser(description="Vitaz script")
parser.add_argument("-m",   dest="mode",        type=str,   default='admin')
parser.add_argument("-s",   dest="showCam",     type=int,   default=0)
parser.add_argument("-d",   dest="drawSquare",  type=int,   default=0)
parser.add_argument("-D",   dest="datasets",    type=str,   default='datasets')
args = parser.parse_args()

showCam = bool(args.showCam)
drawSquare = bool(args.drawSquare)
datasetsDir = args.datasets

if args.mode == 'admin':
    cams = {
        i: Camera(index=i, drawSquareFace=drawSquare, datasetsDir=datasetsDir)
        for i in range(2)
    }
else:
    if args.mode == 'in':
        i = 0
    elif args.mode == 'out':
        i = 1
    elif args.mode == 'save':
        i = 0
    else:
        print('Wrong mode')
        exit()
    cams = {i: Camera(index=i, drawSquareFace=drawSquare,
                      datasetsDir=datasetsDir)}


def drawAccessSquare(frame, color):
    frame = cv2.rectangle(frame, (0, 0), (80, 80), color, -1)
    return frame


def enterInfo(names):
    name = None
    while not name or len(name) > 20 or name in names:
        name = input("NAME:").lower()
        date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    return name, date


def proccess(cam: Camera, mode: str, showCam: bool) -> None:
    winMngr.createWin(cam.idx, 'Camera' if showCam else 'Pass')

    # Last printed info
    info = ''

    while True:
        ret, frame = cam.readFrame()
        if not ret:
            print(f'Camera {cam.idx}: no frame')
            break

        # Detect faces
        frame, faces = cam.detectFaces(frame)

        # Recognize face and print if changed
        ret, name, txt = cam.recognizeFace(faces)
        if txt != info:
            info = txt
            print(info)

        # Show Cam Frame or Access color
        args = [cam.idx, ret]
        if showCam:
            args.append(frame)
        winMngr.showResult(*args)

        # Key logic
        pressedKey = cv2.waitKey(1)
        if pressedKey == ord('q'):
            break
        elif pressedKey == ord('d'):
            cam.toggleDrawSquare()
        elif mode == 'save' and pressedKey == ord('s'):
            names = cam.getNames()
            name, date = enterInfo(names)
            ret = cam.saveFace(name)
            print(ret) if ret else print(name, date)

    del cams[cam.idx]
    winMngr.destroyWin(cam.idx)


def main(args) -> None:
    for i in range(len(cams)):
        thread = threading.Thread(target=proccess,
                                  args=(cams[i], args.mode, args.showCam))
        thread.start()


if __name__ == '__main__':
    main(args)
