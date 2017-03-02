import numpy as np
from sklearn.tree import DecisionTreeClassifier  # , export_graphviz
import time

import keys
from more_gen import make_profile

minmax = {0: 'Min', 1: 'Max'}

left = ['LEFT', 'L', 'MIN', 'MINIMUM']
right = ['RIGHT', 'R', 'MAX', 'MAXIMUM']


def two_smallest(l):
    if l[0] < l[1]:
        smallest_ind = 0
        second_smallest_ind = 1
    else:
        smallest_ind = 1
        second_smallest_ind = 0
    for item in l[2:]:
        if item < l[smallest_ind]:
            second_smallest_ind = smallest_ind
            smallest_ind = l.index(item)
        elif l[smallest_ind] < item < l[second_smallest_ind]:
            second_smallest_ind = l.index(item)
    return smallest_ind, second_smallest_ind


def decision_to_str(d):
    if d == 'Min':
        return 'minimum sentence. (MIN)'
    else:
        return 'maximum sentence. (MAX)'


def remove_attr(attrs, prof):
    if not attrs:
        return prof
    for att in attrs:
        del prof[att]
    return prof


def round(attr_to_remove=None):
    profiles = []
    decisions = []

    for i in range(10):
        profile = make_profile()
        profile = remove_attr(attr_to_remove, profile)
        profiles.append(profile)
        for k, v in profiles[i].items():
            print k, ':', v
        did_not_get_an_acceptable_answer = True
        while did_not_get_an_acceptable_answer:
            answer = raw_input(
                'Should this person be max sentenced (R) or min sentenced (L)?').upper()
            if answer in left:
                decisions.append(minmax[0])
                did_not_get_an_acceptable_answer = False
            elif answer in right:
                decisions.append(minmax[1])
                did_not_get_an_acceptable_answer = False
        #decisions.append(minmax[np.random.randint(0, 2)])
        print 'The decision made was', decision_to_str(decisions[i])
        print decisions
        print
        #time.sleep(8)

    tree = DecisionTreeClassifier()

    profiles_for_tree = []

    for t_p in profiles:
        temp = []
        for name, v in t_p.items():
            temp.append(keys.translate_string_to_int(name, v))
        profiles_for_tree.append(temp)

    X = np.array(profiles_for_tree)
    y = np.array(decisions)

    tree.fit(X, y)

    if len(profiles[0].keys()) <= 3:
        return tree

    print (zip(profiles[0].keys(), list(tree.feature_importances_)))
    print

    feature_imp = list(tree.feature_importances_)
    to_remove = two_smallest(feature_imp)  # index of those to remove
    removed = [profiles[0].keys()[i] for i in to_remove]
    for r in removed:
        print 'Removed', r
    #time.sleep(5)
    print
    return removed

#    for i in range(len(tree.feature_importances_)):
#        print profiles[0].keys()[i], ':', list(tree.feature_importances_)[i]


input_for_round = []

for i in range(4):
    input_for_round += round(input_for_round)

res_tree = round(input_for_round)

a_profile = make_profile()
a_profile = remove_attr(input_for_round, a_profile)

a_X = []
for k, v in a_profile.items():
    a_X.append(keys.translate_string_to_int(k, v))

a_X = np.array([a_X])


print
print zip(a_profile.keys(), list(res_tree.feature_importances_))
print 
for k, v in a_profile.items():
    print k, ":", v
print zip(res_tree.classes_, res_tree.predict_proba(a_X)[0])

