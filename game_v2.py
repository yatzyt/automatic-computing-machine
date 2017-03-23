import numpy as np
from sklearn.tree import DecisionTreeClassifier  # , export_graphviz
import time

import keys
from even_more_gen import make_profile

#PROFILE = 

NUM_ATTR_TO_REMOVE_PER_ROUND = 5

minmax = {0: 'Min', 1: 'Max'}

left = ['LEFT', 'L', 'MIN', 'MINIMUM']
right = ['RIGHT', 'R', 'MAX', 'MAXIMUM']

'''
This method makes 10 profiles, and deletes attributes that were called to be deleted
'''
def make_prof(attrs_to_rmv = None, n_rep=10):
    profs = []
    for i in range(n_rep):
        temp = make_profile()
        if attrs_to_rmv:
            for attr in attrs_to_rmv:
                del temp[attr]
        profs.append(temp)
    return profs

def round_1_and_2(profiles, swipes):
    #assuming client has displayed the profiles, and we have the swipes to work with

    # makes the decision tree
    tree = DecisionTreeClassifier()
    
    # helper
    profiles_for_tree = []

    # this loop makes text into integers to classify
    for t_p in profiles:
        temp = []
        for name, v in t_p.items():
            temp.append(keys.translate_string_to_int(name, v))
        profiles_for_tree.append(temp)

    # makes X and y for the tree
    X = np.array(profiles_for_tree)
    y = np.array(swipes)

    tree.fit(X, y)

    print (zip(profiles[0].keys(), list(tree.feature_importances_)))
    print

    # figures out what attributes to remove
    feature_imp = tree.feature_importances_
    to_remove = feature_imp.argsort()[:NUM_ATTR_TO_REMOVE_PER_ROUND]  # getting the index of those to remove
    removed = [profiles[0].keys()[i] for i in to_remove]

    return removed

def round_3(profiles, swipes):
    #assuming client has displayed the profiles, and we have the swipes to work with

    # makes the decision tree
    tree = DecisionTreeClassifier()
    
    # helper
    profiles_for_tree = []

    # this loop makes text into integers to classify
    for t_p in profiles:
        temp = []
        for name, v in t_p.items():
            temp.append(keys.translate_string_to_int(name, v))
        profiles_for_tree.append(temp)

    # makes X and y for the tree
    X = np.array(profiles_for_tree)
    y = np.array(swipes)

    tree.fit(X, y)

    return X, y

def pre_round_helper(profile):
    profile_to_return_for_tree = []
    for name, val in profile.items():
        profile_to_return_for_tree.append(keys.translate_string_to_int(name, val))
    return np.array([profile_to_return_for_tree])

'''
Uses the X and y returned from round 3, and returns the predicted score for round 4 to display
'''
def pre_round_4(profiles, tree_X, tree_y):
    tree = DecisionTreeClassifier()
    tree.fit(tree_X, tree_y)
    predictions = [pre_round_helper(p) for p in profiles]

    return predictions

def round_4(profiles, swipes, tree_X, tree_y):
    #assuming client has displayed the profiles, and we have the swipes to work with

    # makes the decision tree
    tree = DecisionTreeClassifier()
    
    # helper
    profiles_for_tree = []

    # this loop makes text into integers to classify
    for t_p in profiles:
        temp = []
        for name, v in t_p.items():
            temp.append(keys.translate_string_to_int(name, v))
        profiles_for_tree.append(temp)

    # makes X and y for the tree, and sets it up with round 3's X and y
    X = np.array(profiles_for_tree) 
    X = np.append(X, tree_X, axis = 0)
    y = np.array(swipes)
    y = np.append(y, tree_y, axis = 0)

    tree.fit(X, y)

    return X, y

def pre_round_5(profiles, tree_X, tree_y):
    tree = DecisionTreeClassifier()
    tree.fit(tree_X, tree_y)
    predictions = [pre_round_helper(p) for p in profiles]

    return predictions

