from itertools import takewhile, repeat
import json

def rawbigcount(filename):
    f = open(filename, 'r')
    bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
    #f.close()
    return sum( buf.count(b'\n') for buf in bufgen if buf )

def percentage(up, down):
    print up,'/',down, float(up)/float(down)*100, '%'


fname = "03450-0001-Data.txt"

total = rawbigcount(fname)
file = open(fname, "r")

content = file.readlines()
content = [x.rstrip("\n") for x in content]

felonies = {}
violent = {}
drug = {}
sex = {}

check = 1

def my_sum(a_l):
    curr_sum = 0
    bad = [9, 99, 999]
    for i in a_l:
        temp = int(i)
        if not temp in bad:
            curr_sum += temp 
    return curr_sum

for x in content:
    #print x
    #x = content[28]
    f = my_sum([x[191:192] , x[192:193] , x[193:194] , x[194:195] , x[197:199] , x[199:202] , x[204:205] , x[205:207] , x[210:212] , x[212:214] , x[214:215] , x[215:216]] )
    v = my_sum([x[183:184] , x[184:185] , x[185:186] , x[186:187] , x[195:196] , x[196:197] , x[202:203] , x[203:204]] )
    d = my_sum([x[207:208] , x[208:210]] )
    s = my_sum([x[187:188] , x[188:189] , x[189:190] , x[190:191]] )

    #if f == 50:
     #   print check ,'**********************************'
        #break
    #print f

    if not f in felonies:
        felonies[f] = 1
    else:
        felonies[f] += 1
    
    if not v in violent:
        violent[v] = 1
    else:
        violent[v] += 1
    
    if not d in drug:
        drug[d] = 1
    else:
        drug[d] += 1
    
    if not s in sex:
        sex[s] = 1
    else:
        sex[s] += 1

    percentage(check, total)
    check += 1

a_list = [felonies, violent, drug, sex]

with open('hists.txt', 'w') as ff:
    ff.write(json.dumps(a_list))
