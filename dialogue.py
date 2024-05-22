import pygame

def draw_text():
    screen.fill('dark grey')
    timer.tick(60)
    pygame.draw.rect(screen, 'black', [300, 600, 1065, 200])

pygame.init()
font = pygame.font.Font('GOODDC__.TTF', 40)
screen = pygame.display.set_mode ([1680, 1050])
timer = pygame.time.Clock()
messages = ('All of that for this? Reality is often dissappointing, isn\'t it?',
            'Dread it, run from it, destiny arrives all the same, and YOU are no exception!',
            'Isn\'t this a great text dialogue?')
snip = font.render('', True, 'dark red')
counter = 0
speed = 3
active_message = 0
message = messages[active_message]
done = False
dialogue_finished = False

run = True
while run:
    draw_text()
    if counter < speed * len(message):
        counter += 1
    elif counter >= speed * len(message):
        done = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and done and active_message < len(messages) - 1:
                active_message += 1
                done = False
                message = messages[active_message]
                counter = 0
            if event.key == pygame.K_RETURN and done and active_message == len(messages) - 1:
                if counter >= speed * len(message):
                    dialogue_finished = True
    
    if not dialogue_finished:
        snip = font.render(message[0:counter//speed], True, 'dark red')
        screen.blit(snip, (310, 600))

    if dialogue_finished:  
        pygame.draw.rect(screen, 'dark grey', [300, 600, 1065, 200])

    pygame.display.flip()
pygame.quit()