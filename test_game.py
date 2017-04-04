from game_v2 import *
import pandas as pd
import numpy as np

def make_swipes(N):
    return [np.random.randint(2) for _ in range(N)]

def make_1s(N):
    return [1 for _ in range(N)]

def make_0s(N):
    return [0 for _ in range(N)]

big_n = 10

# round 1
round_1_profs = make_prof(n_rep = big_n)
print round_1_profs[0]
round_1_swipes = make_swipes(big_n)
attr_to_remove = round_1(round_1_profs, round_1_swipes)


#print attr_to_remove
print 'Round 1 done\n'

# round 2
round_2_profs = make_prof(attrs_to_rmv = attr_to_remove, n_rep=big_n)
print round_2_profs[0]
round_2_swipes = make_swipes(big_n)
attr_to_remove += round_2(round_2_profs, round_2_swipes)

#print attr_to_remove
print 'Round 2 done\n'

# round 3

round_3_profs = make_prof(attrs_to_rmv = attr_to_remove, n_rep=big_n)
print round_3_profs[0]
round_3_swipes = make_swipes(big_n)
X, y = round_3(round_3_profs, round_3_swipes)

##if X.any() and y.any():
#    print "X and y exist\n"
print 'Round 3 done\n'

round_4_profs, test_tree = make_prof_with_pred(X, y, attrs_to_rmv = attr_to_remove, n_rep=big_n, round_num=4)
print round_4_profs[0]
round_4_swipes = make_swipes(big_n)
X, y = round_4(round_4_profs, round_4_swipes, X, y)

#print round_4_pred, '\n'
#if X.any() and y.any():
#    print "X and y exist\n"
print 'Round 4 done\n'
    
round_5_profs = make_prof_with_pred(X, y, attrs_to_rmv = attr_to_remove, n_rep=big_n, round_num=5)
print round_5_profs[0]
#round_5_swipes = make_swipes(big_n)

print 'Round 5 done\n'

# these are a list of lists of dictionaries (very good nesting :^)
prof_test = [round_1_profs, round_2_profs, round_3_profs, round_4_profs]
swip_test = [round_1_swipes, round_2_swipes, round_3_swipes, round_4_swipes]

# this returns a list of strings
strings_to_send = endgame(prof_test, swip_test)
for s in strings_to_send:
    print s