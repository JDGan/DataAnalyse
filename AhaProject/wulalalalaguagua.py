# coding=utf-8

import random

def generate_fishes(count):
    if count < 0 :
        return []
    max = count
    if count > 7 :
        max = 7
    fishes = ("寒光智者","鱼人领军","蓝腮战士","老瞎眼")
    sample = []
    for i in range(0,count):
        sample.append(random.sample(fishes,1)[0])
    return sample

def damagesCaculate (fishes):
    blinder = 0
    warrior = 0
    leaderCount = 0
    totalDamge = 0
    for i in range(0,len(fishes)) :
        name = fishes[i]
        print name
        if name == "寒光智者":
           # do nothing
            continue
        elif name == "鱼人领军":
            leaderCount += 1
        elif name == "蓝腮战士":
            warrior += 1
        elif name == "老瞎眼":
            blinder += 1
    totalDamge = (2+len(fishes)-1)*blinder + warrior*2 + leaderCount*2*(blinder+warrior)
    return totalDamge

def input(x,y):
    fishes = generate_fishes(x)
    damage = damagesCaculate(fishes)

    print "damage:%d"%damage
    if damage >= y:
        print "乌拉拉拉拉呱呱"
    else :
        print "讲个笑话：圣骑的斩杀"

input(7,30)
