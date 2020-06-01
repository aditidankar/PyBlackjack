'''
A game of blackjack developed using Python
'''

import random

print('\nWelcome to Blackjack!')

class Bankroll():
    '''
    Class to keep count of the chips available to the player
    '''

    def __init__(self, total=100, bet=0):
        self.total = total # 200
        self.bet = bet # 100

    def check_bankroll(self):
        # Checks whether the betting amount is valid
        if self.bet > self.total:
            print('Your betting amount cannot be greater than your total amount', self.total)
            return True
        else:
            self.total = self.total - self.bet # 200-100=100
            print('\nYour betting amount is', self.bet)
            print('Your remaining amout after deducting the betting amount is', self.total)
            return False

    def win_bet(self, blackjack=False):
        # When the player wins the hand
        # A blackjack win pays 3:2, a non-blackjack win pays 1:1
        if blackjack:
            win = self.bet + 1.5 * self.bet # 100+150=250
            print('\nYou won', win)
            self.total = self.total + win # 100+250=350
            print('Your total amout after winning this hand is', self.total)
            self.bet = 0
        else:
            win = self.bet + self.bet # 100+100=200
            print('\nYou won', win)
            self.total = self.total + win # 100+200=300
            print('Your total amout after winning this hand is', self.total)
            self.bet = 0

    def lose_bet(self):
        # When the player loses the hand
        print('\nYou lost', self.bet)
        print('Your total after losing this hand is', self.total)
        self.bet = 0

    def push_bet(self):
        # When both the player and the dealer has same hands
        self.total = self.total + self.bet # 100+100=200
        print('\nTotal after push remains equal to the previous total', self.total)
        self.bet = 0


class Cards():
    '''
    This class contains the suits and ranks
    '''

    def __init__(self):
        self.suits = ('Spades \u2660', 'Hearts \u2665', 'Diamonds \u2666', 'Clubs \u2663')
        self.ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
        self.values = {
        'Two':2, 'Three':3, 'Four':4, 'Five':5,
        'Six':6, 'Seven':7, 'Eight':8, 'Nine':9,
        'Ten':10, 'Jack':10, 'Queen':10, 'King':10,
        'Ace':11
        }

    def __str__(self):
        # Prints a random card from the deck when print statement is used on the class
        return random.choice(self.ranks) + ' of ' + random.choice(self.suits)


class Deck():
    '''
    This class instantiates a deck of 52 Cards
    '''

    def __init__(self):
        self.card = Cards()
        self.deck = []

        # Forms a deck of 52 cards
        for suit in self.card.suits:
            for rank in self.card.ranks:
                self.deck.append(rank + ' of ' + suit )

    def __str__(self):
        return "This is a deck of 52 cards"

    def shuffle(self):
        # Shuffles the deck
        random.shuffle(self.deck)


class Deal():
    '''
    This class deals the cards to the dealer and the player
    '''

    def __init__(self):
        self.deck_of_cards = Deck()
        self.deck_of_cards.shuffle()

    def deal_card(self):
        # Removes the first card from the shuffled deck whenever there is a draw
        try:
            return self.deck_of_cards.deck.pop()
        except:
            print('\nNo more cards left!')
