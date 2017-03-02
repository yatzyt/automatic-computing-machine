import numpy as np
from sklearn.tree import DecisionTreeClassifier  # , export_graphviz

import keys
from more_gen import make_profile

profiles = []

for i in range(10):
    profiles.append(make_profile())

print "placeholder"