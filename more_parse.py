import pandas as pd
from itertools import takewhile, repeat

def rawbigcount(filename):
    f = open(filename, 'r')
    bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
    #f.close()
    return sum( buf.count(b'\n') for buf in bufgen if buf )

def percentage(up, down):
    print up,'/',down, float(up)/float(down)*100, '%'


fname = "09317-0006-Data.txt"

total = rawbigcount(fname)
file = open(fname, "r")

content = file.readlines()
content = [x.rstrip("\n") for x in content]

parsed = pd.DataFrame.from_csv('data_2.csv')

#del parsed['Unnamed: 0.1']

attributes = list(parsed.columns.values)

# number of profiles
total = len(parsed[attributes[0]])

#parsed = parsed.assign(Offense_Type=['']*total)

print(len(parsed.columns.values))

check = 1

for x in content:
	y = {
        'Date of Birth': x[14:22],
		'Gender': x[45:46],
		'Race': x[43:44],
		'Current Status Supervision Status': '',
		'# Priors': '',		
        'Drug Type': '',
		'Drug Amount': '',
		'Statutory Offense Grade': '',
		'Type of Incarceration': '',
		'Length of Incarceration': '',
		'Restitution Amount': '',
		'Height/Weight': '',
		'Armed Career Criminal Status': '',
		'Career Offender Status': x[605:606],
		'Citizenship': x[49:51],
		'Education': x[46:48],
		'Marital Status': '',
		'Previous Sentencing Time': '',
		'Cost of Bail': '',
		'Warrants': '',
		'District': x[402:404],
		'Offense': x[54:56]
   		}
	#print(len(y.keys()))
	parsed.loc[-1] = y
	parsed.index += 1
	percentage(check, total)
	check += 1

parsed.to_csv('data.csv')