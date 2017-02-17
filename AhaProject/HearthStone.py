import random

sample = [0,1,1,1,1,1,1,1,1,1,1,1,2,2,2,3,3,4,4,4,5,5,5,5,6,6,8,10]
randomPick = [0,1,2]
result = []
count = 99999
for i in range(0,count):
    t = random.sample(sample,3)
    t.sort()
    p = random.sample(randomPick,1)[0]
    r = t[p]
    result.append(r)

def totalPoints(x,y):
    return x+y

total = reduce(totalPoints,result)
print "After %d Test"%len(result)
print "Total Heal Point Is %d,Average Is %f"%(total,total/count)
