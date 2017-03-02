import json

import numpy as np
import pandas as pd

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
    #return p.index
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

month_to_day = {
    31: [1,3,5,7,8,10,11], 
    30: [4,6,9,11]
}

def make_dob(): # year + month + day
    year = np.random.randint(1920, 2001)
    month = np.random.randint(1,13)
    day = 0
    if month in month_to_day[31]:
        day = np.random.randint(1,32)
    elif month in month_to_day[30]:
        day = np.random.randint(1,31)
    else:
        if year % 4 == 0:
            day = np.random.randint(1,30) # potential leap day
        else:
            day = np.random.randint(1,29)
    year = str(year)
    if month < 10:
        month = "0" + str(month)
    else: month = str(month)
    if day < 10:
        day = "0" + str(day)
    else: day = str(day)
    return year+month+day


def make_profile():
    parsed = pd.read_csv('data.csv', low_memory=False, index_col=0)

    attributes = list(parsed.columns.values)
    #print (attributes)

    # number of profiles
    #total = len(parsed[attributes[0]])

    histograms = []
    for att in attributes:
        #print (att, len(parsed[att]))
        hist = parsed[att].value_counts()
        #print (sum(hist.tolist()))  
        histograms.append(hist)

    #print (parsed['Career Offender Status'])


    profile = {}

    # ind is index
    for ind, hist in enumerate(histograms):
        #len_of_att = len(parsed[attributes[attributes.index(hist.name)]])
        name = hist.index.tolist()
        values = hist.tolist()
        percent = []
        if values:
            if hist.name != 'Date of Birth':
                percent = [float(x) / float(sum(values)) for x in values]
                prob = makeProb(percent)
                index = getIndex(prob)
            # random spaces in parsed
                while name[index] == ' ' or name[index] == '  ' or name[index] == '   ':
                    index = getIndex(prob)
            #if hist.name == 'Date of Birth':
                #print (name[index])
                actual_readable_thing = keys.translate_int_to_string(hist.name, int(name[index]))
                profile[attributes[ind]] = actual_readable_thing
                if hist.name == 'Race':
                    zip = getZipCode(int(name[index]))
                    profile['Zipcode'] = zip
            else:
                dob = make_dob()
                readable_dob = keys.translate_int_to_string(hist.name, dob)
                profile[attributes[ind]] = readable_dob

        else:
            profile[attributes[ind]] = 'NaN'

    want_to_remove = []
    for k in profile.keys():
        if profile[k] == 'NaN':
            want_to_remove.append(k)


    for r in want_to_remove:
        profile.pop(r)
    
    return profile

make_profile()

#print(profile)
'''
with open('profile_2.json', 'w') as f:
    f.write(json.dumps([profile]))


with open('profile_2.json', 'r') as f:
    loaded = json.loads(f.read())

with open('profile_2.json', 'w') as f:
    f.write(json.dumps(loaded + [profile]))
    '''
