import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return f"{self.value} of {self.suit}"
    
class Deck:
    def __init__(self):
        self.cards = []
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for value in range(2, 11):
                self.cards.append(Card(suit, str(value)))
            for value in ["J", "Q", "K", "A"]:
                self.cards.append(Card(suit, value))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self):
        return self.cards.pop()
    
class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def get_value(self):
        value = 0
        num_aces = 0
        for card in self.cards:
            if card.value in ["J", "Q", "K"]:
                value += 10
            elif card.value == "A":
                num_aces += 1
                value += 11
            else:
                value += int(card.value)
        
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        
        return value
    
    def __str__(self):
        return ", ".join(str(card) for card in self.cards)

class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
    
    def play(self):
        print("Welcome to Blackjack!")
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        
        print(f"Player's hand: {self.player_hand}")
        print(f"Dealer's hand: {self.dealer_hand.cards[0]}")
        
        while True:
            player_value = self.player_hand.get_value()
            if player_value == 21:
                print("Blackjack! You win!")
                return
            elif player_value > 21:
                print("Bust! You lose.")
                return
            
            choice = input("Do you want to hit or stand? ")
            if choice.lower() == "hit":
                self.player_hand.add_card(self.deck.deal())
                print(f"Player's hand: {self.player_hand}")
            elif choice.lower() == "stand":
                break
        
        dealer_value = self.dealer_hand.get_value()
        while dealer_value < 17:
            self.dealer_hand.add_card(self.deck.deal())
            dealer_value = self.dealer_hand.get_value()
        print(f"Dealer's hand: {self.dealer_hand}")
        
        if dealer_value > 21:
            print("Dealer busts! You win!")
        elif dealer_value > player_value:
            print("Dealer wins!")
        elif player_value > dealer_value:
            print("You win!")
        else:
            print("It's a tie!")
        
game = Blackjack()
game.play()