import pygame
import button

#create display window
SCREEN_HEIGHT = 810
SCREEN_WIDTH = 1535

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Angker')

#load button images
exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('assets/restart_btn.png').convert_alpha()
    
#background image
blood_img = pygame.image.load('assets/blood_bg.png') #how to make this more efficient?
grey_img = pygame.image.load('assets/grey_bg.jpg')
def bg_blood(image):
    size = pygame.transform.scale(image, (1000, 736))
    screen.blit(size, (0, 0)) #position change

def bg_grey(image):
    size = pygame.transform.scale(image, (1000, 736))
    screen.blit(size, (250, 35)) #how to efficiently change position

#create button instances
exit_button = button.Button(1360, 10, exit_img, 1.1)
restart_button = button.Button(1420, 10, restart_img, 0.8)

#game loop
run = True
while run:

    screen.fill((59,59,59))

    if restart_button.draw(screen):
        print('RESTART')
    if exit_button.draw(screen):
        run = False
        print('EXIT')

    bg_grey(grey_img)
    bg_blood(blood_img)

    #event handler
    for event in pygame.event.get():

        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()