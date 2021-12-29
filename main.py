from cv2 import waitKey
from argparse import ArgumentParser
from threading import Thread
from datetime import datetime
from camera import Camera
from windowManager import WindowManager
from socket import gethostname, gethostbyname, socket, AF_INET, SOCK_STREAM


connected = False


def sendDevice(sock: socket, msg: str) -> bytes:
    if not connected:
        return None
    hexMsg = MSGS.get(msg, None)
    if not hexMsg:
        return None
    sock.send(hexMsg.encode())
    data = sock.recv(BUFSIZE)
    return data.decode()


deviceIP = '192.168.4.1'
devicePORT = 17494
hostname = gethostname()
hostIP = gethostbyname(hostname)
BUFSIZE = 4
MSGS = {
    'init':  r'\x00\x06\x07\x00',
    'ready': r'\x00\x0D\x00\x00',
    'lock':  r'\x00\x07\x00\x00',
    'pass1': r'\x00\x09\x00\x00',
    'pass2': r'\x00\x0A\x00\x00',
    'out1':  r'\x00\x0B\x00\x00',
    'out2':  r'\x00\x0C\x00\x00'
}

sock = socket(AF_INET, SOCK_STREAM)
try:
    sock.connect((deviceIP, devicePORT))
except TimeoutError as e:
    date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f'Device powered off {date}')
    # exit()
else:
    connected = True

data = sendDevice(sock, 'init')

if data and data == MSGS['ready']:
    data = sendDevice(sock, 'lock')
else:
    date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f'Device powered off {date}')
    # exit()


winMngr = WindowManager()


parser = ArgumentParser(description="Vitaz script")
parser.add_argument("-m",   dest="mode",        type=str,   default='admin')
parser.add_argument("-s",   dest="showCam",     type=int,   default=0)
parser.add_argument("-d",   dest="drawSquare",  type=int,   default=0)
parser.add_argument("-D",   dest="datasets",    type=str,   default='datasets')
args = parser.parse_args()

showCam = bool(args.showCam)
drawSquare = bool(args.drawSquare) and showCam
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
    iterationsToAprove = 5
    i = 0
    aproved = False

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

        # check if face was recognized for some frames in row
        if ret:
            aproved = False
            i = 0

        else:
            i += 1
            if i >= iterationsToAprove:
                i = iterationsToAprove
                aproved = True

        # Open Pass on Device
        if aproved:
            if sendDevice(sock, f'pass{cam.idx}') == MSGS[f'out{cam.idx}']:
                print(f'Pass {cam.idx} unlocked')

        # Show Cam Frame or Access color
        args = [cam.idx, aproved]
        if showCam:
            args.append(frame)
        winMngr.showResult(*args)

        # Key logic
        pressedKey = waitKey(1)
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
        thread = Thread(target=proccess,
                        args=(cams[i], args.mode, args.showCam))
        thread.start()


if __name__ == '__main__':
    main(args)
