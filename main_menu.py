import pygame

#create main menu window
SCREEN_HEIGHT , SCREEN_WIDTH = 1050, 1680

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

#load button images
start_img = pygame.image.load('start_btn.jpeg').convert_alpha()
exit_img = pygame.image.load('exit_btn.jpeg').convert_alpha()

#button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (500, 800))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        #draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))


#create button instances
start_button =Button(100, 200, start_img, 0.5)
exit_button = Button(650, 200, exit_img, 0.5)

#game loop
run = True
while run:

    screen.fill((202, 228, 241))

    start_button.draw()
    exit_button.draw()

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()