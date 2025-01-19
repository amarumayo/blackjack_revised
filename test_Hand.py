from classes import Hand, Card
import unittest

class TestHand(unittest.TestCase):
    def test_has_blackjack_true(self):
        hand_1 = Hand(is_dealer = False)  
        hand_1.cards = [Card("A", "Spades"), Card("10", "Clubs")]
        self.assertTrue(hand_1.has_blackjack())

    def test_has_blackjack_21_with_3_cards(self):
        hand_1 = Hand(is_dealer = False)    
        hand_1.cards = [Card("A", "Spades"), Card("8", "Clubs"), Card("2", "clubs")]
        self.assertFalse(hand_1.has_blackjack())    

    def test_value_with_one_ace(self):
        hand_1 = Hand(is_dealer = False)  
        hand_1.cards = [Card("A", "Spades"), Card("5", "Clubs")]
        self.assertEqual(hand_1.value, 16)

    def test_value_with_two_ace(self):
        hand_1 = Hand(is_dealer = False)  
        hand_1.cards = [Card("A", "Spades"), Card("A", "Clubs"), Card("10", "Clubs")]
        self.assertEqual(hand_1.value, 12)

    def test_value_with_two_ace2(self):
        hand_1 = Hand(is_dealer = False)  
        hand_1.cards = [Card("A", "Spades"), Card("A", "Clubs"), Card("9", "Clubs")]
        self.assertEqual(hand_1.value, 21)

    def test_value_facecards(self):
        hand_1 = Hand(is_dealer = False)  
        hand_1.cards = [Card("J", "Spades"), Card("Q", "Clubs"), Card("K", "Clubs")]
        self.assertEqual(hand_1.value, 30)

    def test_is_bust_true(self):
        hand_1 = Hand(is_dealer = False)  
        hand_1.cards = [Card("J", "Spades"), Card("Q", "Clubs"), Card("Q", "Clubs")]
        self.assertTrue(hand_1.is_bust())

    def test_is_bust_false(self):
        hand_1 = Hand(is_dealer = False)  
        hand_1.cards = [Card("J", "Spades"), Card("Q", "Clubs")]
        self.assertFalse(hand_1.is_bust())


if __name__ == "__main__":
    unittest.main()



