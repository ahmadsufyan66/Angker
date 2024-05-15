import pygame
import random
import sys
import button

# Create display window
SCREEN_HEIGHT = 810
SCREEN_WIDTH = 1535
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Angker')

# Load button images
exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('assets/restart_btn.png').convert_alpha()
button1_img = pygame.image.load('assets/button1.png').convert_alpha()
button2_img = pygame.image.load('assets/button2.png').convert_alpha()
button3_img = pygame.image.load('assets/button3.png').convert_alpha()

# Create button instances
exit_button = button.Button(1360, 10, exit_img, 1.1)
restart_button = button.Button(1420, 10, restart_img, 0.8)
button1 = button.Button(100, 700, button1_img, 0.3)
button2 = button.Button(600, 700, button2_img, 0.3)
button3 = button.Button(1100, 700, button3_img, 0.3)

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
    x, y = random.randint(1, 100), random.randint(1, 200)
    temp_img = pygame.image.load("assets/attack_card.png").convert_alpha()
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

    if restart_button.draw(screen):
        print('RESTART')
    if exit_button.draw(screen):
        run = False
        print('EXIT')
    if button1.draw(screen):
        print('Display Card 1')
        # Display card 1 when button 1 is clicked

    if button2.draw(screen):
        print('Display Card 2')
        # Display card 2 when button 2 is clicked

    if button3.draw(screen):
        print('Display Card 3')
        # Display card 3 when button 3 is clicked

    bg_grey(grey_img)
    bg_blood(blood_img)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, box in enumerate(boxes):
                    if box.collidepoint(event.pos):
                        active_box = num

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_box = None

        if event.type == pygame.MOUSEMOTION:
            if active_box != None:
                boxes[active_box].move_ip(event.rel)

    index = 0
    for image in images:
        screen.blit(image, boxes[index])
        index += 1

    pygame.display.update()

pygame.quit()
