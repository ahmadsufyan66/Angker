import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1535
SCREEN_HEIGHT = 810

# Font
dialogue_font = pygame.font.Font('GOODDC__.TTF', 40)

# Background
background = pygame.image.load('assets/bomoh1_bg.jpg')
scale_bg = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define Card class
class Card:
    def __init__(self, name, attack, defense, image):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.base_image = pygame.image.load(image)
        self.base_image = pygame.transform.scale(self.base_image, (150, 250))
        self.image = self.base_image.copy()  # Create a copy of the base image
        self.rect = self.image.get_rect()
        self.is_dragging = False
        self.click_count = 0  # Initialize click count attribute
        self.hovered = False  # Track whether the card is being hovered over

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            # Increase the size of the card when hovered over
            self.image = pygame.transform.scale(self.base_image, (180, 270))
        else:
            self.hovered = False
            self.image = self.base_image.copy()  # Reset the image to its original size

    def render(self, surface):
        surface.blit(self.image, self.rect)

# Define Player class
class Player:
    def __init__(self, name, is_human, life_points=100):
        self.name = name
        self.is_human = is_human
        self.deck = []
        self.skill_deck = []
        self.hand = []
        self.life_points = life_points
        self.initial_life_points = life_points  
        self.additional_play = False  # Flag to allow an additional card play

    def shuffle(self, num=1):
        length = len(self.deck)
        for _ in range(num):
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.deck[i], self.deck[randi] = self.deck[randi], self.deck[i]

        # Shuffle skill card deck
        length = len(self.skill_deck)
        for _ in range(num):
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.skill_deck[i], self.skill_deck[randi] = self.skill_deck[randi], self.skill_deck[i]

    def draw_cards(self):
        # Count cards from deck and skill_deck in hand
        normal_deck_count = sum(1 for card in self.hand if card not in self.skill_deck)
        skill_deck_count = sum(1 for card in self.hand if card in self.skill_deck)

        # Draw normal cards
        if normal_deck_count == 0:
            for _ in range(min(2, len(self.deck))):  # Ensure we don't draw more cards than available
                if self.deck:
                    self.hand.append(self.deck.pop())
        elif normal_deck_count == 1:
            if self.deck:
                self.hand.append(self.deck.pop())
        elif normal_deck_count == 2:
            for _ in range(min(2, len(self.deck))):
                if self.deck:
                    self.hand.append(self.deck.pop())

        # Draw skill cards
        if skill_deck_count == 0:
            if self.skill_deck:
                self.hand.append(self.skill_deck.pop())

    def play_card(self, card_index, opponent):
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            if card.attack > opponent.life_points:
                opponent.life_points = 0
            else:
                opponent.life_points -= card.attack
            # Check for card skill
            if card.name == "Kappa (skill)":
                self.life_points += 10
            if card.name == "Pocong (skill)":
                # Implement skill effect for Pocong
                pass
            if card.name == "Freddy Krueger (skill)":
                lost_life_points = self.initial_life_points - self.life_points
                card.attack += lost_life_points  # Increase attack based on lost life points
            if card.name == "Saka (skill)":
                lost_life_points = self.initial_life_points - self.life_points
                card.attack += lost_life_points  # Increase attack based on lost life points
            if card.name == "Pontianak (skill)":
                self.additional_play = True
            return card
        return None

    def ai_play(self, opponent):
        if self.hand:
            # Improve AI strategy by choosing the most effective card
            card_index = max(range(len(self.hand)), key=lambda i: self.hand[i].attack)
            return self.play_card(card_index, opponent)
        return None

# Create display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('ANGKER')

# Create players with adjusted life points
player1 = Player("Player 1", True, life_points=80)  # human with lower starting life points
player2 = Player("Player 2", False, life_points=120)  # AI with higher starting life points

# Create attacking area
rect_1 = pygame.Rect(0, 170, SCREEN_WIDTH, 490)

# Load card images
card_images = ["card_images/kappa.png", "card_images/pocong.png", "card_images/freddykrueger.png", "card_images/saka.png", "card_images/pontianak.png",
               "card_images/skill_kappa.png", "card_images/skill_pocong.png", "card_images/skill_freddykrueger.png", "card_images/skill_saka.png", "card_images/skill_pontianak.png"]

# Customize attack and defense for each card
cards_data = [
    {"name": "Kappa", "attack": 5, "defense": 7, "image": card_images[0]},
    {"name": "Pocong", "attack": 5, "defense": 9, "image": card_images[1]},
    {"name": "Freddy Krueger", "attack": 5, "defense": 11, "image": card_images[2]},
    {"name": "Saka", "attack": 5, "defense": 11, "image": card_images[3]},
    {"name": "Pontianak", "attack": 5, "defense": 11, "image": card_images[4]},
    {"name": "Kappa (skill)", "attack": 5, "defense": 7, "image": card_images[5]},
    {"name": "Pocong (skill)", "attack": 5, "defense": 9, "image": card_images[6]},
    {"name": "Freddy Krueger (skill)", "attack": 5, "defense": 11, "image": card_images[7]},
    {"name": "Saka (skill)", "attack": 5, "defense": 11, "image": card_images[8]},
    {"name": "Pontianak (skill)", "attack": 5, "defense": 11, "image": card_images[9]}
]

# Populate decks with custom cards
for card_data in cards_data[0:5]:
    player1.deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))
    player2.deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))

for card_data in cards_data[5:]:
    player1.skill_deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))
    player2.skill_deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))

# Shuffle decks
player1.shuffle()
player2.shuffle()

# Draw initial hands
player1.draw_cards()
player2.draw_cards()

# Start game loop
running = True
clock = pygame.time.Clock()
selected_card = None

while running:
    screen.fill(WHITE)
    screen.blit(scale_bg, (0, 0))
    text_surface = dialogue_font.render(f"Player 1 Life Points: {player1.life_points}", True, (0, 0, 0))
    screen.blit(text_surface, (50, 50))

    text_surface = dialogue_font.render(f"Player 2 Life Points: {player2.life_points}", True, (0, 0, 0))
    screen.blit(text_surface, (SCREEN_WIDTH - 450, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for index, card in enumerate(player1.hand):
                    if card.rect.collidepoint(event.pos):
                        selected_card = card
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and selected_card:
                if rect_1.collidepoint(event.pos):
                    player1.play_card(player1.hand.index(selected_card), player2)
                    player1.draw_cards()
                    player2.ai_play(player1)
                    player2.draw_cards()
                selected_card = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    for card in player1.hand:
        card.update(pygame.mouse.get_pos())
        card.render(screen)

    pygame.draw.rect(screen, BLACK, rect_1, 2)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

