import pygame

print("Initializing Pygame...")
pygame.init()
print("Pygame initialized.")

import sys
import button
from subprocess import call

#Create win window
SCREEN_WIDTH , SCREEN_HEIGHT = 1680, 1050

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Angker')

#Background music 
pygame.mixer.pre_init(44100, 16, 2, 4096)

#Background
background = pygame.image.load('assets/mainmenu_bg.jpg')
scale_bg = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#available fonts
btn_font = pygame.font.Font("assets/Daydream.ttf", 60)
text_font = pygame.font.Font("GOODDC__.TTF", 200)

#colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#create button instances
start_btn = button.TextButton(450, SCREEN_HEIGHT/2, "START", btn_font, WHITE, RED, 1)
exit_btn = button.TextButton(950, SCREEN_HEIGHT/2, "EXIT", btn_font, WHITE, RED, 1)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(840, 250))
    screen.blit(img, text_rect)

#Play background music
pygame.mixer.music.load("Sound/y2mate.com - Josukes Theme but its lofi hiphop.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#game loop
run = True
while run:


    #Background Image
    screen.blit(scale_bg, (0, 0))

    draw_text("ANGKER", text_font, (255, 0, 0), 400, 600)


    if start_btn.draw(screen):
        print('START')
        pygame.quit()  # Cleanly exit Pygame
        call(('python', 'opponent_selec.py'))  # Start the new script
        sys.exit()  # Exit the current script

    if exit_btn.draw(screen):
        print('EXIT')
        #pygame.mixer.music.stop()
        run = False

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
sys.exit()