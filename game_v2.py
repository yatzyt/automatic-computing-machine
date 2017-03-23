import numpy as np
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz
import time

import keys
from even_more_gen import make_profile

NUM_ATTR_TO_REMOVE_ROUND_1 = 5

NUM_ATTR_TO_REMOVE_ROUND_2 = 6

DEPTH = 3

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

def round_1(profiles, swipes):
    #assuming client has displayed the profiles, and we have the swipes to work with

    # makes the decision tree
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    
    profiles_for_tree = round_helper(profiles)

    # makes X and y for the tree, and sets it up with round 3's X and y
    X = profiles_for_tree
    y = np.array(swipes)

    tree.fit(X, y)

    print (zip(profiles[0].keys(), list(tree.feature_importances_)))
    print

    # figures out what attributes to remove
    feature_imp = tree.feature_importances_
    to_remove = feature_imp.argsort()[:NUM_ATTR_TO_REMOVE_ROUND_1]  # getting the index of those to remove
    removed = [profiles[0].keys()[i] for i in to_remove]

    return removed

def round_2(profiles, swipes):
    #assuming client has displayed the profiles, and we have the swipes to work with

    # makes the decision tree
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    
    profiles_for_tree = round_helper(profiles)

    # makes X and y for the tree, and sets it up with round 3's X and y
    X = profiles_for_tree
    y = np.array(swipes)

    tree.fit(X, y)

    print (zip(profiles[0].keys(), list(tree.feature_importances_)))
    print

    # figures out what attributes to remove
    feature_imp = tree.feature_importances_
    to_remove = feature_imp.argsort()[:NUM_ATTR_TO_REMOVE_ROUND_2]  # getting the index of those to remove
    removed = [profiles[0].keys()[i] for i in to_remove]

    return removed

def round_3(profiles, swipes):
    #assuming client has displayed the profiles, and we have the swipes to work with

    # makes the decision tree
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    
    profiles_for_tree = round_helper(profiles)

    # makes X and y for the tree, and sets it up with round 3's X and y
    X = profiles_for_tree
    y = np.array(swipes)

    tree.fit(X, y)
    
    print (zip(profiles[0].keys(), list(tree.feature_importances_)))
    print

    return X, y

def round_helper(profiles):
    # helper
    profiles_for_tree = []

    # this loop makes text into integers to classify
    for t_p in profiles:
        temp = []
        for name, v in t_p.items():
            temp.append(keys.translate_string_to_int(name, v))
        profiles_for_tree.append(temp)
    return np.array(profiles_for_tree)

'''
Uses the X and y returned from round 3, and returns the predicted score for round 4 to display
'''
def pre_round_4(profiles, tree_X, tree_y):
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    tree.fit(tree_X, tree_y)
    
    pp = round_helper(profiles)
    predictions = tree.predict(pp)#[tree.predict(pre_round_helper(p)) for p in profiles]
    
    return predictions

def round_4(profiles, swipes, tree_X, tree_y):
    #assuming client has displayed the profiles, and we have the swipes to work with

    # makes the decision tree
    tree = DecisionTreeClassifier(max_depth=DEPTH)

    profiles_for_tree = round_helper(profiles)

    # makes X and y for the tree, and sets it up with round 3's X and y
    X = profiles_for_tree 
    X = np.append(X, tree_X, axis = 0)
    y = np.array(swipes)
    y = np.append(y, tree_y, axis = 0)

    tree.fit(X, y)

    print (zip(profiles[0].keys(), list(tree.feature_importances_)))
    print
    
    return X, y

def pre_round_5(profiles, tree_X, tree_y):
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    tree.fit(tree_X, tree_y)
    predictions = tree.predict_proba(round_helper(profiles))
    
    print profiles[0].keys()
    export_graphviz(tree, out_file='round5.dot')

    return predictions

