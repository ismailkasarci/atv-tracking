import numpy as np
import cv2

cap = cv2.VideoCapture('rtsp://username:password@192.168.1.64/1', cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

fourcc = cv2.cv.CV_FOURCC(*'XVID') 
#fourcc = cv2.cv.CV_FOURCC(*'H264') #mp4
#fourcc = cv2.cv.CV_FOURCC(*'X264') #mp4

ret, frame = cap.read()
height, width, _ = frame.shape
# print(width, height)
fps=20
out = cv2.VideoWriter('output.avi', fourcc, fps, (int(width),int(height)))

while True:
    ret, frame = cap.read()

    out.write(frame)
    cv2.imshow("Capture Frame", frame)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()