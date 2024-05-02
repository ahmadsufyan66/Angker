import pygame
import os


WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))#size of game
pygame.display.set_caption("ANGKERRRRRRR")#ni untuk dia pop up dekat atas

BLACK = (000, 000, 000) #define colour 
WHITE = (250, 250, 250)

FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 125 #Kite define size dia

HANTU_IMAGE = pygame.image.load(os.path.join('hantu.jpeg'))
HANTU_IMAGE = pygame.transform.scale(HANTU_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))#untuk resize

def draw_window():
    WIN.fill(BLACK)#fill screen
    WIN.blit(HANTU_IMAGE, (300, 100))#ni utk appearkan spaceship tu kat screen
    pygame.display.update()#kene update baru colour tu tukar



def main():

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()#kite call colour yg kite define kat atas

    pygame.quit()#untuk start game and kalu kite tutup pygame end

if __name__ == "__main__":
    main()
