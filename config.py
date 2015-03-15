#coding=utf-8
history=set()

def validate(before,after):
    if after in history:
        return 'In history'
    if before[-1]!=after[0]:
        return 'Qipa'
    history.add(after)