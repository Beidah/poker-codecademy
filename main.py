from enum import Enum
import random


class OrderedEnum(Enum):
    def __ge__(self, other):

        if self.__class__ is other.__class__:

            return self.value >= other.value

        return NotImplemented

    def __gt__(self, other):

        if self.__class__ is other.__class__:

            return self.value > other.value

        return NotImplemented

    def __le__(self, other):

        if self.__class__ is other.__class__:

            return self.value <= other.value

        return NotImplemented

    def __lt__(self, other):

        if self.__class__ is other.__class__:

            return self.value < other.value

        return NotImplemented


class Value(OrderedEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10

    def __repr__(self) -> str:
        return "<%s.%s>" % (self.__class__.__name__, self._name_)

    def __str__(self) -> str:
        value_map = {
            Value.ACE: "A",
            Value.JACK: "J",
            Value.QUEEN: "Q",
            Value.KING: "K",
        }
        return value_map.get(self, str(self.value))


class Suit(Enum):
    SPADES = 1
    HEARTS = 2
    DIAMONDS = 3
    CLUBS = 4

    def __repr__(self) -> str:
        return "<%s.%s>" % (self.__class__.__name__, self._name_)

    def __str__(self) -> str:
        suit_symbols = {
            Suit.SPADES: "♠",
            Suit.HEARTS: "♥",
            Suit.DIAMONDS: "♦",
            Suit.CLUBS: "♣"
        }

        return suit_symbols[self]


class Card:
    def __init__(self, value: Value, suit: Suit):
        self.value = value
        self.suit = suit

    def __repr__(self) -> str:
        return "<%s, %s>" % (self.value.__repr__(), self.suit.__repr__())

    def __str__(self) -> str:
        return "%s%s" % (self.value, self.suit)


class Hand:
    def __init__(self):
        self.cards = []

    @property
    def value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.value == Value.ACE:
                aces += 1
                value += 1
            else:
                value += card.value.value

        # promote aces to 11, if they can
        while aces > 0 and value <= 11:
            aces -= 1
            value += 10

        return value

    def add_card(self, card):
        self.cards.append(card)

    def clear(self):
        self.cards = []

    def __str__(self) -> str:
        return ", ".join([str(card) for card in self.cards])


class Deck:
    def __init__(self):
        self.cards = []
        for suit in Suit:
            for value in Value:
                self.cards.append(Card(value, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()


class Game:
    def __init__(self) -> None:
        self.dealer = Hand()
        self.player = Hand()
        self.deck = Deck()
        self.deck.shuffle()

        for i in range(2):
            self.dealer.add_card(self.deck.draw())
            self.player.add_card(self.deck.draw())

    def show_cards(self):
        self.print_dealer()
        print("------------------")
        self.print_player()

    def print_dealer(self):
        print("Dealer hand:")
        print(self.dealer)
        print("Value:", self.dealer.value)

    def print_player(self):
        print("Player hand:")
        print(self.player)
        print("Value:", self.player.value)

    def play(self):
        while self.player.value < 21:
            self.print_player()
            answer = input("Hit (h), Stand (s), or Quit (q)? ")
            if answer == "h":
                self.player.add_card(self.deck.draw())
            elif answer == "s":
                break
            elif answer == "q":
                quit()

        self.print_player()
        if self.player.value == 21:
            print("Blackjack!")
            return True
        elif self.player.value > 21:
            print("Bust!")
            return False
        else:
            while self.dealer.value < 17:
                self.print_dealer()
                print("Dealer hits!")
                self.dealer.add_card(self.deck.draw())

        self.print_dealer()
        print("Dealer stays.")
        self.print_dealer()
        if self.dealer.value > 21:
            print("Dealer bust!")
            return True

        return self.player.value > self.dealer.value


if __name__ == "__main__":
    while True:
        game = Game()
        game.print_dealer()
        print("------------------")
        if game.play():
            print("Player wins!")
        else:
            print("Dealer wins!")

        answer = input("Play again? (y/n) ")
        if answer == "n":
            break
