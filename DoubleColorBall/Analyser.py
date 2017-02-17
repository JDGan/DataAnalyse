# coding=utf-8
from DataCenter import load_ball_data_from_file
import random
import copy
import math
import timeit
import time


def analyse_ball_data(data, domain, check=False):
    s = 0
    """
    6+1 = 70% 5000000
    6 = 30% 2000000
    5+1 = 3000
    4+1,5 = 200
    3+1,4 = 10
    0,1,2+1 = 5
    """
    values = {
        "6+1": 5000000,
        "6": 2000000,
        "5+1": 3000,
        "4+1": 200,
        "5": 200,
        "4": 10,
        "3+1": 10,
        "2+1": 5,
        "1+1": 5,
        "0+1": 5,
        "3": 0,
        "2": 0,
        "1": 0,
        "0": 0
    }

    i = 0
    for d in domain:
        same = list(set(d[0:6]).intersection(set(data[0:6])))
        red_count = len(same)
        count = "%d" % red_count
        blue_count = 0
        if (d[6] == data[6]):
            blue_count = 1
            count += "+%d" % blue_count
        if check and values[count] > 0:
            print "中奖方式: ", count, "中奖金额: %d" % values[count], "中奖号码: ", d
        s += values[count]
        i += 1
    return s


RedBalls = []
for i in range(1, 33):
    RedBalls.append(i)
BlueBalls = []
for i in range(1, 16):
    BlueBalls.append(i)


def generateRandomBallData():
    v = random.sample(RedBalls, 6) + random.sample(BlueBalls, 1)
    return v


def random_optimize(domain, costf, count=1000):
    best = 0
    bestRecord = None

    for i in range(count):
        tmp = generateRandomBallData()
        c = costf(tmp, domain)
        if best < c:
            best = c
            bestRecord = tmp
    print best
    return bestRecord


def hill_climb(domain, costf):
    sol = generateRandomBallData()
    best = 0
    while 1:
        neighbors = []
        for j in range(len(domain)):
            i = random.randint(0, 6)
            if sol[i] > domain[j][0]:
                neighbors.append(sol[0:i] + [sol[i] - 1] + sol[i + 1:])
            if sol[i] < domain[j][1]:
                neighbors.append(sol[0:i] + [sol[i] + 1] + sol[i + 1:])
        current = costf(sol, domain)
        best = current
        for j in range(len(neighbors)):
            cost = costf(neighbors[j], domain)
            if cost > best:
                best = cost
                sol = neighbors[j]

        if best == current:
            break
    print best
    return sol


def annealing_optimize(domain, costf, T=10000, cool=0.95, step=1):
    tmp = generateRandomBallData()
    best = 0
    while T > 0.1:
        i = random.randint(0, 6)
        j = random.randint(0, len(domain) - 1)
        dir = random.randint(-step, step)
        tmpB = copy.deepcopy(tmp)
        tmpB[i] += dir
        ea = costf(tmp, domain)
        eb = costf(tmpB, domain)
        best = ea
        if eb > ea or random.random() < pow(math.e, -(ea - eb) / T):
            tmp = tmpB
            best = eb
        T *= cool
    print best
    return tmp


def genetic_optimize(domain, costf, popsize=50, step=1, mutprob=0.4, elite=0.2, maxiter=100):
    # 变异
    def mutate(vec):
        v = copy.deepcopy(vec)
        i = random.randint(0, 6)
        dir = random.randint(-step, step)
        v[i] += dir
        return v

    # 交叉
    def crossover(r1, r2):
        i = random.randint(0, 6)
        r = r1[0:i] + r2[i:]
        return r

    # 构造初始种群
    pop = []
    for i in range(popsize):
        vec = copy.deepcopy(domain[random.randint(0, len(domain) - 1)])
        pop.append(vec)

    # 每一代的胜出者数量
    topelite = int(elite * popsize)

    # 主循环
    scores = []
    for i in range(maxiter):
        scores = [(costf(v, domain), v) for v in pop]
        scores.sort(reverse=True)
        ranked = [v for (s, v) in scores]

        # 从纯粹的胜出者开始
        pop = ranked[0:topelite]

        # 添加变异和配对后的胜出者
        while len(pop) < popsize:
            if random.random() < mutprob:
                # 变异
                c = random.randint(0, topelite)
                pop.append(mutate(ranked[c]))
            else:
                # 交叉
                c1 = random.randint(0, topelite)
                c2 = random.randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))
    print scores[0]
    return scores[0][1]


def genetic_optimize_least(domain, costf, exclude=None, popsize=50, step=1, mutprob=0.4, elite=0.2, maxiter=100):
    # 新变异
    if exclude is None:
        exclude = [[1, 1, 1, 1, 1, 1, 1]]

    def mutate(vec):
        v = copy.deepcopy(vec)
        i = random.randint(0, 6)
        if i == 6:
            r = list(set(BlueBalls).difference(set(v[i:])))
            rep = random.sample(r, 1)
            v[i] = rep[0]
        else:
            r = list(set(RedBalls).difference(set(v[0:6])))
            rep = random.sample(r, 1)
            v[i] = rep[0]
        return v

    # 交叉
    def crossover(r1, r2):
        i = 6
        v = []
        sample_red = list(set(r1[0:i]).union(set(r2[0:i])))
        sample_blue = list(set(r1[i:]).union(set(r2[i:])))
        v += random.sample(sample_red, i)
        v += random.sample(sample_blue, 1)
        if v in exclude:
            v = crossover(r1, r2)
        return v

    # 构造初始种群
    pop = []
    for i in range(popsize):
        vec = copy.deepcopy(domain[random.randint(0, len(domain) - 1)])
        pop.append(vec)

    # 每一代的胜出者数量
    topelite = int(elite * popsize)

    # 主循环
    scores = []
    for i in range(maxiter):
        ls = [','.join(str(i) for i in v) for v in pop]
        vs = list(set(ls))
        ss = [list(int(i) for i in v.split(',')) for v in vs]

        scores = [(costf(v, domain), v) for v in ss]
        scores.sort()
        ranked = [v for (s, v) in scores]

        # 从纯粹的胜出者开始
        pop = ranked[0:topelite]

        # 添加变异和配对后的胜出者
        while len(pop) < popsize:
            if random.random() < mutprob:
                # 变异
                c = random.randint(0, topelite)
                pop.append(mutate(ranked[c]))
            else:
                # 交叉
                c1 = random.randint(0, topelite)
                c2 = random.randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))
    return scores


print time.clock()

domain = load_ball_data_from_file("2015.txt")
domain += load_ball_data_from_file("2014.txt")
domain += load_ball_data_from_file("2013.txt")
domain += load_ball_data_from_file("2012.txt")
domain += load_ball_data_from_file("2011.txt")
domain += load_ball_data_from_file("2010.txt")
domain += load_ball_data_from_file("2009.txt")
domain += load_ball_data_from_file("2008.txt")
domain += load_ball_data_from_file("2007.txt")
domain += load_ball_data_from_file("2006.txt")
domain += load_ball_data_from_file("2005.txt")
domain += load_ball_data_from_file("2004.txt")
domain += load_ball_data_from_file("2003.txt")

print time.clock()
# b = random_optimize(domain,analyse_ball_data)
# b = hill_climb(domain,analyse_ball_data)
# b = annealing_optimize(domain,analyse_ball_data)
# b = genetic_optimize(domain, analyse_ball_data)

a = [[1,2,3],[2,3,1],[3,2,1],[1,2,3]]


ls = [','.join(sorted(str(i) for i in v)) for v in a]
vs = list(set(ls))
ss = [list(int(i) for i in v.split(',')) for v in vs]
print ss


# bestResults = genetic_optimize_least(domain, analyse_ball_data)
# # b = bestResults[0]
# for i in range(10):
#     b = bestResults[i]
#     print b[1] , " +$:%d" % b[0] , "-$:%d" % (len(domain) * 2)
# print time.clock()

# v = analyseBallData(t,domain)
# print v
