import random
import time
class User:
    def __init__(self):
        self.currency = 0

    def display_status(self):
        print(f"Current fake currency: {self.currency} coins")

    def add_currency(self, amount):
        self.currency += amount


def display_commands():
    print("thanks for playing our game. here's a list of available commands:")
    print("2. grind - Grind to stand a chance to win some cash (totally worth it!).")

card = club,heart

class FakeCardGrinder:
    def __init__(self, user):
        self.user = user

    def grind_for_card(self):
        print("randomising...")
        time.sleep(2)
        earned_card = random.randint(card)
        print(f"Bravo, my dear friend. You earned {earned_card} card!")

def grind_for_card(user):
    grinder = FakeCardGrinder(user)
    grinder.user.display_status()
    grinder.grind_for_card()

def display_currency(user):
    user.display_status()

if __name__ == "__main__":
    user = User()
    while True:
        display_commands()
        user_input = input("Enter a command: ").lower()

        if user_input == 'grind': 
            grind_for_card(user)  
