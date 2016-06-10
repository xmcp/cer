#coding=utf-8
"""
这是游戏规则的配置文件。
要想掌握自定义游戏规则的控制技巧，你需要一些肮脏的（划掉 PY编程的基本知识。
编辑完成后，需要重新运行服务器程序。

Cer by @xmcp.
https://github.com/xmcp/cer
"""

description='“X可以随便接”' #简要介绍这个规则
life_step=2 #超时减血的时间（秒），应为正整数
max_live=10 #玩家的生命值上限，应为正整数
skip_cost=3 #跳过当前回合所需的生命值，应为非负整数

import random

history=set()
with open('dict.txt','r') as f:
    words=set(f.read().split('\n'))

def init():
    """ 当每局新游戏开始时被调用。

    你需要初始化进行新一局游游戏需要的所有东西，例如单词历史纪录。
    返回这局游戏的第一个单词。
    """
    history.clear()
    return random.choice(tuple(words))

def validate(before,after):
    """ 当玩家试图提交一个新单词时被调用。
    
    参数 before 是当前的单词，after 是玩家尝试提交的单词。
    如果这次提交合法，返回 None；否则返回一个字符串，解释为什么这样不合法。
    """
    after=after.strip()
    if after in history:
        return '单词已经用过了'
    elif not after.isalpha():
        return '只能包含字母'
    elif before[-1]!=after[0]:
        return '首字母不符合要求'
    elif before[-1]!='x' and after not in words:
        return '单词不在词典中'
    history.add(after)

def skip(before):
    """ 当玩家试图跳过当前回合时被调用。
    
    参数 before 是当前单词。
    如果可以跳过，返回 {'valid': True, 'after': x}，其中 x 是下一回合的单词。
    如果不可以，返回 {'valid': False, 'error': r}，其中 r 是这个操作不合法的原因。
    """
    return {
        'valid':True,
        'after':random.choice(tuple(words))
    }
