import pandas as pd

fname = "03496-0001-Data.txt"

file = open(fname, "r")

content = file.readlines()
content = [x.rstrip("\n") for x in content]

parsed = []

for x in content:
    y = {}
    y.update({'Date of Birth': x[489:497]})  # DDMMYYYY, 1012001 = Missing
    y.update({'Gender': x[497:498]})         # 0 = Male, 1 = Female
    y.update({'Race': x[488:489]})           # 1 = White/Caucasian, 2 = Black, 3 = American Indian/Alaska Native
                                             # 4 = Asian/Pacific Islander, 5 = Mutil-racial, 6 = Other
    y.update({'Armed Career Criminal Status': x[417:418]})
                                             # 0 = Not applied, 1 = applied
    y.update({'Career Offender Status': x[418:419]})
                                             # 0 = Not applied, 1 = applied
    y.update({'Citizenship': x[419:422]})    # Check booklet aka add later
    y.update({'Highest edu': x[435:437]})    # 0 = None, 1-11 = number of years completed, 12 = High school
                                             # 13-15 = years in college, 16 = college grad, 21 = GED
                                             # 22 = Trade/vocational deg, 23 = associate, 24 = Grad
                                             # 31 = Some elementary, 32 = some high, 33 = some trade/vocational
                                             # 34 = some college, 35 = some grad, 36 = military training, 37 = Middle/jr high
    y.update({'Marital Status': x[446:447]}) # 1 = single, 2 = married, 3 = Cohabitating, 4 = divorced, 5 = widowed, 6 = separated
    y.update({'District': x[402:404]})       # as listed in reports

    parsed.append(y)

print (y)
