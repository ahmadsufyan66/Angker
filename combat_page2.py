import pygame
import random
import sys
import button
from subprocess import call

# Create display window
SCREEN_HEIGHT = 810
SCREEN_WIDTH = 1535
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Angker')

# Load button images
exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('assets/restart_btn.png').convert_alpha()

#define colours
BG = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create button instances
exit_button = button.Button(1360, 10, exit_img, 1.1)
restart_button = button.Button(1420, 10, restart_img, 0.8)

#Create attacking area
rect_1 = pygame.Rect(0, 0, 1535, 405)

# Background images
blood_img = pygame.image.load('assets/blood_bg.png')
grey_img = pygame.image.load('assets/grey_bg.jpg')

# Function to display background images
def bg_blood(image):
    size = pygame.transform.scale(image, (1000, 736))
    screen.blit(size, (0, 0))

def bg_grey(image):
    size = pygame.transform.scale(image, (1000, 736))
    screen.blit(size, (250, 35))

# Drag and drop function
boxes = []
images = []

for i in range(0, 1):
    x, y = 767.5, 510
    temp_img = pygame.image.load("card_images/Card1.png").convert_alpha()
    image = pygame.transform.scale(temp_img, (100,100))
    object_rect = image.get_rect()
    object_rect.center = (x, y)
    boxes.append(object_rect)
    images.append(image)

active_box = None

# Game loop
run = True
while run:
    screen.fill((59,59,59))

    #Attacking area
    pygame.draw.rect(screen, RED, rect_1)

    #Restart and exit button
    if restart_button.draw(screen):
        run = False
        print('RESTART')
    if exit_button.draw(screen):
        run = False
        print('EXIT')
    
    bg_blood(blood_img)
    bg_grey(grey_img)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, box in enumerate(boxes):
                    if box.collidepoint(event.pos):
                        active_box = num

        if event.type == pygame.MOUSEMOTION:
            if active_box != None:
                boxes[active_box].move_ip(event.rel)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:

                #Check collision
                if object_rect.colliderect(rect_1):
                    print("Card 1 is played.")
            
                active_box = None

    #Making cards appear on screen
    index = 0
    for image in images:
        screen.blit(image, boxes[index])
        index += 1

    pygame.display.update()

pygame.quit()
