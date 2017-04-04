import numpy as np
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz
import time

#My Libraries
import keys 
from even_more_gen import make_profile 

NUM_ATTR_TO_REMOVE_ROUND_1 = 5

NUM_ATTR_TO_REMOVE_ROUND_2 = 5

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
        del p['File Name']

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

    for ind, tr in enumerate(to_remove):
        if profiles[0].keys()[tr] == 'Offense':
            to_remove = np.delete(to_remove, ind, 0)
            next_in_line = np.array([feature_imp.argsort()[NUM_ATTR_TO_REMOVE_ROUND_1]])
            to_remove = np.append(to_remove, next_in_line, 0)

    removed = [profiles[0].keys()[i] for i in to_remove]

    return removed

def round_2(profiles, swipes):
    #assuming client has displayed the profiles, and we have the swipes to work with
    for p in profiles:
        del p['Min']
        del p['Max']
        del p['File Name']

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

    for ind, tr in enumerate(to_remove):
        if profiles[0].keys()[tr] == 'Offense':
            to_remove = np.delete(to_remove, ind, 0)
            next_in_line = np.array([feature_imp.argsort()[NUM_ATTR_TO_REMOVE_ROUND_2]])
            to_remove = np.append(to_remove, next_in_line, 0)

    removed = [profiles[0].keys()[i] for i in to_remove]

    return removed

def round_3(profiles, swipes):
    #assuming client has displayed the profiles, and we have the swipes to work with
    for p in profiles:
        del p['Min']
        del p['Max']
        del p['File Name']

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


def extract_proba(pred, flag, value):
    pred_ret = []
    if flag:
        if value == 1:
            for p in pred:
                pred_ret.append(int(p[0] * 10))
        elif value == 0:
            for p in pred:
                pred_ret.append(10 - int(p[0] * 10))
        else:
            raise Exception("There was non 0 or 1 input")
    else:
        for p in pred:
            pred_ret.append(int(p[1] * 10))
    return pred_ret

def check_y_is_single(tree_y):
    '''
    This function checks to see if an array y has all the same values in the array, and returns True if it does, and returns the value along with it.
    '''
    curr = tree_y[0]
    for i in tree_y:
        if curr != i:
            return False, curr
    return True, curr

'''
Uses the X and y returned from round 3, and returns the predicted score for round 4 to display
'''
def pre_round_4(profiles, tree_X, tree_y):
    tree = DecisionTreeClassifier(max_depth=DEPTH)
    tree.fit(tree_X, tree_y)

    single_y_flag, single_y_value = check_y_is_single(tree_y)
    
    temp_min = []
    temp_max = []
    temp_file_name = [] 
    for p in profiles:
        temp_min.append(p['Min'])
        temp_max.append(p['Max'])
        temp_file_name.append(p['File Name'])
        del p['Min']
        del p['Max']
        del p['File Name']

    #print profiles[0].keys()
    pp = round_helper(profiles)
    
    predictions = tree.predict_proba(pp)#[tree.predict(pre_round_helper(p)) for p in profiles]

    importances = sorted(zip(tree.feature_importances_, profiles[0].keys()), reverse=True)
    imp_ret = []
    for i in importances:
        imp_ret.append(i[1])    

    for ind, p in enumerate(profiles):
        p['Min'] = temp_min[ind]
        p['Max'] = temp_max[ind]
        p['File Name'] = temp_file_name[ind]    
    
    return extract_proba(predictions, single_y_flag, single_y_value), imp_ret

def make_prof_with_pred(tree_X, tree_y, attrs_to_rmv = None, n_rep=10, round_num=4):
    profs = make_prof(attrs_to_rmv, n_rep)

    pred = []
    if round_num == 4:
        pred, imp_ret = pre_round_4(profs, tree_X, tree_y)
    else:
        pred = pre_round_5(profs, tree_X, tree_y)
    for i in range(len(profs)):
        profs[i]['Prediction'] = pred[i]
        #print i


    if round_num == 5:
		profs_5 = [{ 'Prediction': p['Prediction'], 'Min': p['Min'], 'Max': p['Max'], 'File Name': p['File Name']} for p in profs]
		return profs_5  #, profs
	
    return profs, int_ret

def round_4(profiles, swipes, tree_X, tree_y):
    #assuming client has displayed the profiles, and we have the swipes to work with
    for p in profiles:
        del p['Min']
        del p['Max']
        del p['Prediction']
        del p['File Name']

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

    single_y_flag, single_y_value = check_y_is_single(tree_y)

    temp_min = []
    temp_max = []
    temp_file_name = []
    for p in profiles:
        temp_min.append(p['Min'])
        temp_max.append(p['Max'])
        temp_file_name.append(p['File Name'])
        del p['Min']
        del p['Max']
        del p['File Name']

    predictions = tree.predict_proba(round_helper(profiles))

    for ind, p in enumerate(profiles):
        p['Min'] = temp_min[ind]
        p['Max'] = temp_max[ind]
        p['File Name'] = temp_file_name[ind]
    
    #print profiles[0].keys()
    export_graphviz(tree, out_file='round5.dot')

    return extract_proba(predictions, single_y_flag, single_y_value)

def endgame(profiles, swipes):
    '''
    uses two lists of lists of dictionaries in the order of round 1, round 2, round 3, round 4 to determine certain user results
    '''

    # helps keep track of the results, is a dictionary of dictionaries
    results = {}

    # stores what attributes made it to the end
    good = []

    # things in the dictionaries that we don't care about
    bad = ['Min', 'Max', 'File Name', 'Prediction']

    # adds 1 if we have 1, subtracts 1 otherwise
    counter_helper = {
        1 : 1,
        0 : -1
    }

    # extracts the info we need
    for at in profiles[3][0].keys():
        if not at in bad:
            good.append(at)
            results[at] = {}

    #iterating through each round
    for ind, round_n in enumerate(profiles):
        #iterating through each profile in each round
        for ind_2, prof in enumerate(round_n):
            #iterating through each attribute in each profile
            for attr, actual in prof.items():
                if attr == 'Date of Birth':
                    actual = keys.translate_string_to_int(attr,actual)
                if attr in results:
                    if not actual in results[attr]:
                        results[attr][actual] = counter_helper[swipes[ind][ind_2]]
                    else:
                        results[attr][actual] += counter_helper[swipes[ind][ind_2]]
    
    return_strings = []

    for attr, counts in results.items():
        max_name, max_count = '', -1000
        min_name, min_count = '', 1000
        for name, count in counts.items():
            if count >= max_count:
                max_count = count
                max_name = name
            if count <= min_count:
                min_count = count
                min_name = name
        if attr == 'Date of Birth':
            attr = 'age'
        return_strings.append('You tend to sentence people with a(n) ' + attr.lower() + ' of ' + str(max_name).lower() + ' harsher.')
        return_strings.append('You tend to sentence people with a(n) ' + attr.lower() + ' of ' + str(min_name).lower() + ' lighter.')

    return return_strings