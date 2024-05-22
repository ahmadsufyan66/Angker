import pygame
import sys
import random
# Initialize Pygame
pygame.init()

#font
font = pygame.font.Font('GOODDC__.TTF', 40)

#dialogue
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

# Screen dimensions
SCREEN_WIDTH = 1535
SCREEN_HEIGHT = 810

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
    def __init__(self, name, is_human):
        self.name = name
        self.is_human = is_human
        self.deck = []
        self.hand = []
        self.life_points = 8000

    #------------------------------------------#
    def shuffle(self, num=1):
        length = len(self.deck)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.deck[i], self.deck[randi] = self.deck[randi], self.deck[i]
    #------------------------------------------#

    def draw_card(self, num=1):
        if self.deck:
            for _ in range(3):
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
    
    def ai_play(self, opponent):
        if self.hand:
            card_index = random.randint(0, len(self.hand) - 1)
            return self.play_card(card_index, opponent)
        return None

# Create display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TCG Game')

# Create players
player1 = Player("Player 1",True)#human
player2 = Player("Player 2",False)#ai

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

#Shuffle deck
player1.shuffle()
player2.shuffle()

# Game loop
running = True
turn_counter = 0  # Initialize turn counter
player1_turn = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and turn_counter < 1:  # Only draw cards for the first three spacebar presses
                player1.draw_card()
                player2.draw_card()
                turn_counter += 1  # Increment turn counter
                print(f"{player1.name} and {player2.name} draw a card.")
            elif event.key == pygame.K_SPACE and turn_counter == 1:  # On the fourth spacebar press, allow player 1 to play a card
                player1_turn = True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player1.name == "Player 1" and player1_turn:
                for i, card in enumerate(player1.hand):
                    if card.rect.collidepoint(event.pos):
                        card.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if player1.name == "Player 1" and player1_turn:  # Only play card if it's player 1's turn
                for i, card in enumerate(player1.hand):
                    if card.is_dragging:
                        card.is_dragging = False
                        card.rect.center = (50 + i * 120 + 50, SCREEN_HEIGHT - 170)  # Reset card position
                        played_card = player1.play_card(i, player2)
                        if played_card:
                            print(f"{player1.name} plays {played_card.name}.")
                            print(f"{player2.name} has {player2.life_points} life points remaining.")
                        player1_turn = False  # End player 1's turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and done and active_message < len(messages) - 1:
                active_message += 1
                done = False
                message = messages[active_message]
                counter = 0

    snip = font.render(message[0:counter//speed], True, 'dark red')
    screen.blit(snip, (310, 600))

    # AI player's turn
    if not player1_turn and turn_counter == 1:  # Only let AI play after player 1's turn and all cards have been drawn
        played_card = player2.ai_play(player1)
        if played_card:
            print(f"{player2.name} plays {played_card.name}.")
            print(f"{player1.name} has {player1.life_points} life points remaining.")
        player1_turn = True  # End AI player's turn

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
























