import pygame

# Initialize Pygame
pygame.init()

import sys
import button
from subprocess import call

#create display window
SCREEN_HEIGHT = 810
SCREEN_WIDTH = 1535

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Angker')

#Background
background = pygame.image.load('assets/oppsel_bg.jpg')
scale_bg = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Background sound
pygame.mixer.pre_init(44100, 16, 2, 4096)

#title
text_font = pygame.font.Font("GOODDC__.TTF", 200)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(770, 100))
    screen.blit(img, text_rect)

#load button images
exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()
bomoh1_img = pygame.image.load('assets/bomoh1_bw.png').convert_alpha()
bomoh2_img = pygame.image.load('assets/bomoh2_bw.png').convert_alpha()
bomoh3_img = pygame.image.load('assets/bomoh3_bw.png').convert_alpha()
bomoh4_img = pygame.image.load('assets/bomoh4_bw.png').convert_alpha()

bomoh1_hover_img = pygame.image.load('assets/bomoh1.png').convert_alpha()
bomoh2_hover_img = pygame.image.load('assets/bomoh2.png').convert_alpha()
bomoh3_hover_img = pygame.image.load('assets/bomoh3.png').convert_alpha()
bomoh4_hover_img = pygame.image.load('assets/bomoh4.png').convert_alpha()

#create button instances
exit_btn = button.Button(40, 700, exit_img, exit_img, 1.1)
bomoh1_btn = button.Button(280, 220, bomoh1_img, bomoh1_hover_img, 0.5)
bomoh2_btn = button.Button(560, 420, bomoh2_img, bomoh2_hover_img, 0.5)
bomoh3_btn = button.Button(840, 220, bomoh3_img, bomoh3_hover_img, 0.5)
bomoh4_btn = button.Button(1120, 420, bomoh4_img, bomoh4_hover_img, 0.5)

#game loop
run = True
while run:
    #get mouse position
    pos = pygame.mouse.get_pos()

    screen.fill((59,59,59))

    #Background Image
    screen.blit(scale_bg, (0, 0))

    #title
    draw_text("SELECT YOUR BOMOH", text_font, (255, 0, 0), 0, 0)


    #button click function
    if exit_btn.draw(screen):
        print('EXIT')
        pygame.quit()
        call(('python', "main_menu.py"))
        sys.exit()
        

    if bomoh1_btn.draw(screen):
        print('OPEN bomoh1.py')
        pygame.mixer.music.load("Sound/bomoh1 sound(1).mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(0)
        while pygame.mixer.music.get_busy():  # Wait for music to finish playing
          pygame.time.Clock().tick(0.9)  # Control the loop's speed
        pygame.quit()
        call(('python', "bomoh1.py"))
        sys.exit()
        

    if bomoh2_btn.draw(screen):
        print('OPEN bomoh2.py')
        pygame.mixer.music.load("Sound/bomoh2 sound.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(0)
        while pygame.mixer.music.get_busy():  # Wait for music to finish playing
          pygame.time.Clock().tick(0.9)  # Control the loop's speed
        pygame.quit()
        call(('python', "bomoh2.py"))
        sys.exit()
        

    if bomoh3_btn.draw(screen):
        print('OPEN bomoh3.py')
        pygame.mixer.music.load("Sound/bomoh3 sound.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(0)
        while pygame.mixer.music.get_busy():  # Wait for music to finish playing
          pygame.time.Clock().tick(0.9)  # Control the loop's speed
        pygame.quit()
        call(('python', "bomoh3.py"))
        sys.exit()
        

    if bomoh4_btn.draw(screen):
        print('OPEN bomoh4.py')
        pygame.mixer.music.load("Sound/bomoh4 sound.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(0)
        while pygame.mixer.music.get_busy():  # Wait for music to finish playing
          pygame.time.Clock().tick(0.9)  # Control the loop's speed
        pygame.quit()
        call(('python', "bomoh4.py"))
        sys.exit()
        

    #event handler
    for event in pygame.event.get():

        #quit game
        if event.type == pygame.QUIT:
            run = False

    index = 0
    pygame.display.update()

pygame.quit()
sys.exit()