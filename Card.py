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


if __name__ == "__main__":
    deck = [card(rank, suit) for rank in range(1, 14)
            for suit in iter(Suit)]
