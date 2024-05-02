import pygame

import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

screen = pygame.display.set_mode(SCREEN_WIDTH, SCREEN_HEIGHT)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
pygame.display.set_caption("Move Cards !!!")

boxes = []
images = []

for i in range(0, 1):
    x, y = random.randint(1, 100), random.randint(1, 200)

    temp_img = pygame.image.load(f"{i}.png").convert_alpha()
    image = pygame.transform.scale(temp_img, (100,100))
    object_rect = image.get_rect()
    object_rect.center = (x, y)
    boxes.append(object_rect)
    images.append(image)

active_box = None

running = True
while running:

    screen.fill(BLACK)

    for event in pygame.event.get()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, box in enumerate(boxes):
                    if box.collidepoint(event.pos):
                        active_box = num
