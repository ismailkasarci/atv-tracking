import cv2 
import pygame
import numpy as np
import concurrent.futures
from threading import Thread

WIDTH = 640
HEIGHT = 480

pygame.init()
screen = pygame.display.set_mode((WIDTH * 2, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 64)

cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap1.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

#cap2.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
#cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

frame1 = None
#frame2 = None



def cam1_read():
    while True:
        ret1, frame1 = cap1.read()
        frame1 = cv2.flip(frame1, 1)

def cam2_read():
    while False:
        ret2, frame2 = cap2.read()
        frame2 = cv2.flip(frame2, 1)
        #print(ret2)


t1 = Thread(target=cam1_read)
t1.setDaemon(True)
t1.start()
#t2 = Thread(target=cam2_read)
#t2.setDaemon(True)
#t2.start()

running = True
while running:
    
    #if frame1 and frame2:
    #vis = np.concatenate((frame2, frame1), axis=1)
    if True:
        cv2.imshow("C1", frame1)

    #cv2.imshow("Combine", framex1)

    screen.fill((255, 0, 0))
    #screen.blit(frame1, (0, 0))
    fps_counter = font.render(str(int(clock.get_fps())), 1, pygame.Color('coral'))
    screen.blit(fps_counter, (20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    clock.tick(60)
    pygame.display.update()

pygame.quit()
cap1.release()
#cap2.release()
cv2.destroyAllWindows()