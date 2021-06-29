#!/usr/bin/env python3
#
# Author: August Frisk
# Course: CmpEt 269 - Spring 2018
# Assign: Lab 02
# File: test_assert.py
#

from card import Card
from deck import Deck
import logging

logging.basicConfig(level=logging.DEBUG)

my_card = Card("hearts", "6")
my_card.suit = "blobs"

deck = Deck()
