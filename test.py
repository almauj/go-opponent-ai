"""
Testing class objects and functions

"""

from model import GoEngine

obj = GoEngine()

neighbors = obj.get_neighbors(3,5)
group = obj.find_group(3,5)
liberties = obj.count_liberties(group)

print(neighbors)
print(group) # function works, but cannot test on empty board
print(liberties) # returns zero if set is emtpy.