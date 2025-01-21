import random
import sys
import time
import os
import enlighten


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

    def __init__(self, is_dealer, turn = False):
        self.cards = []
        self.is_dealer = is_dealer
        self.turn = turn
        self.win_count = 0

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
                return(f' X, {", ".join(str(card) for card in self.cards[1:])}')
            else:
                return(f'{", ".join(str(card) for card in self.cards)}')
        else:
            return(f' {", ".join(str(card) for card in self.cards)}')
   

    def __repr__(self):
        return f'Hand({self.cards}, {self.is_dealer}, {self.turn})'

    def __str__(self):
        num_cards = f'Number of cards in hand: {len(self.cards)}'
        value = f'Hand value: {str(self.value)}'
        return(num_cards + '\n' + value)

    
class Game:
    
    def __init__(self):
        self.deck = Deck()
        self.player = Hand(is_dealer = False, turn = None)
        self.dealer = Hand(is_dealer = True)
        self.game_active = True
    
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

            # set up score board
            score_manager = enlighten.get_manager()
            score_status_bar_format = '{fill}Player Score: {player_score}{fill}Dealer Score: {dealer_score}{fill}'
            score_status_bar = score_manager.status_bar(
                status_format = score_status_bar_format,
                color ='red',
                autorefresh = True,
                position = 6,
                player_score = self.player.show(),
                dealer_score = self.dealer.show()
            )

            # set up container for hands 
            hand_manager = enlighten.get_manager()
            hand_status_bar_format = '{fill}{player_hand}{fill}{dealer_hand}{fill}'
            hand_status_bar = hand_manager.status_bar(
                status_format = hand_status_bar_format,
                color = 'blue',
                position = 2,
                player_hand = '',
                dealer_hand = ''
            )
            time.sleep(.2)

            # set up container for messages 
            message_manager = enlighten.get_manager()
            message_status_bar_format = '{message}'
            message_status_bar = message_manager.status_bar(
                status_format = message_status_bar_format,
                color = 'green',
                position = 10,
                message = ''
            )
            time.sleep(.2)
         
            # clear hands, shuffle and set player turn each time we play
            self.deck.clear_deck()
            self.deck.fill_deck()
            self.deck.shuffle()
            self.player.clear()
            self.dealer.clear()
            self.player.turn = True

            # deal 2 cards to each player
            for _ in range(2):
                for p in [self.dealer, self.player]:
                    # p = player
                    p.add_card(self.deck.deal())

            
            # show hand
            hand_status_bar.update(
                player_hand = str(self.player.show()),
                dealer_hand = str(self.dealer.show())
            )
            time.sleep(.2)


            # check for any blackjacks
            if self.dealer.has_blackjack:
                message_status_bar.update(message = 'Dealer has blackjack. You Lose.')
                time.sleep(.2)

                self.dealer.win_count += 1
                self.player.turn = False
    
            if self.player.has_blackjack and self.player.turn:
                message_status_bar.update(message = 'You have blackjack! You Win!')
                time.sleep(2)

                self.player.win_count += 1
                self.player.turn = False
                time.sleep(.2)
                
            while self.player.turn:
                
                answer = ''
                while answer not in ['h', 's']:
                    answer = input("Hit or Stand? H/S: ")
                                
                if answer.lower() == "h":
                    self.player.add_card(self.deck.deal())
                    hand_status_bar.update(player_hand = str(self.player.show()))
                    time.sleep(2)

                
                    if self.player.is_bust:
                        message_status_bar.update(message = 'Bust! You Lose')
                        time.sleep(2)

                        self.dealer.win_count += 1
                        self.player.turn = False

                elif answer.lower() == "s":
                    self.player.turn = False

            
            if not self.player.is_bust \
                and not self.player.has_blackjack \
                    and not self.dealer.has_blackjack:
                
                # dealer turn
                self.dealer.turn = True
                while self.dealer.turn:

                    while self.dealer.value <= 16 and \
                        not self.dealer.is_bust:
                        
                        message_status_bar.update(message = 'Dealer hits')
                        self.dealer.add_card(self.deck.deal())
                        hand_status_bar.update(dealer_hand = str(self.dealer.show()))
                        time.sleep(2)

                        if self.dealer.is_bust:
                            message_status_bar.update(message = 'Dealer busts! You Win')
                            self.player.win_count +=1
                            self.dealer.turn = False

                    if not self.dealer.is_bust:
                        message_status_bar.update(message = 'Dealer stands')
                        time.sleep(2)
                    
                    # end dealer turn
                    self.dealer.turn = False

                # evaluate hands if the game is still going   
                if not self.dealer.turn and \
                    not self.player.turn and \
                    not self.player.is_bust and \
                    not self.dealer.is_bust:

                    if self.dealer.value >= self.player.value:
                        self.dealer.win_count += 1 
                        message_status_bar.update(message = 'you lose')
                        time.sleep(2)


                    else: 
                        self.player.win_count += 1 
                        message_status_bar.update(message = 'you win!')
                        time.sleep(2)


            
            # updates scores
            score_status_bar.update(
                player_score = str(self.player.win_count),
                dealer_score = str(self.dealer.win_count)
            )

            
            answer = ''
            while answer not in ['y', 'n']:
                answer = input("Play again? Y/N:")

                if answer.lower() == 'n':
                    self.game_active = False
                    self.end()