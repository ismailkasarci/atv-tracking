import pygame

WIDTH, HEIGHT = 1920, 1080 

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Tracking')

glow_img = pygame.image.load('./assets/glow_star.png').convert_alpha()

    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        screen.fill((255, 0, 0))
        
        screen.blit(glow_img, (20, 20))

        pygame.display.flip()

pygame.quit()