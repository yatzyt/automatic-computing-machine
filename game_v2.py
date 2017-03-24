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
This method makes n_rep profiles, and deletes attributes that were called to be deleted
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
    for p in profiles:
        del p['Min']
        del p['Max']

    # makes the decision tree
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    
    profiles_for_tree = round_helper(profiles)

    # makes X and y for the tree, and sets it up with round 3's X and y
    X = profiles_for_tree
    y = np.array(swipes)

    tree.fit(X, y)

    #print (zip(profiles[0].keys(), list(tree.feature_importances_)))
    #print

    # figures out what attributes to remove
    feature_imp = tree.feature_importances_
    to_remove = feature_imp.argsort()[:NUM_ATTR_TO_REMOVE_ROUND_1]  # getting the index of those to remove
    removed = [profiles[0].keys()[i] for i in to_remove]

    return removed

def round_2(profiles, swipes):
    #assuming client has displayed the profiles, and we have the swipes to work with
    for p in profiles:
        del p['Min']
        del p['Max']

    # makes the decision tree
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    
    profiles_for_tree = round_helper(profiles)

    # makes X and y for the tree, and sets it up with round 3's X and y
    X = profiles_for_tree
    y = np.array(swipes)

    tree.fit(X, y)

    #print (zip(profiles[0].keys(), list(tree.feature_importances_)))
    #print

    # figures out what attributes to remove
    feature_imp = tree.feature_importances_
    to_remove = feature_imp.argsort()[:NUM_ATTR_TO_REMOVE_ROUND_2]  # getting the index of those to remove
    removed = [profiles[0].keys()[i] for i in to_remove]

    return removed

def round_3(profiles, swipes):
    #assuming client has displayed the profiles, and we have the swipes to work with
    for p in profiles:
        del p['Min']
        del p['Max']

    # makes the decision tree
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    
    profiles_for_tree = round_helper(profiles)

    # makes X and y for the tree, and sets it up with round 3's X and y
    X = profiles_for_tree
    y = np.array(swipes)

    tree.fit(X, y)
    
    #print (zip(profiles[0].keys(), list(tree.feature_importances_)))
    #print

    return X, y

def round_helper(profiles):
    # helper
    #for p in profiles:
    #    if 'Min' in p:
    #        del p['Min']
    #    if 'Max' in p:
    #        del p['Max']
    #    if 'Prediction' in p:
    #        del p['Prediction']

    profiles_for_tree = []

    # this loop makes text into integers to classify
    for t_p in profiles:
        temp = []
        for name, v in t_p.items():
            temp.append(keys.translate_string_to_int(name, v))
        profiles_for_tree.append(temp)
    return np.array(profiles_for_tree)


def extract_proba(pred):
    pred_ret = []
    for p in pred:
        pred_ret.append(int(p[1] * 10))
    return pred_ret

'''
Uses the X and y returned from round 3, and returns the predicted score for round 4 to display
'''
def pre_round_4(profiles, tree_X, tree_y):
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    tree.fit(tree_X, tree_y)
    
    temp_min = []
    temp_max = []
    for p in profiles:
        temp_min.append(p['Min'])
        temp_max.append(p['Max'])
        del p['Min']
        del p['Max']

    pp = round_helper(profiles)
    
    predictions = tree.predict_proba(pp)#[tree.predict(pre_round_helper(p)) for p in profiles]
    for ind, p in enumerate(profiles):
        p['Min'] = temp_min[ind]
        p['Max'] = temp_max[ind]
    
    return extract_proba(predictions)

def make_prof_with_pred(tree_X, tree_y, attrs_to_rmv = None, n_rep=10, round_num=4):
    profs = make_prof(attrs_to_rmv, n_rep)
    pred = []
    if round_num == 4:
        pred = pre_round_4(profs, tree_X, tree_y)
    else:
        pred = pre_round_5(profs, tree_X, tree_y)
    for i in range(len(profs)):
        profs[i]['Prediction'] = pred[i]
    return profs

def round_4(profiles, swipes, tree_X, tree_y):
    #assuming client has displayed the profiles, and we have the swipes to work with
    for p in profiles:
        del p['Min']
        del p['Max']
        del p['Prediction']

    # makes the decision tree
    tree = DecisionTreeClassifier(max_depth=DEPTH)

    profiles_for_tree = round_helper(profiles)

    # makes X and y for the tree, and sets it up with round 3's X and y
    X = profiles_for_tree 
    X = np.append(X, tree_X, axis = 0)
    y = np.array(swipes)
    y = np.append(y, tree_y, axis = 0)

    tree.fit(X, y)

    #print (zip(profiles[0].keys(), list(tree.feature_importances_)))
    #print
    
    return X, y


def pre_round_5(profiles, tree_X, tree_y):
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    tree.fit(tree_X, tree_y)

    temp_min = []
    temp_max = []
    for p in profiles:
        temp_min.append(p['Min'])
        temp_max.append(p['Max'])
        del p['Min']
        del p['Max']

    predictions = tree.predict_proba(round_helper(profiles))

    for ind, p in enumerate(profiles):
        p['Min'] = temp_min[ind]
        p['Max'] = temp_max[ind]
    
    #print profiles[0].keys()
    #export_graphviz(tree, out_file='round5.dot')

    return extract_proba(predictions)

