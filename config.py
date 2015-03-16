#coding=utf-8
"""
The sample config module for Cer.

This module should contains 2 functions: `init()` and `validate(before, after)`.
"""

import random
history=set()
with open('dict.txt','r') as f:
    words=set(f.read().split('\n'))

def init():
    """ Called when a game is about to start.
    In this function, you should clear the game data to prepare for a new game.

    :return: Returns the first word of the game.
    """
    history.clear()
    return random.choice(tuple(words))

def validate(before,after):
    """ Called when a player wants to submit the word during the game.

    :param before: The current word.
    :param after: The player's word.
    :return: Returns a false-like object if the attempt is valid; otherwise returns a description str.
    """
    if after in history:
        return 'In history'
    elif before[-1]!=after[0]:
        return 'Qipa'
    elif after not in words:
        return 'Not In Dict'
    history.add(after)