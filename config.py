#coding=utf-8
"""
The sample config module for Cer.

This module should contains 3 functions: `init()`, `skip(before)` and `validate(before, after)`
and a constant str `description`
"""

import random

history=set()
with open('dict.txt','r') as f:
    words=set(f.read().split('\n'))
description='经典规则' #Briefly introduce this config

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
        return '单词在历史记录中'
    elif before[-1]!=after[0]:
        return '首字母不符合要求'
    elif after not in words:
        return '单词不在字典中'
    history.add(after)

def skip(before):
    """ Called when a player wants to skip the turn.

    :param before: The current word.
    :return: Returns a dict containing a bool key `valid` descripting wether the attempt is granted
        and a key `after` for the new word if granted else a key `error` desctipting the reason.
    """
    return {
        'valid':True,
        'after':random.choice(tuple(words))
    }