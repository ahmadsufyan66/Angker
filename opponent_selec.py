import pygame
import button
import random

#create display window
SCREEN_HEIGHT = 810
SCREEN_WIDTH = 1535

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Angker')

#load button images
exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()
    
#background image
grey_img = pygame.image.load('assets/grey_bg.jpg')

def bg_grey(image):
    size = pygame.transform.scale(image, (1000, 736))
    screen.blit(size, (250, 35)) #how to efficiently change position

#create button instances
exit_button = button.Button(1360, 10, exit_img, 1.1)

#game loop
run = True
while run:

    screen.fill((59,59,59))

    #button
    if exit_button.draw(screen):
        run = False
        print('EXIT')

    #bg
    bg_grey(grey_img)

    #event handler
    for event in pygame.event.get():

        #quit game
        if event.type == pygame.QUIT:
            run = False

    index = 0
    pygame.display.update()

pygame.quit()