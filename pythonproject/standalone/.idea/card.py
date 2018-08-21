#-*- coding:utf-8 –*-
import collections
from random import choice

card=collections.namedtuple('Card',['size','color'])

class card_init():
    size=[str(n) for n in range(2,11)]+list('JQK')
    color='spades diamonds clubs hearts'.split()
    def __init__(self):
        self.card=[card(s,c) for s in self.size for c in self.color]
    def __len__(self):
        return len(self.card)
    def __getitem__(self, item):
        return self.card[item]

color_value=dict(spades=3,hearts=2,diamonds=1,clubs=0)
def cal_value(_cards):
    return color_value[_cards.color]*len(color_value)+card_init.size.index(_cards.size)

_cards=card_init()
print u'随机选取一张牌：'
print choice(_cards)
print u'牌的总数：'
print len(_cards)
print u'选择指定牌：'
print _cards[0]
#print u'迭代输出所有牌：'
#for card in _cards:
 #   print card
print u'牌值大小排序：'
for card in sorted(_cards,key=cal_value):
    print card