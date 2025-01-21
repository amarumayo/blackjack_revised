import enlighten
import time
from classes import Card, Hand
import io


card1 = Card("5", "C")
card2 = Card("10", "D")
hand1 = Hand(is_dealer=False)
hand1.cards = [card1, card2]

card1 = Card("4", "S")
card2 = Card("6", "D")
hand2 = Hand(is_dealer=True)
hand2.cards = [card1, card2]

manager = enlighten.get_manager()

status_format = '{hand1}{fill}{hand2}{fill}'
status_bar = manager.status_bar(status_format = status_format,
                                color ='red',
                                position = 10,
                                hand1 = hand1.show(),
                                hand2 = hand2.show())
hand1.add_card(Card("A", "D"))
time.sleep(2)
status_bar.update(hand1 = hand1.show())

hand2.add_card(Card("A", "D"))
time.sleep(2)
status_bar.update(hand2 = hand2.show())
time.sleep(2)
