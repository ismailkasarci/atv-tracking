import numpy as np
import cv2

cap = cv2.VideoCapture('rtsp://username:password@192.168.1.64/1', cv2.CAP_DSHOW)

#cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)


while True:
    ret, frame = cap.read()

    height, width, _ = frame.shape
    # print(width, height)

    cv2.imshow("Show Frame", frame)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()