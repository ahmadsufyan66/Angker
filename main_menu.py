import pygame
import button
from subprocess import call

#create main menu window
SCREEN_WIDTH , SCREEN_HEIGHT = 1680, 1050

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')
pygame.init()

#Background
background = pygame.image.load('background image.png')

#load button images
start_img = pygame.image.load('start_btn-removebg-preview.png').convert_alpha()
exit_img = pygame.image.load('exit_btn-removebg-preview.png').convert_alpha()

#button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action 


#create button instances
start_button = button.Button(300, 450, start_img, 1.30)
exit_button = button.Button(950, 450, exit_img, 0.5)

text_font = pygame.font.Font("arial.ttf", 100)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(840, 250))
    screen.blit(img, text_rect)

#game loop
run = True
while run:

    screen.fill((255, 20, 255))
    #Background Image
    screen.blit(background, (0, 0))

    draw_text("MAIN MENU", text_font, (255, 0, 0), 400, 600)

    if start_button.draw(screen):
        print('START')
        call(('python', "opponent_selec.py"))

    if exit_button.draw(screen):
        run = False
        print('EXIT')

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()