from itertools import (takewhile, repeat)
import pandas as pd
import numpy as np

def rawbigcount(filename):
    f = open(filename, 'r')
    bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen if buf )

def percentage(up, down):
    print up,'/',down, float(up)/float(down)*100, '%'


parsed = pd.read_csv('Federal 2000')

fname = '03496-0001-Data.txt'

total = rawbigcount(fname)

myFile = open(fname, 'r')

content = myFile.readlines()
content = [x.rstrip('\n') for x in content]

parsed['Offense'] = np.random.randn(total)
parsed['Offense'].astype(str)

index = 0

for x in content:
    crime = x[354:356]
    parsed['Offense'][index] = crime
    index = index + 1
    percentage(index, total)

parsed.to_csv('Federal 2000 v2')
