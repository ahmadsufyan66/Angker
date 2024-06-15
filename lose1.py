import pygame
pygame.init()
import button
from subprocess import call

#Create win window
SCREEN_WIDTH , SCREEN_HEIGHT = 1680, 1050

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Angker')

#Background music 
pygame.mixer.pre_init(44100, 16, 2, 4096)

#Background
background = pygame.image.load('assets/lose_bg.jpg')
scale_bg = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#available fonts
btn_font = pygame.font.Font("assets/Daydream.ttf", 60)
text_font = pygame.font.Font("GOODDC__.TTF", 200)

#colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#create button instances
back_button = button.TextButton(450, SCREEN_HEIGHT/2, "BACK", btn_font, WHITE, RED, 1)
retry_button = button.TextButton(950, SCREEN_HEIGHT/2, "RETRY", btn_font, WHITE, RED, 1)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(840, 250))
    screen.blit(img, text_rect)

#Play background music
pygame.mixer.music.load("Sound/Undertale OST 085  Fallen Down Reprise.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#game loop
run = True
while run:

    screen.fill((255, 20, 255))
    # Background Image   
    screen.blit(scale_bg, (0, 0))

    draw_text("YOU LOST", text_font, (255, 0, 0), 400, 600)


    if back_button.draw(screen):
        print('BACK')
        pygame.mixer.music.stop()
        pygame.quit()
        call (('python', 'opponent_selec.py'))

    if retry_button.draw(screen):
        print('RETRY')
        pygame.mixer.music.stop()
        pygame.quit()
        call (('python', 'bomoh1.py'))

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()