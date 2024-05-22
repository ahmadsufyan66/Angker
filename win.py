import pygame
import button
from subprocess import call

#Create win window
SCREEN_WIDTH , SCREEN_HEIGHT = 1680, 1050

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('win page')
pygame.init()

#Background music 
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

#Background
background = pygame.image.load('win_background.png')
scale_bg = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#load button images
back_img = pygame.image.load('back-removebg-preview.png').convert_alpha()
retry_img = pygame.image.load('retry_button-removebg-preview.png').convert_alpha()

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
back_button = button.Button(400, 540, back_img, 0.9)
retry_button = button.Button(950, 450, retry_img, 0.85)

text_font = pygame.font.Font("GOODDC__.TTF", 200)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(840, 250))
    screen.blit(img, text_rect)

#Play background music
pygame.mixer.music.load("Undertale OST 073  The Choice.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#game loop
run = True
while run:

    screen.fill((255, 20, 255))
    #Background Image
    screen.blit(scale_bg, (0, 0))

    draw_text("YOU WIN", text_font, (255, 0, 0), 400, 600)


    if back_button.draw(screen):
        print('BACK')
        pygame.mixer.music.stop()
        pygame.quit()
        call (('python', 'main_menu.py'))

    if retry_button.draw(screen):
        print('RETRY')
        pygame.mixer.music.stop()
        pygame.quit()
        call (('python', 'test game(ieman).py'))

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()