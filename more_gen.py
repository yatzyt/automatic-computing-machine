import numpy as np
import pandas as pd
import json
import keys


def makeProb(array):
    p = [array[0]]
    for i in range(len(array)-1):
        p.append(p[i] + array[i+1])
    return p

def checkProb(check, p):
    for i in p:
        if check <= i:
            return p.index(i)
    raise Exception(check)
    #'check should not be greater than 1')

def getIndex(p):
    r =  float(np.random.rand(1,1))
    return checkProb(r, p)

zipcodes = {
    2:[45110, 45113], # Black
    #3:[45113, 45138], # Hispanic
    1:[45131, 45244], # White
    4:[45126] # Asian
}

def getZipCode(race):
    if race in zipcodes:
        if len(zipcodes[race]) > 1:
            return zipcodes[race][np.random.randint(0,2)]
        else:
            return zipcodes[race][0]
    else:
        return 45100

parsed = pd.read_csv('data.csv', low_memory=False, index_col=0)

attributes = list(parsed.columns.values)
print (attributes)

# number of profiles
total = len(parsed[attributes[0]])

profiles = []

histograms = []
for att in attributes:
    hist = parsed[att].value_counts()
    histograms.append(hist)

#print (parsed['Career Offender Status'])

   
profile = {}

# ind is index
for ind, hist in enumerate(histograms):
    name = hist.index.tolist()
    values = hist.tolist()
    percent = []
    if values:
        percent = [float(x) / float(total) for x in values]
        prob = makeProb(percent)
        index = getIndex(prob)
        # random spaces in parsed
        while name[index] == ' ' or name[index] == '  ' or name[index] == '   ':
            index = getIndex(prob)
        if hist.name == 'Date of Birth':
            print (name[index])
        actual_readable_thing = keys.translate_int_to_string(hist.name, int(name[index]))
        profile[attributes[ind]] = actual_readable_thing
        if hist.name == 'Race':
            zip = getZipCode(int(name[index]))
            profile['Zipcode'] = zip
    else:
        profile[attributes[ind]] = 'NaN'

want_to_remove = []
for k in profile.keys():
    if profile[k] == 'NaN':
        want_to_remove.append(k)


for r in want_to_remove:
    profile.pop(r)

#print(profile)
'''
with open('profile_2.json', 'w') as f:
    f.write(json.dumps([profile]))
'''

with open('profile_2.json', 'r') as f:
    loaded = json.loads(f.read())

with open('profile_2.json', 'w') as f:
    f.write(json.dumps(loaded + [profile]))