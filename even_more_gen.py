import json
import pandas as pd
import numpy as np

#My Libraries
import keys
from make_histo import *

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

hc_years = [18, 20, 25, 30, 35, 40, 45, 50]

def make_dob(): # year + month + day
    year = 2016 - hc_years[ np.random.randint(0, 8) ] 
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
	
def make_citz():
    my_r = np.random.randint(1, high=101)
    if my_r <= 70:
        return 1
    if my_r <= 76:
        return 2
    if my_r <= 82:
        return 3
    if my_r <= 88:
        return 4
    if my_r <= 94:
        return 5
    return 6

def make_edu():
    e = make_edu_hist()
    vals = e.tolist()
    percent = [float(x) / float(sum(vals)) for x in vals]
    prob = makeProb(percent)
    ind = getIndex(prob)
    return e.index.tolist()[ind]

def make_gen():
    g = make_gender_hist()
    vals = g.tolist()
    percent = [float(x) / float(sum(vals)) for x in vals]
    prob = makeProb(percent)
    ind = getIndex(prob)
    return int(g.index.tolist()[ind])

def make_ms():
    m = make_ms_hist()
    vals = m.tolist()
    percent = [float(x) / float(sum(vals)) for x in vals]
    prob = makeProb(percent)
    ind = getIndex(prob)
    return int(m.index.tolist()[ind])

def make_off():
    my_r = np.random.randint(1, high=9)
    return my_r

off_min_times = {
	1: 235,
	2: 97,
	3: 21,
	4: 15,
	5: 0,
	6: 0,
	7: 27,
	8: 0
}

off_max_times = {
    1: "Life",
	2: "Life",
	3: "Life",
	4: 293,
	5: 121,
	6: 51,
	7: 51,
	8: 16
}


def make_times(offense, f, v, d, s):
    max_ret = off_max_times[offense]
    if not max_ret == 'Life':
        max_ret += (f+v+d+s) * 4
    return off_min_times[offense] + (f+v+d+s) * 4, max_ret

def make_race():
    r = make_race_hist()
    vals = r.tolist()
    percent = [float(x) / float(sum(vals)) for x in vals]
    prob = makeProb(percent)
    ind = getIndex(prob)
    return int(r.index.tolist()[ind])

def make_emp(): # 0 is unemployed
    my_r = np.random.randint(1, high=1001)
    if my_r > 953:
        return 0
    return 1

def prior_helper(my_l):
    curr_l = my_l.tolist()
    curr_name, curr_vals = [], []
    for i in curr_l:
        if i[0] == '4+':
            curr_name.append(4)
        else:
            curr_name.append(int(i[0]))
        curr_vals.append(i[1])
    return curr_name, curr_vals

def make_prior():
    f, v, d, s = make_prior_hist()
    
    name_f, vals_f = prior_helper(f)
    percent = [float(x) / float(sum(vals_f)) for x in vals_f]
    prob = makeProb(percent)
    ind_f = getIndex(prob)
    
    name_v, vals_v = prior_helper(v)
    percent = [float(x) / float(sum(vals_v)) for x in vals_v]
    prob = makeProb(percent)
    ind_v = getIndex(prob)

    name_d, vals_d = prior_helper(d)
    percent = [float(x) / float(sum(vals_d)) for x in vals_d]
    prob = makeProb(percent)
    ind_d = getIndex(prob)

    name_s, vals_s = prior_helper(s)
    percent = [float(x) / float(sum(vals_s)) for x in vals_s]
    prob = makeProb(percent)
    ind_s = getIndex(prob)
    
    return name_f[ind_f], name_v[ind_v], name_d[ind_d], name_s[ind_s]

def make_image_name(id_num):
    return 'mugshot' + str(id_num) + 'f.png'

id_to_name = { 
    #(age, gender, race)
    #gender: 1 = female, 0 = male
    #race: 1 = white, 2 = black, 3 = amer ind, 4 = asian, 9 = hisp
    (18,0,1):[2],
    (18,0,4):[6],
    (18,0,3):[18],
    (18,0,2):[30],
    (20,0,1):[1, 3, 17, 22],
    (20,1,1):[10],
    (20,0,2):[29, 35],
    (20,0,9):[38],
    (25,1,1):[4],
    (25,0,1):[5, 12, 20],
    (25,0,4):[7, 40, 48],
    (25,0,2):[26],
    (25,0,9):[31, 33, 42, 43],
    (25,1,2):[36, 50],
    (30,0,1):[9, 24],
    (30,0,2):[28, 34, 49],
    (30,0,4):[37, 39],
    (35,0,1):[15, 21, 25],
    (35,0,4):[44],
    (40,0,1):[13, 16],
    (40,0,4):[23],
    (40,0,9):[32],
    (40,1,9):[45],
    (45,0,2):[27],
    (45,0,9):[41],
    (45,0,4):[47],
    (50,0,1):[8, 11, 46],
    (50,1,1):[14],
    (50,0,4):[19],
}

def make_race_and_gen(age):
    curr_range = []
    for x in id_to_name.keys():
        if x[0] == age:
            for _ in range(len(id_to_name[x])):
                curr_range.append(x[1:])
    return curr_range[np.random.randint(len(curr_range))]

def make_image(prof):
    p_age = prof['Age']
    p_race = keys.translate_string_to_int('Race', prof['Race'])
    p_gender = keys.translate_string_to_int('Gender', prof['Gender'])
    p_id = (p_age, p_gender, p_race)
    if p_id in id_to_name:
        image_name_arr = id_to_name[p_id]
    else:
        return 'Error'
    return make_image_name(image_name_arr[np.random.randint(len(image_name_arr))])
    
attributes = ['Citizenship', 'Education', 'Gender', 'Marital Status', 'Offense', 'Race', 'Employment', 'Prior felonies', 'Prior violent felonies', 'Prior drug offense', 'Prior sex offenses']

def make_profile():
    profile = {}
    
    # Makes the Date of Birth
    dob = make_dob()
    readable_dob = keys.translate_string_to_int('Date of Birth', keys.translate_int_to_string('Date of Birth', dob))
    profile['Age'] = readable_dob

    # Makes the citizenship
    citz = make_citz()
    readable_citz = keys.translate_int_to_string("Citizenship", citz)
    profile['Citizenship'] = readable_citz

    # Makes the education
    edu = make_edu()
    readable_edu = keys.translate_int_to_string("Education", edu)
    profile['Education'] = readable_edu

    # Makes the gender
    gen, race = make_race_and_gen(readable_dob)
    readable_gen = keys.translate_int_to_string("Gender", gen)
    profile['Gender'] = readable_gen

    # Makes the race
    readable_race = keys.translate_int_to_string("Race", race)
    profile['Race'] = readable_race

    # Makes the image name
    image_name = make_image(profile)
    profile['File Name'] = image_name

    # Makes the Marital Status
    ms = make_ms()
    readable_ms = keys.translate_int_to_string("Marital Status", ms)
    profile['Marital Status'] = readable_ms

    # Makes the Offense
    off = make_off()
    readable_off = keys.translate_int_to_string("Offense", off)
    profile['Offense'] = readable_off

    # Makes the zipcode
    profile['Zipcode'] = getZipCode(race)

    # Makes the Employment rating
    emp = make_emp()
    readable_emp = keys.translate_int_to_string("Employment", emp)
    profile['Employment'] = readable_emp

    # Makes the Prior felonies
    p_f, p_v, p_d, p_s = make_prior()
    profile['Prior felonies'] = p_f

    # Makes the Prior violent felonies
    profile['Prior violent felonies'] = p_v

    # Makes the Prior drug offense
    profile['Prior drug offense'] = p_d

    # Makes the Prior sex offenses
    profile['Prior sex offenses'] = p_s

    # Gives the max and min sentence for the Offense
    min_time, max_time = make_times(off, p_f, p_v, p_d, p_s)
    profile['Min'] = min_time
    profile['Max'] = max_time

    return profile