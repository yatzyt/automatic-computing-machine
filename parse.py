import pandas as pd
from itertools import (takewhile,repeat)

def rawbigcount(filename):
    f = open(filename, 'r')
    bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen if buf )

def percentage(up, down):
    print float(up)/float(down)*100, '%'

fname = "03496-0001-Data.txt"

total = rawbigcount(fname)

file = open(fname, "r")

content = file.readlines()
content = [x.rstrip("\n") for x in content]

parsed = pd.DataFrame({ 'Date of Birth':[], 'Gender':[], 'Race':[] ,'Current Status Supervision Status':[], '# Priors':[], 'Drug Type':[], 'Drug Amount':[], 'Statutory Offense Grade':[], 'Type of Incarceration':[], 'Length of Incarceration':[], 'Restitution Amount':[], 'Height/Weight':[], 'Armed Career Criminal Status Applied':[], 'Career Offender Status Applied':[], 'Citizenship':[], 'Education':[], 'Marital Status':[], 'Previous Sentencing Time':[], 'Cost of Bail':[], 'Warrants':[], 'District':[] })

check = 1

for x in content:
    y = {}
    y.update({'Date of Birth': x[489:497]})
    y.update({'Gender': x[497:498]})
    y.update({'Race': x[488:489]})
    y.update({'Current Status Supervision Status': []})
    y.update({'# Priors': []})
    y.update({'Drug Type': []})
    y.update({'Drug Amount': []})
    y.update({'Statutory Offense Grade': []})
    y.update({'Type of Incarceration': []})
    y.update({'Length of Incarceration': []})
    y.update({'Restitution Amount': []})
    y.update({'Height/Weight': []})
    y.update({'Armed Career Criminal Status': x[417:418]})
    y.update({'Career Offender Status': x[418:419]})
    y.update({'Citizenship': x[419:422]})
    y.update({'Education': x[435:437]})
    y.update({'Marital Status': x[446:447]})
    y.update({'Previous Sentencing Time': []})
    y.update({'Cost of Bail': []})
    y.update({'Warrants': []})
    y.update({'District': x[402:404]})
    parsed.loc[-1] = y
    parsed.index = parsed.index + 1
    print percentage(check, total)
    check = check + 1

parsed.to_hdf('Federal 2000', 'parsed')
