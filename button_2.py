import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Button Example')

# Clock to control the frame rate
clock = pygame.time.Clock()

# Button properties
button_color = blue
button_hover_color = red
button_clicked_color = green
button_width = 200
button_height = 100
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
        if mouse_pressed[0]:  # Left mouse button is pressed
            current_color = button_clicked_color
        else:
            current_color = button_hover_color
    else:
        current_color = button_color

    # Fill the screen with white
    screen.fill(white)

    # Draw the button
    pygame.draw.rect(screen, current_color, button_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 frames per second
    clock.tick(60)

pygame.quit()
sys.exit()
