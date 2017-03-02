import numpy as np
from sklearn.tree import DecisionTreeClassifier  # , export_graphviz

import keys
from more_gen import make_profile

profile = make_profile()

for k, v in profile.items():
    print keys.translate_int_to_string(k, v)
