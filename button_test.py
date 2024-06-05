import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Button Example")

# Set up the clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 48)

# Button properties
button_rect = pygame.Rect(350, 250, 100, 50)
button_color = GREEN
button_text = font.render('Back', True, WHITE)
button_text_rect = button_text.get_rect(center=button_rect.center)

# Message properties
message = 'Press the button!'
message_text = font.render(message, True, BLACK)
message_text_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

def draw_button():
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(button_text, button_text_rect)

def draw_message():
    screen.blit(message_text, message_text_rect)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                message = 'Back button pressed!'
                message_text = font.render(message, True, BLACK)
                message_text_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Drawing
    screen.fill(WHITE)  # Clear the screen with a white background
    draw_button()
    draw_message()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
