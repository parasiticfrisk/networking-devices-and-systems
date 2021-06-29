#!/usr/bin/env python3
#
# Author: August Frisk
# Course: CmpEt 269 - Spring 2018
# Assign: Lab 01
# File: deck.py
#
# Description: A model of a deck of cards that can form the basis for building
#              digital card game programs such as Poker or Gin Rummy.
#

import random
from card import Card


class Deck:
    def __init__(self):
        self._cards = []
        self.populate()

    def populate(self):
        suits = ["hearts", "clubs", "diamonds", "spades"]
        numbers = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]
        self._cards = [Card(s, n) for s in suits for n in numbers]

    def shuffle(self):
        random.shuffle(self._cards)

    def deal(self, no_of_cards):
        dealt_cards = []
        for i in range(no_of_cards):
            dealt_card = self._cards.pop(0)
            dealt_cards.append(dealt_card)
        return dealt_cards

    def __repr__(self):
        cards_in_deck = len(self._cards)
        return "Deck of " + str(cards_in_deck) + " cards"


deck = Deck()
print(deck)
