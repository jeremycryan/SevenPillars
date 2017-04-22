from Constants import *
from random import *


class Pad():
    def __init__(self, pos):
        self.KEY_DICT = PAD_DICT[pos]

def gen_sequence(length):
    seq = [5]
    #list_of_thing = [None]
    while len(seq) < length:
        num = randint(1, 9)
        try:
            list_of_thing = [num, seq[0], seq[1]]
        except:
            list_of_thing = [num, seq[0]]
        if num not in seq and list_of_thing.sort() not in NOT_COOL:
            seq.insert(0, num)
    return seq
