'''
A game of blackjack developed using Python
'''

STARTING_AMOUNT = 0

class Bankroll():
    '''
    Class to keep count of the chips available to the player
    '''

    def __init__(self, total=100, bet=0):
        self.total = total # 200
        self.bet = bet # 100

        print('Your total amount is ', self.total)
        print('You bet ', self.bet)


    def check_bankroll(self):
        if self.bet > self.total:
            return True
        else:
            self.total = self.total - self.bet # 200-100=100
            print('Your total amout after deducting the betting amount is ', self.total)
            return False

    def win_bet(self, blackjack=False):
        # A blackjack win pays 3:2, a non-blackjack win pays 1:1
        if blackjack:
            win = self.bet + 1.5 * self.bet # 100+150=250
            print('You won ', win)
            self.total = self.total + win # 100+250=350
            print('Your total amout after winning this hand is ', self.total)
            self.bet = 0
        else:
            win = self.bet + self.bet # 100+100=200
            print('You won ', win)
            self.total = self.total + win # 100+200=300
            print('Your total amout after winning this hand is ', self.total)
            self.bet = 0

    def lose_bet(self):
        print('Your total after losing this hand is ', self.total)
        self.bet = 0

    def push_bet(self):
        self.total = self.total + self.bet # 100+100=200
        print('Total after push remains equal to the previous total ', self.total)
        self.bet = 0
