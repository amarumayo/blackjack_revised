

import random
from classes import Card, Hand, Deck, Game

# create a card
test_card = Card('A', 'L')

# create a test dealer and player hand
deck = Deck()
deck.fill_deck()
deck.shuffle()
player = Hand(is_dealer = False)
player.cards.append(Card("A", "D"))
player.cards.append(Card("5", "D"))
dealer = Hand(is_dealer = True)
dealer.cards.append(Card("10", "D"))
dealer.cards.append(Card("15", "D"))
hands = [dealer, player]

blackjack = [hand.has_blackjack() for hand in hands]
high = [hand.value for hand in hands]
high = [score == max(high) for score in high]
bust = [hand.is_bust for hand in hands]

blackjack
high
bust
