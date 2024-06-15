import pygame
pygame.init()
import random

# Define player class

# Load sound effects
sound_cardplay = pygame.mixer.Sound('Sound/sound_cardplay.mp3')

class Player:
    def __init__(self, name, is_human, initial_life_points, aggressiveness=0.7):
        self.name = name
        self.is_human = is_human
        self.deck = []
        self.skill_deck = []
        self.hand = []
        self.life_points = 100
        self.initial_life_points = 100
        self.additional_play = False  # Flag to allow an additional card play
        self.half_next_attack = False  # Flag to indicate if the next attack should be halved
        self.aggressiveness = aggressiveness

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
            attack_points = card.attack
            print(f"Playing card: {card.name}")
            print(f"Initial attack points: {attack_points}")
            print(f"Opponent's half_next_attack flag: {opponent.half_next_attack}")

            # Play sound effect
            sound_cardplay.play()

            # Apply halving effect if the flag is set
            if self.half_next_attack:
                attack_points //= 2
                self.half_next_attack = False  # Reset the flag after applying the effect
                print(f"Attack points after halving: {attack_points}")

            # Update attack points if it's a Freddy Krueger (skill) card
            if card.name == "Freddy Krueger (skill)":
                lost_life_points = self.initial_life_points - self.life_points
                attack_points += lost_life_points  # Increase attack based on lost life points
                print(f"Freddy Krueger attack points with lost life points: {attack_points}")

            # Update attack points if it's a Saka (skill) card
            if card.name == "Saka (skill)":
                lost_life_points = self.initial_life_points - self.life_points
                attack_points += lost_life_points  # Increase attack based on lost life points
                print(f"Saka attack points with lost life points: {attack_points}")


            # Apply attack to opponent's life points
            if attack_points > opponent.life_points + card.defense:
                opponent.life_points = 0
            else:
                opponent.life_points -= attack_points

            print(f"Opponent's remaining life points: {opponent.life_points}")

            # Check for other card skills
            if card.name == "Kappa (skill)":
                print(f"{self.name} +10 HP")
                self.life_points += 10
                print(f"{self.name} has {self.life_points} remaining.")
            
            elif card.name == "Pocong (skill)":
                print(f"{opponent.name}'s next attack will be halved!")
                opponent.half_next_attack = True  # Set the flag for halving the next attack
                print(f"Set opponent's half_next_attack flag to: {opponent.half_next_attack}")

            elif card.name == "Toyol (skill)":
                print(f"{opponent.name}'s next attack will be halved!")
                opponent.half_next_attack = True  # Set the flag for halving the next attack
                print(f"Set opponent's half_next_attack flag to: {opponent.half_next_attack}")

            elif card.name == "Pontianak (skill)":
                print(f"{self.name} gains another turn!")
                self.additional_play = True

            return card
        return None


    def ai_play(self, opponent):
        if not self.hand:
            return None

        # Calculate the probability threshold for choosing the highest attack card
        threshold = 1 / self.aggressiveness

        if random.random() < threshold:
            # Choice 1: Play a random card from the hand
            card_index = random.randint(0, len(self.hand) - 1)
        else:
            # Choice 2: Play the card with the highest attack value
            card_index = max(range(len(self.hand)), key=lambda i: self.hand[i].attack)

        return self.play_card(card_index, opponent)
