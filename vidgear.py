from threading import Thread
from vidgear.gears import CamGear
import cv2
from tracker import *

tracker = EuclideanDistTracker()

stream = CamGear(source="rtsp://admin:Admin1234@192.168.1.64:554/live").start()

object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

boxes_ids = []
frame = stream.read()


def process_cam(frame):
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 1000:
            # cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append([x, y, w, h])

    boxes_ids = tracker.update(detections)


t = Thread(target=process_cam, args=(frame,))
t.setDaemon(True)
t.start()

while True:

    frame = stream.read()

    if frame is None:
        break

    # {do something with the frame here}

    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(
            frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2
        )
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Output", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()

stream.stop()
