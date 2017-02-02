import numpy as np
import pandas as pd

# I should have used dictionaries here but I'm too lazy to rethink these methods so dictionaries work :D
# jk i think pandas takes care of this for me

def makeProb(array):
    p = [array[0]]
    for i in range(len(array)-1):
        p.append(p[i] + array[i+1])
    return p

def checkProb(check, p):
    for i in p:
        if check <= i:
            return p.index(i)
    raise Exception('check should not be greater than 1')

def getIndex(p):
    r =  float(np.random.rand(1,1))
 #   print r
    return checkProb(r, p)

profile = {}
#print type(profile)

parsed = pd.read_csv('Federal 2000 v2')

attributes = list(parsed.columns.values)[1:]

# number of profiles
total = len(parsed[attributes[0]])

histograms = []
for att in attributes:
    hist = parsed[att].value_counts()
    histograms.append(hist)

for ind, hist in enumerate(histograms):
    name = hist.index.tolist()
#    print ind, attributes[ind]
    values = hist.tolist()
    percent = []
    if values:
        percent = [float(x) / float(total) for x in values]
        prob = makeProb(percent)
        ###print prob
        index = getIndex(prob)
        while name[index] is ' ' or name[index] is '  ' or name[index] is '   ':
            index = getIndex(prob)
        profile[attributes[ind]] = name[index]
    else:
        #print attributes[ind]
        profile[attributes[ind]] = 'NaN'

print profile
