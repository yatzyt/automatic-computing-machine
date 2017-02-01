import pandas as pd
from itertools import (takewhile,repeat)

def rawbigcount(filename):
    f = open(filename, 'r')
    bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen if buf )

def percentage(up, down):
    print up,'/',down, float(up)/float(down)*100, '%'
	

fname = "03496-0001-Data.txt"

total = rawbigcount(fname)

file = open(fname, "r")

content = file.readlines()
content = [x.rstrip("\n") for x in content]

parsed = pd.DataFrame({ 'Date of Birth':[], 'Gender':[], 'Race':[] ,'Current Status Supervision Status':[], '# Priors':[], 'Drug Type':[], 'Drug Amount':[], 'Statutory Offense Grade':[], 'Type of Incarceration':[], 'Length of Incarceration':[], 'Restitution Amount':[], 'Height/Weight':[], 'Armed Career Criminal Status Applied':[], 'Career Offender Status Applied':[], 'Citizenship':[], 'Education':[], 'Marital Status':[], 'Previous Sentencing Time':[], 'Cost of Bail':[], 'Warrants':[], 'District':[] })

check = 1

for x in content:
    y = {
		'Date of Birth': x[489:497],
		'Gender': x[497:498],
		'Race': x[488:489],
		'Current Status Supervision Status': 'NaN',
		'# Priors': 'NaN',
		'Drug Type': 'NaN',
		'Drug Amount': 'NaN',
		'Statutory Offense Grade': 'NaN',
		'Type of Incarceration': 'NaN',
		'Length of Incarceration': 'NaN',
		'Restitution Amount': 'NaN',
		'Height/Weight': 'NaN',
		'Armed Career Criminal Status': x[417:418],
		'Career Offender Status': x[418:419],
		'Citizenship': x[419:422],
		'Education': x[435:437],
		'Marital Status': x[446:447],
		'Previous Sentencing Time': 'NaN',
		'Cost of Bail': 'NaN',
		'Warrants': 'NaN',
		'District': x[402:404]
		}
    parsed.loc[-1] = y
    parsed.index = parsed.index + 1
	#parsed.append(y, ignore_index=True)
    percentage(check, total)
    check = check + 1

parsed.to_csv('Federal 2000')
