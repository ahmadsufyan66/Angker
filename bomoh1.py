import pygame
import sys
import random
from subprocess import call

# Initialize Pygame
pygame.init()

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
        self.trigger_deck = []
        self.hand = []
        self.trigger_hand = []
        self.life_points = 80

    #------------------------------------------#
    def shuffle(self, num=1):

        #Shuffle normal card deck
        length = len(self.deck)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.deck[i], self.deck[randi] = self.deck[randi], self.deck[i]

        #Shuffle trigger card deck
        length = len(self.trigger_deck)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.trigger_deck[i], self.trigger_deck[randi] = self.trigger_deck[randi], self.trigger_deck[i]
    #------------------------------------------#

    def draw_card(self, num=1):
        if self.deck:
            card = self.deck.pop()
            self.hand.append(card)

        if self.trigger_deck:
            card = self.trigger_deck.pop()
            self.trigger_hand.append(card)

    def play_card(self, card_index, opponent):
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            if card.attack > opponent.life_points:
                opponent.life_points = 0
            else:
                opponent.life_points -= card.attack
            return card
        return None
    
    #Trigger card play function
    def play_trigger_card(self, card_index, opponent):
        if 0 <= card_index < len(self.trigger_hand):
            if card.attack == 2:
                opponent.life_points -= card.attack
            elif card.defense == 2:
                for i, card in random.randrange(len(opponent.hand)):
                    opponent.card.attack -= card.defense
            else:
                self.life_points += card.attack
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

##Create attacking area
rect_1 = pygame.Rect(0, 170, SCREEN_WIDTH, 490)

# Load card images
card_images = ["card_images/trigger_atk.jpg", "card_images/trigger_def.jpg", "card_images/trigger_heal.jpg",
               "card_images/Card1.png", "card_images/Card2.png", "card_images/Card3.png", "card_images/Card4.png", "card_images/Card5.png"]

# Customize attack and defense for each card
cards_data = [{"name": "Trigger Attack", "attack": 2, "defense": 0, "image": card_images[0]}, 
              {"name": "Trigger Defense", "attack": 0, "defense": 2, "image": card_images[1]}, 
              {"name": "Trigger Heal", "attack": 2, "defense": 0, "image": card_images[2]},
              {"name": "Card 1", "attack": 8, "defense": 7, "image": card_images[3]},
              {"name": "Card 2", "attack": 10, "defense": 9, "image": card_images[4]},
              {"name": "Card 3", "attack": 12, "defense": 11, "image": card_images[5]},
              {"name": "Card 4", "attack": 12, "defense": 11, "image": card_images[6]},
              {"name": "Card 5", "attack": 12, "defense": 11, "image": card_images[7]},
              
]

# Populate decks with custom cards
for card_data in cards_data[3:]:
    player1.deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))
    player2.deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))

#Populate trigger card decks
for card_data in cards_data[0:3]:
    player1.trigger_deck.append(Card(card_data["name"], card_data["attack"], card_data["defense"], card_data["image"]))

#Shuffle deck
player1.shuffle()
player2.shuffle()

#Drag and drop function
boxes = []
images = []

for i in range(len(card_images)):
    temp_img = pygame.image.load(card_images[i]).convert_alpha()
    image = pygame.transform.scale(temp_img, (100,100))
    object_rect = image.get_rect()
    boxes.append(object_rect)
    images.append(card_images)

active_box = None

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
            if event.key == pygame.K_SPACE and turn_counter < 3:  # Only draw cards for the first three spacebar presses
                player1.draw_card()
                player2.draw_card()
                turn_counter += 1  # Increment turn counter
                print(f"{player1.name} and {player2.name} draw a card.")
            elif event.key == pygame.K_SPACE and turn_counter == 3:  # On the fourth spacebar press, allow player 1 to play a card
                player1_turn = True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player1.name == "Player 1" and player1_turn:
                for num, box in enumerate(boxes):
                    if box.collidepoint(event.pos):
                        active_box = num
                for i, card in enumerate(player1.hand):
                    if card.rect.collidepoint(event.pos):
                        card.is_dragging = True

        if event.type == pygame.MOUSEMOTION:
            if active_box != None:
                boxes[active_box].move_ip(event.rel)
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if player1.name == "Player 1" and player1_turn:  # Only play card if it's player 1's turn
                #Check collision
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
                
                        #Choosing trigger card
                        for i, card in enumerate(player1.trigger_hand):
                            if card.is_dragging:
                                card.is_dragging = False
                                card.rect.center = (50 + i * 120 + 50, SCREEN_HEIGHT - 170)  # Reset card position
                                played_trigger_card = player1.play_trigger_card(i, player2)
                                if played_trigger_card:
                                    print(f"{player1.name} plays {played_trigger_card.name}.")
                                    print(f"{player2.name} has {player2.life_points} life points remaining.")
                                player1_turn = False  # End player 1's turn
                            


    # AI player's turn
    if not player1_turn and turn_counter == 3:  # Only let AI play after player 1's turn and all cards have been drawn
        played_card = player2.ai_play(player1)
        if played_card:
            print(f"{player2.name} plays {played_card.name}.")
            print(f"{player1.name} has {player1.life_points} life points remaining.")
        player1_turn = True  # End AI player's turn

    # Draw background
    screen.fill(WHITE)
    
    #Attacking area
    pygame.draw.rect(screen, (255, 0, 0), rect_1)

    # Draw player 1's hand
    for i, card in enumerate(player1.hand):
        card.rect.bottomleft = (50 + i * 120, SCREEN_HEIGHT)  # Adjust card position
        screen.blit(card.image, card.rect)

    for i, card in enumerate(player1.trigger_hand):
        card.rect.bottomright = (700 + i * 120, SCREEN_HEIGHT)  # Adjust card position
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