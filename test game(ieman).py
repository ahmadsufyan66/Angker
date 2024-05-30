# Import required libraries
import pygame

# Initialize Pygame
pygame.init()

import sys
import random
from subprocess import call

# Font
dialogue_font = pygame.font.Font('GOODDC__.TTF', 40)

# Dialogue
timer = pygame.time.Clock()
messages = [
    'All of that for this? Reality is often disappointing, isn\'t it?   (press enter to continue)',
    'Dread it, run from it, destiny arrives all the same, and YOU are no exception!   (press enter to continue)',
    'Isn\'t this a great text dialogue?'
]
snip = dialogue_font.render('', True, 'dark red')
counter = 0
speed = 3
active_message = None
done = False
dialogue_active = False

# Screen dimensions
SCREEN_WIDTH = 1535
SCREEN_HEIGHT = 810

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define Card class
class Card:
    def __init__(self, name, attack, defense, image, trigger_effect=None):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect()
        self.is_dragging = False
        self.trigger_effect = trigger_effect
        self.trigger_uses = 0  # Initialize trigger uses count

    def use_trigger_effect(self, player, opponent):
        if self.trigger_effect and self.trigger_uses < 3:
            self.trigger_effect(self, player, opponent)
            self.trigger_uses += 1
            print(f"{self.name}'s trigger effect used {self.trigger_uses} times.")
            if self.trigger_uses == 3:
                print(f"{self.name}'s trigger effect can no longer be used.")

# Define Player class
class Player:
    def __init__(self, name, is_human):
        self.name = name
        self.is_human = is_human
        self.deck = []
        self.skill_deck = []
        self.hand = []
        self.life_points = 80

    def shuffle(self, num=1):
        length = len(self.deck)
        for _ in range(num):
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.deck[i], self.deck[randi] = self.deck[randi], self.deck[i]

        #Shuffle skill card deck
        length = len(self.skill_deck)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.skill_deck[i], self.skill_deck[randi] = self.skill_deck[randi], self.skill_deck[i]

    def draw_card(self):
        if self.deck:
            for _ in range(2):
                card = self.deck.pop()
                self.hand.append(card)
        
        if self.skill_deck:
            for _ in range(1):
                card = self.skill_deck.pop()
                self.hand.append(card)


    def play_card(self, card_index, opponent):
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            if card.attack > opponent.life_points:
                opponent.life_points = 0
            else:
                opponent.life_points -= card.attack
            # Check for trigger effect
            card.use_trigger_effect(self, opponent)
            return card
        return None

    def ai_play(self, opponent):
        if self.hand:
            card_index = random.randint(0, len(self.hand) - 1)
            return self.play_card(card_index, opponent)
        return None

# Define a function to handle the randomization of the effect
def randomize_effect(card, player, opponent):
    if random.choice([True, False]):
        opponent.life_points -= card.attack  # Use the attack value of the card that triggered the effect
        print(f"{player.name}'s attack is doubled!")
    else:
        player.life_points += 10
        print(f"{player.name} heals 10 life points!")

# Create display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TCG Game')

# Create players
player1 = Player("Player 1", True)  # human
player2 = Player("Player 2", False)  # ai

# Create attacking area
rect_1 = pygame.Rect(0, 170, SCREEN_WIDTH, 490)

# Load card images
card_images = ["card_images/Card1.png", "card_images/Card2.png", "card_images/Card3.png", "card_images/Card4.png", "card_images/Card5.png", "card_images/skill_card.jpg"]

# Customize attack and defense for each card
cards_data = [
    {"name": "Card 1", "attack": 20, "defense": 7, "image": card_images[0], "trigger_effect": randomize_effect},
    {"name": "Card 2", "attack": 20, "defense": 9, "image": card_images[1], "trigger_effect": randomize_effect},
    {"name": "Card 3", "attack": 20, "defense": 11, "image": card_images[2], "trigger_effect": randomize_effect},
    {"name": "Card 4", "attack": 20, "defense": 11, "image": card_images[3], "trigger_effect": randomize_effect},
    {"name": "Card 5", "attack": 20, "defense": 11, "image": card_images[4], "trigger_effect": randomize_effect},  # Trigger card example
]

# Populate decks with custom cards
for card_data in cards_data:
    player1.deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"], card_data.get("trigger_effect")))
    player2.deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"], card_data.get("trigger_effect")))

#Populate skill card decks
for card_data in cards_data[5:]:
    player1.skill_deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))
    player2.skill_deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))


# Shuffle deck
player1.shuffle()
player2.shuffle()

# Drag and drop function
boxes = []
images = []

for i in range(len(card_images)):
    temp_img = pygame.image.load(card_images[i]).convert_alpha()
    image = pygame.transform.scale(temp_img, (100, 100))
    object_rect = image.get_rect()
    boxes.append(object_rect)
    images.append(card_images)

active_box = None

# Function to render dialogue
def render_dialogue(message, counter, speed):
    if counter < speed * len(message):
        counter += 1
    snip = dialogue_font.render(message[:counter // speed], True, 'dark red')
    return snip, counter

# Game loop
running = True
turn_counter = 0  # Initialize turn counter
player1_turn = True

while running:

    # Update card positions if dragging
    mouse_pos = pygame.mouse.get_pos()
    for i, card in enumerate(player1.hand):
        if card.is_dragging:
            card.rect.center = mouse_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and turn_counter < 1:  # Only draw cards for the first spacebar press
                player1.draw_card()
                player2.draw_card()
                turn_counter += 1  # Increment turn counter
                print(f"{player1.name} and {player2.name} draw a card.")
            elif event.key == pygame.K_SPACE and turn_counter == 1:  # On the second spacebar press, allow player 1 to play a card
                player1_turn = True
            elif event.key == pygame.K_RETURN and done and dialogue_active:
                dialogue_active = False
                active_message = None
                counter = 0
                done = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player1_turn:
                for num, box in enumerate(boxes):
                    if box.collidepoint(event.pos):
                        active_box = num
                for i, card in enumerate(player1.hand):
                    if card.rect.collidepoint(event.pos):
                        card.is_dragging = True

        if event.type == pygame.MOUSEMOTION:
            if active_box is not None:
                boxes[active_box].move_ip(event.rel)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if player1_turn:  # Only play card if it's player 1's turn
                # Check collision
                if object_rect.colliderect(rect_1):
                    call(('python', "opponent_selec.py"))

                active_box = None
                for i, card in enumerate(player1.hand):
                    if card.is_dragging:
                        card.is_dragging = False
                        card.rect.center = (50 + i * 120 + 50, SCREEN_HEIGHT - 170)  # Reset card position
                        played_card = player1.play_card(i, player2)
                        if played_card:
                            print(f"{player1.name} plays {played_card.name}.")
                            print(f"{player2.name} has {player2.life_points} life points remaining.")
                            if player2.life_points <= 50 and active_message is None:
                                dialogue_active = True
                                active_message = 1
                                counter = 0
                        player1_turn = False  # End player 1's turn

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # AI player's turn
    if not player1_turn and turn_counter == 1 and not dialogue_active:  # Only let AI play after player 1's turn and all cards have been drawn
        played_card = player2.ai_play(player1)
        if played_card:
            print(f"{player2.name} plays {played_card.name}.")
            print(f"{player1.name} has {player1.life_points} life points remaining.")
            if player1.life_points <= 50 and active_message is None:
                dialogue_active = True
                active_message = 0
                counter = 0
        player1_turn = True  # End AI player's turn

    # Draw background
    screen.fill(WHITE)

    # Attacking area
    pygame.draw.rect(screen, (255, 0, 0), rect_1)

    # Draw player 1's hand
    for i, card in enumerate(player1.hand):
        card.rect.bottomleft = (50 + i * 120, SCREEN_HEIGHT)  # Adjust card position
        screen.blit(card.image, card.rect)

    # Draw player 2's hand
    for i, card in enumerate(player2.hand):
        screen.blit(card.image, (50 + i * 120, 20))

    # Draw player 1's life points
    font = pygame.font.Font('GOODDC__.TTF', 36)
    text = font.render(f"{player1.name} HP: {player1.life_points}", True, BLACK)
    screen.blit(text, (50, SCREEN_HEIGHT - 50))

    # Draw player 2's life points
    text = font.render(f"{player2.name} HP: {player2.life_points}", True, BLACK)
    screen.blit(text, (50, 10))

    # Draw dialogue if active
    if dialogue_active and active_message is not None:
        snip, counter = render_dialogue(messages[active_message], counter, speed)
        screen.blit(snip, (50, SCREEN_HEIGHT - 100))
        if counter // speed >= len(messages[active_message]):
            done = True

    # If player 1 wins
    if player2.life_points <= 0:
        pygame.quit()
        call(('python', 'win.py'))

    # If player 1 loses
    if player1.life_points <= 0:
        pygame.quit()
        call(('python', 'lose.py'))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
