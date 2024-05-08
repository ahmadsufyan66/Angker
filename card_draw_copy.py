import random

#Classes to determine attributes
class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

class Character: #add opponent class
    def __init__(self,
                 name: str,
                 health: int,
                 atk: int,
                 ) -> None:
        self.name = name
        self.health = health
        self.health_max = health

    def attack(self, target) -> None:
        target.health -= self.atk
        target.health = max(target.health, 0)
        
    def heal(self, target) -> None:
        target.health += self.potion.points #trigger card heal points
        target.health = max(target.health, 0)

    def defend(self, target) -> None:
        self.health = target.atk + 1#trigger card defend points 
        target.health = max(target.health, 0)

class Opponent: #add opponent class
    def __init__(self,
                 name: str,
                 health: int,
                 atk: int,
                 ) -> None:
        self.name = name
        self.health = health
        self.health_max = health

    def attack(self, target) -> None:
        target.health -= self.atk
        target.health = max(target.health, 0)
        
    def heal(self, target) -> None:
        target.health += self.potion.points #trigger card heal points
        target.health = max(target.health, 0)

    def defend(self, target) -> None:
        self.health = target.atk + 1#trigger card defend points 
        target.health = max(target.health, 0)


    # Implementing build in methods so that you can print a card object
    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()
        
    def show(self):
        if self.value == 1:
            val = "Ace"
        elif self.value == 11:
            val = "Jack"
        elif self.value == 12:
            val = "Queen"
        elif self.value == 13:
            val = "King"
        else:
            val = self.value

        return "{} of {}".format(val, self.suit)


class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    # Display all cards in the deck
    def show(self):
        for card in self.cards:
            print(card.show())

    # Generate 52 cards
    def build(self):
        self.cards = []
        for suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
            for val in range(1, 14):
                self.cards.append(Card(suit, val))

    # Shuffle the deck
    def shuffle(self, num=1):
        length = len(self.cards)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.cards[i], self.cards[randi] = self.cards[randi], self.cards[i]
            # You can also use the build in shuffle method
            # random.shuffle(self.cards)

    # Return the top card
    def deal(self):
        return self.cards.pop()


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []

    def sayHello(self):
        print("Hi! My name is {}".format(self.name))
        return self

    # Draw n number of cards from a deck
    # Returns true in n cards are drawn, false if less then that
    def draw(self, deck, num=1):
        for _ in range(num):
            card = deck.deal()
            if card:
                self.hand.append(card)
            else: 
                return False
        return True

    # Display all the cards in the players hand
    def showHand(self):
        print("{}'s hand: {}".format(self.name, self.hand))
        return self

    def discard(self):
        return self.hand.pop()

#Attribute customization (health subjected to change)
mc = You(name="You", health=10)

bomoh = Bomoh(name="Bomoh", health=5, weapon=dagger)

# Test making a Card
# card = Card('Spades', 6)
# print card

# Test making a Deck
myDeck = Deck()
myDeck.shuffle()
# deck.show()

aqil = Player("Aqil")
aqil.sayHello()
aqil.draw(myDeck, 5)
aqil.showHand()
