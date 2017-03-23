from game_v2 import *
import pandas as pd
import numpy as np

def make_swipes(N):
    return [np.random.randint(2) for _ in range(N)]

# round 1
round_1_profs = make_prof(n_rep = 30)
round_1_swipes = make_swipes(30)
attr_to_remove = round_1_and_2(round_1_profs, round_1_swipes)

print attr_to_remove
print

# round 2
round_2_profs = make_prof(attrs_to_rmv = attr_to_remove, n_rep=30)
round_2_swipes = make_swipes(30)
attr_to_remove += round_1_and_2(round_2_profs, round_2_swipes)

print attr_to_remove