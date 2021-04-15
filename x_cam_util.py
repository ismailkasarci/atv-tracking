from threading import Thread
import cv2
from datetime import datetime
import numpy as np
from tracker import *
from x_config import *

class VideoGet:

    def __init__(self):
        self.stream1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        #self.stream1.set(cv2.CAP_PROP_FRAME_WIDTH, M_CAM_WIDTH)
        #self.stream1.set(cv2.CAP_PROP_FRAME_HEIGHT, M_CAM_HEIGHT)
        self.stream2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        #self.stream2.set(cv2.CAP_PROP_FRAME_WIDTH, M_CAM_WIDTH)
        #self.stream2.set(cv2.CAP_PROP_FRAME_HEIGHT, M_CAM_HEIGHT)
        (self.grabbed1, self.frame1) = self.stream1.read()
        (self.grabbed2, self.frame2) = self.stream2.read()
        self.frame = np.concatenate((self.frame2, self.frame1), axis=1)
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=(), daemon=True).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed1:
                self.stop()
            else:
                (self.grabbed1, self.frame1) = self.stream1.read()
                (self.grabbed2, self.frame2) = self.stream2.read()
                self.frame1 = cv2.flip(self.frame1, 1)
                self.frame2 = cv2.flip(self.frame2, 1)
                self.frame = np.concatenate((self.frame2, self.frame1), axis=1)

    def stop(self):
        self.stream1.release()
        self.stream2.release()
        self.stopped = True

class VideoShow:

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=BACKGROUND_HISTORY, varThreshold=BACKGROUND_THRESHOLD)
        self.tracker = EuclideanDistTracker()
        self.blobs = []

    def start(self):
        Thread(target=self.show, args=(), daemon=True).start()
        return self

    def show(self):
        while not self.stopped:
            mask = self.object_detector.apply(self.frame, learningRate=MASK_LEARNING_RATE)
            _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            detections = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > MIN_BLOB_SIZE:
                    #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                    x, y, w, h = cv2.boundingRect(cnt)

                    detections.append([x, y, w, h])
            
            
            boxes_ids = self.tracker.update(detections)
            
            
            for box_id in boxes_ids:
                # print(box_id)
                x, y, w, h, id = box_id
                cv2.putText(self.frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (100, 54, 255), 3)
                # cv2.rectangle(bg_img, (x, y), (x + w, y + h), (255, 255, 255), -1)

                found = False

                for blobItem in self.blobs:
                    bx, by, bw, bh, bid, bf, bs = blobItem
                    if id == bid:
                        found = True
                        blobItem[6] = (x - bx) / 20
                        blobItem[0] += blobItem[6] 
                        blobItem[1] += (y - by) / 20
                        blobItem[2] += (w - bw) / 20
                        blobItem[3] += (h - bh) / 20
                        if blobItem[5] < 100:
                            blobItem[5] += 10
                
                if not found:
                    self.blobs.append([x, y, w, h, id, 0, 1])

            temp_blobs = []
            for blobItem in self.blobs:
                found = False
                to_be_copied = True
                for box_id in boxes_ids:
                    x, y, w, h, id = box_id
                    if id == blobItem[4]:
                        found = True
                if not found:
                    #blobItem[6] = 5
                    blobItem[0] += blobItem[6]
                    blobItem[5] -= 1
                    if blobItem[5] < 0:
                        to_be_copied = False
                if to_be_copied:
                    temp_blobs.append(blobItem)
            self.blobs.clear()
            self.blobs = temp_blobs.copy()
            temp_blobs.clear()
            
            cv2.imshow("Video", self.frame)
            #cv2.imshow("Mask", mask)
            
            if cv2.waitKey(10) == ord("q"):
                self.stopped = True

    def stop(self):
        #cv2.destroyAllWindows()
        self.stopped = True