import pygame
from x_cam_util import VideoGet, VideoShow

DEBUG = True

WIDTH = 1920
HEIGHT = 1080


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    font = pygame.font.SysFont('Arial', 64)
    bg_img = pygame.image.load('./assets/id_3073×757.png').convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

    glow_img = pygame.image.load('./assets/glow_star.png').convert_alpha()

    
    pygame.display.set_caption('Tracking')

    video_getter = VideoGet().start()
    video_shower = VideoShow(video_getter.frame).start()

    running = True    
    while running:

        frame = video_getter.frame
        video_shower.frame = frame

        screen.fill((0, 255, 0))

        for glow in video_shower.blobs:
            gx, gy, gw, gh, gid, gf, gs = glow
            glow_img.set_alpha(gf * 5)
            #glow_img.set_alpha(255)
            #glow_img = pygame.transform.scale(glow_img, (100, 100))
            screen.blit(glow_img, (gx, 300))
        
        #screen.blit(bg_img, (0, 0))
        fps_text = font.render(str(int(clock.get_fps())), 0, pygame.Color('red'))
        screen.blit(fps_text, (100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video_shower.stop()
                video_getter.stop()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    video_shower.stop()
                    video_getter.stop()
                    running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()