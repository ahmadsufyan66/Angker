import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define Card class
class Card:
    def __init__(self, name, attack, defense, image):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect()
        self.is_dragging = False

# Define Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.hand = []
        self.life_points = 8000

    def draw_card(self):
        if self.deck:
            card = self.deck.pop()
            self.hand.append(card)

    def play_card(self, card_index, opponent):
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            if card.attack > opponent.life_points:
                opponent.life_points = 0
            else:
                opponent.life_points -= card.attack
            return card
        return None

# Create display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TCG Game')

# Create players
player1 = Player("Player 1")
player2 = Player("Player 2")

# Load card images
card_images = ["card_images/Card1.png", "card_images/Card2.png", "card_images/Card3.png"]

# Customize attack and defense for each card
cards_data = [
    {"name": "Card 1", "attack": 800, "defense": 700, "image": card_images[0]},
    {"name": "Card 2", "attack": 1000, "defense": 900, "image": card_images[1]},
    {"name": "Card 3", "attack": 1200, "defense": 1100, "image": card_images[2]}
]

# Populate decks with custom cards
for card_data in cards_data:
    player1.deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))
    player2.deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player1.draw_card()
                player2.draw_card()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player1.name == "Player 1":
                for i, card in enumerate(player1.hand):
                    if card.rect.collidepoint(event.pos):
                        card.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i, card in enumerate(player1.hand):
                if card.is_dragging:
                    card.is_dragging = False
                    card.rect.center = (50 + i * 120 + 50, SCREEN_HEIGHT - 170)  # Reset card position
                    played_card = player1.play_card(i, player2)
                    if played_card:
                        print(f"{player1.name} plays {played_card.name}.")
                        print(f"{player2.name} has {player2.life_points} life points remaining.")

    # Update card positions if dragging
    mouse_pos = pygame.mouse.get_pos()
    for i, card in enumerate(player1.hand):
        if card.is_dragging:
            card.rect.center = mouse_pos

    # Draw background
    screen.fill(WHITE)

    # Draw player 1's hand
    for i, card in enumerate(player1.hand):
        card.rect.bottomleft = (50 + i * 120, SCREEN_HEIGHT)  # Adjust card position
        screen.blit(card.image, card.rect)

    # Draw player 2's hand
    for i, card in enumerate(player2.hand):
        screen.blit(card.image, (50 + i * 120, 20))

    # Draw player 1's life points
    font = pygame.font.Font(None, 36)
    text = font.render(f"{player1.name} HP: {player1.life_points}", True, BLACK)
    screen.blit(text, (50, SCREEN_HEIGHT - 50))

    # Draw player 2's life points
    text = font.render(f"{player2.name} HP: {player2.life_points}", True, BLACK)
    screen.blit(text, (50, 10))

    pygame.display.flip()

# Quit Pygame
pygame.quit()






















