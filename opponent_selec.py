import pygame
import button
from subprocess import call

#create display window
SCREEN_HEIGHT = 810
SCREEN_WIDTH = 1535

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Angker')
pygame.init()

#background image
grey_img = pygame.image.load('assets/grey_bg.jpg')

def bg_grey(image):
    size = pygame.transform.scale(image, (2000, 1000))
    screen.blit(size, (0, 0)) #position

#title
text_font = pygame.font.Font("GOODDC__.TTF", 200)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(770, 100))
    screen.blit(img, text_rect)

#load button images
exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()
button_img = pygame.image.load('assets/button1.png').convert_alpha()    

#create button instances
exit_button = button.Button(30, 700, exit_img, 1.1)
bomoh1_button = button.Button(50, 200, button_img, 0.5)
bomoh2_button = button.Button(400, 400, button_img, 0.5)
bomoh3_button = button.Button(750, 200, button_img, 0.5)
bomoh4_button = button.Button(1100, 400, button_img, 0.5)    

#game loop
run = True
while run:

    screen.fill((59,59,59))

    #bg
    bg_grey(grey_img)

    #title
    draw_text("SELECT YOUR BOMOH", text_font, (255, 0, 0), 0, 0)

    #button
    if exit_button.draw(screen):
        pygame.quit()
        call(('python', "main_menu.py"))
        print('EXIT')

    if bomoh1_button.draw(screen):
        call(('python', "test game(ieman).py"))
        print('OPEN COMBAT PAGE')

    if bomoh2_button.draw(screen):
        call(('python', "test game(ieman).py"))
        print('OPEN COMBAT PAGE')

    if bomoh3_button.draw(screen):
        call(('python', "test game(ieman).py"))
        print('OPEN COMBAT PAGE')

    if bomoh4_button.draw(screen):
        call(('python', "test game(ieman).py"))
        print('OPEN COMBAT PAGE')

    #event handler
    for event in pygame.event.get():

        #quit game
        if event.type == pygame.QUIT:
            run = False

    index = 0
    pygame.display.update()

pygame.quit()