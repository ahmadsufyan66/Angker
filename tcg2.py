import random

class Card:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense

class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []  # List of Card objects
        self.hand = []  # List of Card objects
        self.life_points = 8000  # Starting life points

    def draw_card(self):
        if self.deck:
            card = self.deck.pop()
            self.hand.append(card)
            print(f"{self.name} draws {card.name} (Attack: {card.attack}, Defense: {card.defense}).")
        else:
            print("Deck is empty. Cannot draw a card.")

    def play_card(self, card_index, opponent):
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            print(f"{self.name} plays {card.name} (Attack: {card.attack}, Defense: {card.defense}).")
            if card.attack > opponent.life_points:
                opponent.life_points = 0
            else:
                opponent.life_points -= card.attack
            print(f"{opponent.name} has {opponent.life_points} life points remaining.")
            return card
        print(f"{self.name} doesn't have a card at index {card_index}.")
        return None

#def initialize_deck():
    # Create and return a list of Card objects representing a deck
    #deck = []
    #for i in range(1, 6):
     #   card_name = f"Monster {i}"
      #  attack = random.randint(500, 1000)
       # defense = random.randint(500, 1000)
        #card = Card(card_name, attack, defense)
        #deck.append(card)
    #return deck

# Initialize players
player1 = Player("Player 1")
player2 = Player("Player 2")

# Populate decks with custom and random monsters
custom_hantu1 = Card("Langsuir", 1500, 1200)
custom_hantu2 = Card("Toyol", 1800, 1000)
custom_hantu3 = Card("Saka", 3000, 0)
player1.deck.extend([custom_hantu1, custom_hantu2, custom_hantu3])
player2.deck.extend([custom_hantu1, custom_hantu2, custom_hantu3])

# Game loop
while True:
    # Player 1's turn
    print("\nPlayer 1's turn:")
    player1.draw_card()
    player1.draw_card()
    
    print("\nPlayer 1's hand:")
    for i, card in enumerate(player1.hand):
        print(f"{i+1}. {card.name}")
    
    card_to_play_index = int(input("Select a card to play (enter index): ")) - 1
    played_card = player1.play_card(card_to_play_index, player2)
    if played_card:
        if player2.life_points <= 0:
            print("Player 1 wins!")
            break
    
    # Player 2's turn
    print("\nPlayer 2's turn:")
    player2.draw_card()
    player2.draw_card()
    
    print("\nPlayer 2's hand:")
    for i, card in enumerate(player2.hand):
        print(f"{i+1}. {card.name}")
    
    card_to_play_index = int(input("Select a card to play (enter index): ")) - 1
    played_card = player2.play_card(card_to_play_index, player1)
    if played_card:
        if player1.life_points <= 0:
            print("Player 2 wins!")
            break
