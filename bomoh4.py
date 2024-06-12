# Import required libraries
import pygame

# Initialize Pygame
pygame.init()

import pygame.time
import sys
import random
from subprocess import call

# Screen dimensions
SCREEN_WIDTH = 1535
SCREEN_HEIGHT = 810

# Font
dialogue_font = pygame.font.Font('GOODDC__.TTF', 40)

#Background
background = pygame.image.load('assets/bomoh1_bg.jpg')
scale_bg = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Dialogue
timer = pygame.time.Clock()
messages = [
    'All of that for this? Reality is often disappointing, isn\'t it?   (press enter to continue)',
    'Dread it, run from it, destiny arrives all the same, and YOU are no exception!   (press enter to continue)',
    'Empty deck! (press enter to continue)',
    'Isn\'t this a great text dialogue?'
]

snip = dialogue_font.render('', True, 'dark red')
counter = 0
speed = 3
active_message = None
done = False
dialogue_active = False


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define Card class
class Card:
    def __init__(self, name, attack, defense, image, trigger_effect=None):
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
    def __init__(self, name, is_human,initial_life_points ,aggressiveness=1.5):
        self.name = name
        self.is_human = is_human
        self.deck = []
        self.skill_deck = []
        self.hand = []
        self.life_points = initial_life_points
        self.additional_play = False  # Flag to allow an additional card play
        self.aggressiveness = aggressiveness  # Aggressiveness parameter for AI

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
            if card.attack > opponent.life_points + card.defense:
                opponent.life_points = 0
            else:
                opponent.life_points -= card.attack
            if card.name == "Kappa (skill)":
                print("")
                print(f"{self.name} +10 HP")
                print(f"{self.name} has {self.life_points} remaining.")
                print("")
                self.life_points += 10
            if card.name == "Pocong (skill)":
                print("")
                print("-Will insert skill-")
                print("")
            if card.name == "Freddy Krueger (skill)":
                lost_life_points = self.initial_life_points - self.life_points
                card.attack += lost_life_points  # Increase attack based on lost life points
                print("")
                print(f"Freddy Krueger attacks with {card.attack} points.")
                print("")
            if card.name == "Saka (skill)":
                lost_life_points = self.initial_life_points - self.life_points
                card.attack += lost_life_points  # Increase attack based on lost life points
                print("")
                print(f"Saka attacks with {card.attack} points.")
                print("")
            if card.name == "Pontianak (skill)":
                print("")
                print(f"{self.name} gains another turn!")
                print("")
                self.additional_play = True
            return card
        return None

    def ai_play(self, opponent):
        if self.hand:
            # Improve AI strategy by choosing the most effective card
            if self.aggressiveness >= 1.0:
                card_index = max(range(len(self.hand)), key=lambda i: self.hand[i].attack)
            else:
                card_index = random.randint(0, len(self.hand) - 1)
            return self.play_card(card_index, opponent)
        return None

# Create display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('ANGKER')

# Create players
player1 = Player("Player 1", True,80)  # human
player2 = Player("Player 2", False,120, aggressiveness=1.5,)  # ai (more aggressive)

# Create attacking area
rect_1 = pygame.Rect(0, 170, SCREEN_WIDTH, 490)

# Load card images
card_images = ["card_images/kappa.png", "card_images/pocong.png", "card_images/freddykrueger.png", "card_images/saka.png", "card_images/pontianak.png",
               "card_images/skill_kappa.png", "card_images/skill_pocong.png", "card_images/skill_freddykrueger.png", "card_images/skill_saka.png", "card_images/skill_pontianak.png"]

# Customize attack and defense for each card
cards_data = [
    {"name": "Kappa", "attack": 15, "defense": 5, "image": card_images[0]},  # Increase attack to 15 and lower defense to 5
    {"name": "Pocong", "attack": 13, "defense": 7, "image": card_images[1]},  # Increase attack to 13 and lower defense to 7
    {"name": "Freddy Krueger", "attack": 14, "defense": 8, "image": card_images[2]},  # Increase attack to 14 and lower defense to 8
    {"name": "Saka", "attack": 12, "defense": 6, "image": card_images[3]},  # Increase attack to 12 and lower defense to 6
    {"name": "Pontianak", "attack": 16, "defense": 9, "image": card_images[4]},  # Increase attack to 16 and lower defense to 9
    {"name": "Kappa (skill)", "attack": 14, "defense": 5, "image": card_images[5]},  # Increase attack to 14 and lower defense to 5
    {"name": "Pocong (skill)", "attack": 15, "defense": 7, "image": card_images[6]},  # Increase attack to 15 and lower defense to 7
    {"name": "Freddy Krueger (skill)", "attack": 14, "defense": 8, "image": card_images[7]},  # Increase attack to 14 and lower defense to 8
    {"name": "Saka (skill)", "attack": 13, "defense": 6, "image": card_images[8]},  # Increase attack to 13 and lower defense to 6
    {"name": "Pontianak (skill)", "attack": 16, "defense": 9, "image": card_images[9]}  # Increase attack to 16 and lower defense to 9
]

# Populate decks with custom cards
for card_data in cards_data[0:5]:
    player1.deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"], card_data.get("trigger_effect")))
    player2.deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"], card_data.get("trigger_effect")))

#Populate skill card decks
for card_data in cards_data[5:]:
    player1.skill_deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))
    player2.skill_deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))


# Shuffle deck
player1.shuffle()
player2.shuffle()

#Draw life scale
def draw_life_scale(player, x, y):
    pygame.draw.rect(screen, GREEN, (x, y, player.life_points * 2, 20))

# Drag and drop function
boxes = []
images = []

for i in range(len(card_images)):
    temp_img = pygame.image.load(card_images[i]).convert_alpha()
    image = pygame.transform.scale(temp_img, (100000, 100))
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
            if event.key == pygame.K_SPACE:
                if turn_counter < 1 or (not player1.hand and not player2.hand):  # First turn or both hands are empty
                    while len(player1.hand) <3:
                        player1.draw_cards()
                    while len(player2.hand) <3:
                        player2.draw_cards()
                    turn_counter += 1  # Increment turn counter
                    print("")
                    print(f"{player1.name} and {player2.name} draw cards.")
                    print("")
                elif not player1.hand and len(player2.hand) > 0:  # Player 1's hand is empty and player 2 has cards
                    #draw card for player 1
                    while len(player1.hand) <3:
                        player1.draw_cards()
                    # Draw cards for player 2
                    while len(player2.hand) <3:
                        player2.draw_cards()
                    turn_counter += 1  # Increment turn counter
                    print("")
                    print(f"{player1.name} and {player2.name} draw cards until they have the required number of cards.")
                    print("")
                elif turn_counter == 1:  # On the second spacebar press, allow player 1 to play a card
                    player1_turn = True
                    player1.draw_cards()
                    player2.draw_cards()
            elif event.key == pygame.K_RETURN and done and dialogue_active:
                dialogue_active = False
                active_message = None
                counter = 0
                done = False
            elif len(player1.deck) == 0 and len(player2.deck) == 0:
                dialogue_active = True
                active_message = 1
                counter = 0

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
                            print("")
                            print(f"{player1.name} plays {played_card.name}.")
                            print(f"{player2.name} has {player2.life_points} life points remaining.")
                            print("")
                            if player2.life_points <= 50 and active_message is None:
                                dialogue_active = True
                                active_message = 1
                                counter = 0
                        # Check if player can play another card
                        if player1.additional_play:
                            player1_turn = True  # Allow player 1 to play another card
                            player1.additional_play = False  # Reset the flag
                        else:
                            player1_turn = False  # End player 1's turn
                        # Switch to player 2's turn after player 1's turn

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # AI player's turn
    if not player1_turn and not dialogue_active:  # Only let AI play after player 1's turn and all cards have been drawn
        played_card = player2.ai_play(player1)
        if played_card:
            print("")
            print(f"{player2.name} plays {played_card.name}.")
            print(f"{player1.name} has {player1.life_points} life points remaining.")
            print("")
            if player1.life_points <= 50 and active_message is None:
                dialogue_active = True
                active_message = 0
                counter = 0
        # Switch to player 1's turn after player 2's turn
        player1_turn = True

    #Background Image
    screen.blit(scale_bg, (0, 0))

    # Draw player 1's hand
    for i, card in enumerate(player1.hand):
        card.rect.bottomleft = (500 + i * 200, SCREEN_HEIGHT)  # Adjust card position
        screen.blit(card.image, card.rect)

    for card in player1.hand:
        card.update(pygame.mouse.get_pos())
        card.render(screen)

    # Draw player 2's hand
    for i, card in enumerate(player2.hand):
        screen.blit(card.image, (500 + i * 200, 20))
     
    # Draw life point scales
    draw_life_scale(player1, 50, SCREEN_HEIGHT - 50)
    draw_life_scale(player2, 50, 30)

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


