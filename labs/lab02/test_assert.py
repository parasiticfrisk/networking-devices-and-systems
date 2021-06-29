#!/usr/bin/env python3
#
# Author: August Frisk
# Course: CmpEt 269 - Spring 2018
# Assign: Lab 02
# File: test_assert.py
#

from card import Card

card1 = Card("hearts", "2")
assert repr(card1) == "2 of hearts"

card2 = Card("hearts", "K")
assert card1.number != card2.number
