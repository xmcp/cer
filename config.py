#coding=utf-8
history=set()
with open('dict.txt','r') as f:
    words=set(f.read().split('\n'))
start_word='hello'

def validate(before,after):
    if after in history:
        return 'In history'
    if before[-1]!=after[0]:
        return 'Qipa'
    if after not in words:
        return 'Not In Dict'
    #okay
    history.add(after)