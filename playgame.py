from blackjack import Bankroll
from blackjack import Cards
from blackjack import Deck
from blackjack import Deal

STARTING_AMOUNT = 0
FINAL_AMOUNT = 0

class Play():
    """
    Class to play the game
    """

    def __init__(self):
        self.deal = Deal()
        self.get_total()
        self.play_hand()

    def get_total(self):
        # Gets the total amout you want to play with
        print('\nWhat is your total amout?')
        while True:
            try:
                self.total = int(input('Please enter the total amount: '))
                self.bankroll = Bankroll(total=self.total)
                break
            except:
                print('Your input is not valid!')

        global STARTING_AMOUNT
        STARTING_AMOUNT = self.total

    def play_hand(self):
        # Fuctions that plays each hand or each round until the cards or the total amount is exhausted
        self.betting = True

        self.player_cards = []
        self.player_points = 0
        self.player_aces = 0
        self.player_ace_deduction = 0

        self.dealer_cards = []
        self.dealer_points = 0
        self.dealer_aces = 0
        self.dealer_ace_deduction = 0

        if len(self.deal.deck_of_cards.deck) > 0:
            self.take_bet()

            for i in range(0, 2):
                if len(self.deal.deck_of_cards.deck) == 0:
                    break
                self.players_draw()
                self.dealers_draw()

            self.blackjack_win()

        while len(self.deal.deck_of_cards.deck) > 0:
            # If the player wants to hit, the player draws the cards
            # If the player wants to stand, the dealer draws the cards
            try:
                self.hit_or_stand = input("\nDo you want to hit or stand?\nPlease enter 'hit' or 'h' for hitting and 'stand' or 's' for standing: ").lower()
            except:
                print('Invalid input!')
                continue
            else:
                if self.hit_or_stand not in ['h', 'hit', 's', 'stand']:
                    print('Invalid input!')
                    continue

                if self.hit_or_stand == 'hit' or self.hit_or_stand == 'h':
                    if len(self.deal.deck_of_cards.deck) == 0:
                        break
                    self.players_draw()
                else:
                    # The dealer draws for any points of 16 or less and stands for any value of 17 or more
                    while self.dealer_points <= 16:
                        if len(self.deal.deck_of_cards.deck) == 0:
                            break
                        self.dealers_draw(stand=True)

                    self.check_win()
                    break

        else:
            self.final_result()

    def take_bet(self):
        # Gets the amount that you want to bet
        self.total = self.bankroll.total # To make the total amount same in both the modules

        self.check_total()

        exitorquit = input('\nDo you want to proceed/continue with the game?\nIf yes, please press the enter key. If no, enter quit or exit!\n').lower()
        if exitorquit == 'exit' or exitorquit == 'quit':
            self.final_result()
            quit()
        print('How much do you want to bet?')
        while self.betting:
            try:
                self.bet = int(input('Please enter the betting amount: '))
            except:
                print('Your input is not valid!')
            else:
                self.bankroll = Bankroll(total=self.total, bet=self.bet)
                self.betting = self.bankroll.check_bankroll()

    def check_total(self):
        # Function to check whether the player has exhausted all the amount that they began the game with
        if self.bankroll.total == 0:
            print("\nYou've lost all the money that you bet. You can't bet any further!")
            self.final_result()
            replay_game = input("\nDo you want to play again?\nEnter 'yes' or 'y' if you want to replay!\n").lower()
            if replay_game == 'yes' or replay_game == 'y':
                print('\nRestarting the game...\n')
                play = Play()
            else:
                print("You did not enter 'yes', quitting the game!\n")
                quit()

    def players_draw(self):
        # Function to draw and print cards for the dealer and to calculate the points
        self.current_player_card = self.deal.deal_card()
        self.player_cards.append(self.current_player_card)

        print("\nThe player's cards are: ")
        for card in self.player_cards:
            print(card)

        if len(self.player_cards) == 2:
            self.player_blackjack = self.check_blackjack(self.player_cards)
            if self.player_blackjack:
                print('\nPlayer has a Blackjack')

        suit = self.current_player_card.split()
        score = self.deal.deck_of_cards.card.values

        if suit[0] == 'Ace':
            self.player_aces += 1

        if suit[0] in score.keys():
            self.player_points += score[suit[0]]
            if self.player_points > 21 and self.player_aces > self.player_ace_deduction:
                self.player_points -= 10
                self.player_ace_deduction += 1
            print("Player's score is", self.player_points)
            self.player_busts()

    def dealers_draw(self, stand=False):
        # Function to draw and print cards for the dealer and to calculate the points
        self.current_dealer_card = self.deal.deal_card()
        self.dealer_cards.append(self.current_dealer_card)

        if len(self.dealer_cards) == 1:
            print("\nDealer's first card:", self.dealer_cards[0])

        if len(self.dealer_cards) == 2:
            print("\nDealer's second card is hidden")
            self.dealer_blackjack = self.check_blackjack(self.dealer_cards)
            if self.dealer_blackjack:
                print('\nDealer has a Blackjack')
                print("Dealer's second card:", self.dealer_cards[1])

        if stand:
            print("\nThe dealer's cards are: ")
            for card in self.dealer_cards:
                print(card)

        suit = self.current_dealer_card.split()
        score = self.deal.deck_of_cards.card.values

        if suit[0] == 'Ace':
            self.dealer_aces += 1

        if suit[0] in score.keys():
            self.dealer_points += score[suit[0]]
            if self.dealer_points > 21 and self.dealer_aces > self.dealer_ace_deduction:
                self.dealer_points -= 10
                self.dealer_ace_deduction += 1

            if len(self.dealer_cards) > 2:
                print("Dealer's score is", self.dealer_points)

            self.dealer_busts()

    def check_blackjack(self, received_cards):
        # Checks if either the dealer or the player has a blackjack
        suit1 = received_cards[0].split()
        suit2 = received_cards[1].split()
        if suit1[0] == 'Ace' and suit2[0] in ['King', 'Queen', 'Jack', 'Ten'] or suit2[0] == 'Ace' and suit1[0] in ['King', 'Queen', 'Jack', 'Ten']:
            return 'blackjack'
        else:
            return None

    def blackjack_win(self):
        # Checks blackjack winning conditions
        if self.player_blackjack == 'blackjack' and self.dealer_blackjack == 'blackjack':
            print('\nBoth the player and the dealer has blackjack, this hand is a push')
            self.bankroll.push_bet()
            self.play_hand()
        elif self.player_blackjack == 'blackjack':
            print("\nDealer's second card:", self.dealer_cards[1])
            print('\nPlayer wins this hand')
            self.bankroll.win_bet(blackjack=True)
            self.play_hand()
        elif self.dealer_blackjack == 'blackjack':
            print('\nDealer wins this hand')
            self.bankroll.lose_bet()
            self.play_hand()
        else:
            pass

    def player_busts(self):
        # Checks whether player goes over 21
        if self.player_points > 21:
            print('\nPlayer busts')
            self.bankroll.lose_bet()
            self.play_hand()

    def dealer_busts(self):
        # Checks whether dealer goes over 21
        if self.dealer_points > 21:
            print('\nDealer busts')
            self.bankroll.win_bet()
            self.play_hand()

    def check_win(self):
        # Checks non-blackjack winning conditions
        if self.player_points == self.dealer_points:
            print('\nBoth the player and the dealer has equal points, this hand is a push')
            self.bankroll.push_bet()
            self.play_hand()
        elif self.player_points > self.dealer_points:
            if len(self.dealer_cards) == 2:
                print("\nDealer's second card:", self.dealer_cards[1])
            print('\nPlayer wins this hand')
            self.bankroll.win_bet()
            self.play_hand()
        else:
            print('\nDealer wins this hand')
            self.bankroll.lose_bet()
            self.play_hand()

    def final_result(self):
        # Final result of the game, when the player quits or when the entire deck has been drawn
        global FINAL_AMOUNT
        FINAL_AMOUNT = self.bankroll.total

        if FINAL_AMOUNT > STARTING_AMOUNT:
            print('\nYour starting amount was', STARTING_AMOUNT)
            print('Your final amout is', FINAL_AMOUNT)
            self.difference = FINAL_AMOUNT - STARTING_AMOUNT
            print('\nCongratulations, you won', self.difference)
            print('\n')
        else:
            print('\nYour starting amount was', STARTING_AMOUNT)
            print('Your final amout is', FINAL_AMOUNT)
            self.difference = STARTING_AMOUNT - FINAL_AMOUNT
            print('\nSorry, you lost', self.difference)
            print('\n')

play = Play()
