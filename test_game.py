from game_v2 import *
import pandas as pd
import numpy as np

def make_swipes(N):
    return [np.random.randint(2) for _ in range(N)]

big_n = 10

# round 1
round_1_profs = make_prof(n_rep = big_n)
round_1_swipes = make_swipes(big_n)
attr_to_remove = round_1(round_1_profs, round_1_swipes)

#print attr_to_remove
print 'Round 1 done\n'

# round 2
round_2_profs = make_prof(attrs_to_rmv = attr_to_remove, n_rep=big_n)
round_2_swipes = make_swipes(big_n)
attr_to_remove += round_2(round_2_profs, round_2_swipes)

#print attr_to_remove
print 'Round 2 done\n'

# round 3

round_3_profs = make_prof(attrs_to_rmv = attr_to_remove, n_rep=big_n)
round_3_swipes = make_swipes(big_n)
X, y = round_3(round_3_profs, round_3_swipes)

##if X.any() and y.any():
#    print "X and y exist\n"
print 'Round 3 done\n'

round_4_profs = make_prof(attrs_to_rmv = attr_to_remove, n_rep=big_n)
round_4_swipes = make_swipes(big_n)
round_4_pred = pre_round_4(round_4_profs, X, y)
X, y = round_4(round_4_profs, round_4_swipes, X, y)

#print round_4_pred, '\n'
#if X.any() and y.any():
#    print "X and y exist\n"
print 'Round 4 done\n'
    
round_5_profs = make_prof(attrs_to_rmv = attr_to_remove, n_rep=big_n)
round_5_swipes = make_swipes(big_n)
round_5_pred = pre_round_5(round_5_profs, X, y)

print round_5_pred