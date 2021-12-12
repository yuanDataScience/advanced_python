# function factory method example:
from enum import Enum
from typing import Tuple


class Card:
    def __init__(self, rank: str, suit: str) -> None:
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()

    def _points(self) -> Tuple[int, int]: return int(self.rank), int(self.rank)


class AceCard(Card):
    def _points(self) -> Tuple[int, int]: return 1, 11


class FaceCard(Card):
    def _points(self) -> Tuple[int, int]: return 10, 10


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


def card(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    elif 11 <= rank < 14:
        name = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard(name, suit)
    raise Exception("Design Failure")


def card6(rank: int, suit: Suit) -> Card:
    class_, rank_str = {
                        1: (AceCard, "A"),
                        11: (FaceCard, "J"),
                        12: (FaceCard, "Q"),
                        13: (FaceCard, "K")
    }.get(rank, (Card, str(rank))
          )
    return class_(rank_str, suit)


#This use of the partial() function is a common technique for functional programming.
# It is one way to achieve a kind of polymorphism so that several different functions
# can be used in a similar way.
#In general, however, partial functions aren't helpful for most object-oriented programming.
# When building complex objects, it is common to define methods that accept arguments
# incrementally. Instead of using rank to create a partial function,
# a more object-oriented approach is to use separate methods to set rank and suit.

def card7(rank: int, suit: Suit) -> Card:
    class_rank = {
        1: lambda suit: AceCard("A", suit),
        11: lambda suit: FaceCard("J", suit),
        12: lambda suit: FaceCard("Q", suit),
        13: lambda suit: FaceCard("K", suit),
}.get(
rank, lambda suit: Card(str(rank), suit)
                    )
    return class_rank(suit)


class CardFactory:
    def rank(self, rank: int) -> "CardFactory":
        self.class_, self.rank_str = {1: (AceCard, "A"),
                                      11: (FaceCard, "J"),
                                      12: (FaceCard, "Q"),
                                      13: (FaceCard, "K"),
                                      }.get(
            rank, (Card, str(rank))
        )
        return self

    def suit(self, suit: Suit) -> Card:
        return self.class_(self.rank_str, suit)

if __name__ == "__main__":
    deck = [card(rank, suit) for rank in range(1, 14)
            for suit in iter(Suit)]

    deck7 = [card7(rank, suit) for rank in range(1, 14)
            for suit in iter(Suit)]

    card8 = CardFactory()
    deck8 = [card8.rank(r + 1).suit(s) for r in range(13) for s in Suit]