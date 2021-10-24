from vidgear.gears import CamGear
from vidgear.gears import VideoGear
import cv2
from tracker import *
import pygame
import numpy as np
import sys

tracker = EuclideanDistTracker()

# stream = CamGear(source="rtsp://admin:Admin1234@192.168.1.64:554/live").start()
stream = VideoGear(source="./recs/02.mp4").start()

object_detector = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=80)

CAM_WIDTH = 480
CAM_HEIGHT = 270

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 810

bg = stream.read()
bg = cv2.resize(bg, (CAM_WIDTH, CAM_HEIGHT))

takeBg = 0

while True:

    frame = stream.read()

    if frame is None:
        break

    frame = cv2.resize(frame, (CAM_WIDTH, CAM_HEIGHT))

    if takeBg == 1:
        bg = frame
        takeBg = 0

    fgMask = object_detector.apply(frame)

    diff = cv2.subtract(frame, bg)
    diff[abs(diff) < 20.0] = 0

    cv2.imshow("diff", diff)

    kernel = np.ones((2, 2), np.uint8)

    fgMask = cv2.erode(fgMask, kernel, iterations=5)
    fgMask = cv2.dilate(fgMask, kernel, iterations=5)

    fgMask[np.abs(fgMask) < 100] = 0

    contours, _ = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 100:
            # cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append([x, y, w, h])

    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(
            frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2
        )
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Frame", frame)
    cv2.imshow("FG Mask", fgMask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif ord("e") == key:
        takeBg = 1

cv2.destroyAllWindows()

stream.stop()
