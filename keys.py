
citz = {
    1: "United States",
    2: "Russia",
    3: "Syria", 
    4: "Mexico",
    5: "China",
    6: "Jamaica"
}


edu = {
    1: "Did not finish high school",
    2: "Finished high school, or have a GED",
    3: "Some College",
    4: "Finished College",
    5: "Finished Graduate School",
    6: "Did trade or vocational school"
}

gender = {
    0 : 'Male',
    1 : 'Female',
}

marriage = {
    1: "Single",
2: "Married",
3: "Cohabitating",
4: "Divorced",
5: "Widowed",
6: "Separated"
}

offense = {
1: "Murder",
2: "Sexual Assault",
3: "Drug Trafficking",
4: "Drug Possesion",
5: "Bribery",
6: "Vandalism",
7: "Stalking",
8: "Petty Theft"
}

race = {
    1: "White/Caucasian",
2: "Black",
3: "American Indian or Alaskan Native",
4: "Asian or Pacific Islander",
7: "Hispanic",
9: "Hispanic"
}

emp = {
    1: "Employed",
    0: "Unemployed"
}

attr = {
    "Citizenship": citz,
    'Education': edu,
    'Gender': gender,
    'Marital Status': marriage,
    'Offense': offense,
    'Race': race,
    'Employment': emp
}

months = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}


def readable_dob(string_val): #i forgot about negative step, oh well
    string_val += ' '
    if string_val[-5:-3] == '19':
        month = months[int(string_val[-7:-5])]
        return month + ' ' + string_val[-9:-7] + ', ' + string_val[-5:-1]
    else:
        month = months[int(string_val[-5:-3])]
        return month + ' ' + string_val[-3:-1] + ', ' + string_val[-9:-5]

def dob_to_int(string_val): #Month Day, Year
    reverse_month_map = {v: k for k,v in months.items()}
    month_str, day_str, year_str = str.split(string_val)
    day_str = str.split(day_str, ',')[0]
    month_str = str(reverse_month_map[month_str])
    if len(month_str) == 1:
        month_str = '0' + month_str
    return 2016 - int(year_str)
    #return int(month_str+day_str+year_str)
    


def translate_int_to_string(name, int_val):
    if name == 'Date of Birth':
        return readable_dob(str(int_val))
    if name in attr:
        if int_val in attr[name]:
            return attr[name][int_val]
    return 'Other'    

def translate_string_to_int(name, str_val):
    if str_val == 'Other':
        return -1
    if name == 'Zipcode':
        return str_val
    if name == 'Date of Birth':
        return dob_to_int(str_val)
    if "Prior" in name:
        return str_val
    if name in attr:
        reverse_map = {v:k for k,v in attr[name].items()}
        if str_val in reverse_map:
            return reverse_map[str_val]
    if name == 'Min' or name == 'Max':
        return str_val
    raise Exception
