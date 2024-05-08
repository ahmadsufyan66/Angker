import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1535
SCREEN_HEIGHT = 810

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Card dimensions
CARD_WIDTH = 100
CARD_HEIGHT = 150

# Define Card class
class Card:
    def __init__(self, name, image_path, rect):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.rect = rect
        self.outcome = random.randint(1, 10)  # Random outcome between 1 and 10
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Define HealthBar class
class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health

    def draw(self, screen):
        # Calculate health bar fill percentage
        fill_percentage = self.current_health / self.max_health

        # Calculate fill width
        fill_width = int(self.width * fill_percentage)

        # Draw health bar outline
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)

        # Draw health bar fill
        if fill_percentage > 0.6:
            fill_color = GREEN
        elif fill_percentage > 0.3:
            fill_color = (255, 165, 0)  # Orange
        else:
            fill_color = RED
        pygame.draw.rect(screen, fill_color, (self.x + 1, self.y + 1, fill_width - 2, self.height - 2))

# Create display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Deck of Cards')

# Create cards
cards = []
card_names = ["Card1", "Card2", "Card3", "Card4", "Card5"]
for i, name in enumerate(card_names):
    image_path = f"card_images/card{i+1}.png"
    card_rect = pygame.Rect(50 + i * 270, 600, CARD_WIDTH, CARD_HEIGHT)
    card = Card(name, image_path, card_rect)
    cards.append(card)

# Create health bar
player_health_bar = HealthBar(50, 50, 200, 20, max_health=100)

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw cards
    for card in cards:
        card.draw(screen)

    # Draw health bar
    player_health_bar.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for card in cards:
                    if card.rect.collidepoint(event.pos):
                        card.dragging = True
                        mouse_x, mouse_y = event.pos
                        card.offset_x = card.rect.x - mouse_x
                        card.offset_y = card.rect.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                for card in cards:
                    card.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            for card in cards:
                if card.dragging:
                    mouse_x, mouse_y = event.pos
                    card.rect.x = mouse_x + card.offset_x
                    card.rect.y = mouse_y + card.offset_y

    pygame.display.flip()

# Quit Pygame
pygame.quit()


