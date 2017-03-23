import json
import pandas as pd

f = open('hists.txt', 'r')

a = json.loads(f.readline())

d = a[0]
s_d = sorted(d.items(), key=lambda x: x[1], reverse=True)

print (pd.Series(s_d)[:5])

#print(pd.Series(a[0]))
