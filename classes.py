import random
import sys
import time

class Card:
    # card class
    def __init__(self, rank, suit):

        if rank not in [
            '1', '2', '3', '4', '5', '6',
            '7', '8', '9', '10', 'A', 'J', 'Q', 'K', 'X']:
                raise ValueError("Invalid rank")

        valid_suits = ['D', 'S', 'C', 'H', 'X']
        if suit not in valid_suits:
            raise ValueError(f"Invalid suit. Valid suits are {valid_suits}")

        self.suit = suit
        self.rank = rank

    # unicode value to print suit symbols
    suit_lu = {
        "C": "\u2663",
        "H": "\u2665",
        "D": "\u2666",
        "S": "\u2660",
        "X": ''
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

    def clear_hand(self):
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

    def show_hand(self, dealer_hide = False):
        
        if (self.is_dealer and dealer_hide):
            dealer_display = self.cards[:] 
            dealer_display[0] = Card('X', 'X')
            print('Dealer: ' + ' '.join(str(card) for card in dealer_display))
        elif (self.is_dealer and not dealer_hide):
            print('Dealer: ' + ' '.join(str(card) for card in self.cards))
        elif(not self.is_dealer):
            print('Player: ' + ' '.join(str(card) for card in self.cards))

    def message_hand_win(self):
        if self.is_dealer:
            print("Dealer wins!")
        elif not self.is_dealer:
            print("Player wins!")

    def player_choice(self, deck):
        '''Prompt player to hit or stand with a hand instance'''

        answer = ''
        while answer not in ['h', 's']:
            answer = input("Hit or Stand? H/S: ")
            if answer.lower() == "h":
                self.add_card(deck.deal())
            if answer.lower() == "s":
                print(f"Player stands with hand of {str(self.value)}\n")
                self.is_active = False

    def __repr__(self):
        return f'Hand({self.cards}, {self.is_dealer}, {self.is_active})'

    def __str__(self):
        num_cards = f'Number of cards in hand: {len(self.cards)}'
        value = f'Hand value: {str(self.value)}'
        return(num_cards + '\n' + value)

    

class Game:
    
    def __init__(self):
        self.hands = []
        self.deck = []
        self.player_turn = True

    def check_winner(self):
        #list(map())
        # print("here")

        # for i in self.hands:
        #     print(i.value)
        pass

    def end(self):
        print("Goodbye")
        sys.exit()

    
    def play(self):
        # self = Game()
        self.deck = Deck()
        self.deck.fill_deck()
        self.deck.shuffle()

        player = Hand(is_dealer = False, is_active = True)
        dealer = Hand(is_dealer = True)
        self.hands = [player, dealer]

        # deal 2 cards to each player
        for _ in range(2):
            for p in self.hands:
                # p = player
                p.add_card(self.deck.deal())


        # check for any blackjacks
        if dealer.has_blackjack:
            player.show_hand()
            dealer.show_hand()
            print('Blackjack!')
            dealer.message_hand_win()
            self.end()
 
        if player.has_blackjack and not dealer.has_blackjack:
            player.show_hand()
            dealer.show_hand()
            print('Blackjack!')
            player.message_hand_win()
            self.end()

        dealer.show_hand(dealer_hide = True)

        while player.is_active:
            player.show_hand()

            player.player_choice(deck = self.deck)

            if player.is_bust:
                print("Player busts. You lose!")
                player.is_active = False
                self.end()
        
        # dealer turn
        dealer.is_active = True

        while dealer.is_active:

            while dealer.value <= 16:
                
                print("Dealer Hits")
                dealer.add_card(self.deck.deal())
                dealer.show_hand()
                time.sleep(2)

                if dealer.is_bust:
                    print("Dealer busts. You win!")
                    dealer.is_active = False
                    self.end()
            
            dealer.is_active = False
            print(print(f"Dealer stands with hand of {str(dealer.value)}\n")
)

             



        # deck = Deck()
        # deck.fill_deck()
        # deck.shuffle()