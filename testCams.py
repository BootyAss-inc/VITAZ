import cv2


def testDevice(source):
    cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', source)
    else:
        ret, frame = cap.read()
        cv2.imshow('Input', frame)
        cv2.waitKey(0)
        cap.release()
        cv2.destroyAllWindows()



for i in range(100):
    testDevice(i) # no printout
