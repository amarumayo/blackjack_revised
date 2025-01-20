import random
import sys
import time
import os

class Card:
    # card class
    def __init__(self, rank, suit):

        if rank not in [
            '1', '2', '3', '4', '5', '6',
            '7', '8', '9', '10', 'A', 'J', 'Q', 'K']:
                raise ValueError("Invalid rank")

        valid_suits = ['D', 'S', 'C', 'H']
        if suit not in valid_suits:
            raise ValueError(f"Invalid suit. Valid suits are {valid_suits}")

        self.suit = suit
        self.rank = rank

    # unicode value to print suit symbols
    suit_lu = {
        "C": "\u2663",
        "H": "\u2665",
        "D": "\u2666",
        "S": "\u2660"
    }    
    
    def __repr__(self):
        rep = f"Card('{self.rank}', '{self.suit}')"
        return rep

    def __str__(self):
        string = "".join((str(self.rank), self.suit_lu[self.suit]))
        return string
       
class Deck():
    def __init__(self):
        self.cards = []
        self.fill_deck()
        self.shuffle()

    def fill_deck(self):
        suits = ["C", "D", "S", "H"]    
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [Card(r, s) for r in ranks for s in suits]
        
    def clear_deck(self):
        self.cards = []

    def shuffle(self):
        return random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop(0)

    def __str__(self):
        num_remaining = f"Cards Remaining: {len(self.cards)}"
        next_card =  f"Next Card: {str(self.cards[0])}"  
        return num_remaining + '\n' + next_card

    def __repr__(self):
        return f'Deck({self.cards})'


class Hand:

    def __init__(self, is_dealer, is_active = False):
        self.cards = []
        self.is_dealer = is_dealer
        self.is_active = is_active

    def add_card(self, card):
        self.cards.append(card)

    def clear(self):
        self.cards = []

    @property
    def has_blackjack(self):
        blackjack = False
        if len(self.cards) == 2 and self.value == 21:
            blackjack = True
        return(blackjack)

    @property
    def is_bust(self):
        bust = False
        if self.value > 21:
            bust = True
        return(bust)

    @property
    def value(self):
        '''Calculate the value of the cards in a hand instance'''
        val = 0
        num_aces = 0

        for card in self.cards:
            if card.rank.isnumeric():
                val += int(card.rank)
            elif card.rank == "A":
                num_aces += 1
                val += 11
            else:
                val += 10
        while num_aces > 0 and val > 21:
            val -= 10
            num_aces -= 1

        return val

    def show(self, dealer_hide = False):
        
        if self.is_dealer:
            if dealer_hide:
                print(f'Dealer: X, {", ".join(str(card) for card in self.cards[1:])}')
            else:
                print(f'Dealer: {", ".join(str(card) for card in self.cards)}')
        else:
            print(f'Player: {", ".join(str(card) for card in self.cards)}')

    def player_choice(self, deck):
        '''Prompt player to hit or stand with a hand instance'''

        answer = ''
        while answer not in ['h', 's']:
            answer = input("Hit or Stand? H/S: ")
            if answer.lower() == "h":
                print("Player hits...")
                self.add_card(deck.deal())
                time.sleep(2)
            if answer.lower() == "s":
                print(f"Player stands with hand of {str(self.value)}\n")
                self.is_active = False
                time.sleep(2)

    def __repr__(self):
        return f'Hand({self.cards}, {self.is_dealer}, {self.is_active})'

    def __str__(self):
        num_cards = f'Number of cards in hand: {len(self.cards)}'
        value = f'Hand value: {str(self.value)}'
        return(num_cards + '\n' + value)

    

class Game:
    
    def __init__(self):
        self.deck = Deck()
        self.player = Hand(is_dealer = False, is_active = None)
        self.dealer = Hand(is_dealer = True)
        self.game_active = True

    def check_winner(self):
        if self.dealer.value >= self.player.value:
            print(f'You lose with {str(self.player.value)}. Dealer has {str(self.dealer.value)}')
        else: 
            print(f'You win with {str(self.player.value)}. Dealer has {str(self.dealer.value)}')

    def end(self):
        print("Goodbye")
        sys.exit()
        
    def play(self):
        
        def clear_console():
            """Clears the console."""
            command = 'cls' if os.name in ('nt', 'dos') else 'clear'
            os.system(command)

        while (self.game_active):
            
            clear_console()

            # clear hands, shuffle and set player turn each time we play
            self.deck.clear_deck()
            self.deck.fill_deck()
            self.deck.shuffle()
            self.player.clear()
            self.dealer.clear()
            self.player.is_active = True

            # deal 2 cards to each player
            for _ in range(2):
                for p in [self.dealer, self.player]:
                    # p = player
                    p.add_card(self.deck.deal())

            
            # check for any blackjacks
            if self.dealer.has_blackjack:
                self.player.show()
                self.dealer.show()
                print('Dealer has blackjack. You Lose.')
                self.player.is_active = False
                time.sleep(2)
    
            if self.player.has_blackjack and self.player.is_active:
                self.player.show()
                self.dealer.show()
                print('Player has blackjack! You win!')
                self.player.is_active = False
                time.sleep(2)
                
            while self.player.is_active:
                
                # show both hands:
                self.player.show()
                self.dealer.show(dealer_hide = True)
                self.player.player_choice(deck = self.deck)

                if self.player.is_bust:
                    self.player.show()
                    print(f"Player busts with {str(self.player.value)}. You lose!")
                    self.player.is_active = False
            
            if not self.player.is_bust \
                and not self.player.has_blackjack \
                    and not self.dealer.has_blackjack:
                
                # dealer turn
                self.dealer.is_active = True
                while self.dealer.is_active:

                    while self.dealer.value <= 16 and \
                        not self.dealer.is_bust:
                        
                        print("Dealer hits...")
                        self.dealer.add_card(self.deck.deal())
                        self.dealer.show()
                        time.sleep(2)

                        if self.dealer.is_bust:
                            print(f"Dealer busts with {str(self.dealer.value)}. You win!")
                            self.dealer.is_active = False

                    if not self.dealer.is_bust:
                         print(f"Dealer stands with hand of {str(self.dealer.value)}\n")
                    
                    # end dealer turn
                    self.dealer.is_active = False

                # evaluate hands if the game is still going   
                if not self.dealer.is_active and \
                    not self.player.is_active and \
                    not self.player.is_bust and \
                    not self.dealer.is_bust:
                    self.check_winner()   
            
            
            answer = ''
            while answer not in ['y', 'n']:
                answer = input("Play again? Y/N:")

                if answer.lower() == 'n':
                    self.game_active = False
                    self.end()



        


             



        # deck = Deck()
        # deck.fill_deck()
        # deck.shuffle()