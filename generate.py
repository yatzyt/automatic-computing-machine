import numpy as np
import pandas as pd

# I should have used dictionaries here but I'm too lazy to rethink these methods so dictionaries work :D

def makeProb(array):
    prob = [array[0]]
    for i in range(len(array)-1):
        prob.append(prob[i] + array[i+1])
    return prob

def checkProb(check, prob):
    for i in prob:
        if check <= i:
            return prob.index(i)
    raise Exception('check should not be greater than 1')

