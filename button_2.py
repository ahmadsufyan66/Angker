import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Button Example')

# Clock to control the frame rate
clock = pygame.time.Clock()

# Load button images
button_image = pygame.image.load('assets/bomoh1_bw.png')
button_hover_image = pygame.image.load('assets/bomoh1.png')

# Button properties
button_width = button_image.get_width()
button_height = button_image.get_height()
button_x = (screen_width - button_width) // 2
button_y = (screen_height - button_height) // 2

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if the mouse is over the button
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    if button_rect.collidepoint(mouse_pos):
        current_image = button_hover_image
    else:
        current_image = button_image

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the button
    screen.blit(current_image, (button_x, button_y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 frames per second
    clock.tick(60)

pygame.quit()
sys.exit()
