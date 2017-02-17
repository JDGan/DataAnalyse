# coding=utf-8
import DataLoader , random , math ,copy

""" CostMethod """
def analyseBallData(data ,domain):
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
        "6+1":5000000,
        "6":2000000,
        "5+1":3000,
        "4+1":200,
        "5":200,
        "4":10,
        "3+1":10,
        "2+1":5,
        "1+1":5,
        "0+1":5,
        "3":0,
        "2":0,
        "1":0,
        "0":0
    }

    for d in domain :
        same = list(set(d.red).intersection(set(data.red)))
        redCount = len(same)
        count = "%d"%redCount
        blueCount = 0
        if(d.blue == data.blue) :
            blueCount = 1
            count += "+%d"%blueCount

        s += values[count]
    return s

RedBalls = []
for i in range(1,33):
    RedBalls.append(i)
BlueBalls = []
for i in range(1,16):
    BlueBalls.append(i)

""" 随机算法 """
def randomoptimize(domain,costf,count = 1000):
    best = 0
    bestRecord = None
    tmp = DataLoader.Result("")
    for i in range(count):
        tmp.red = random.sample(RedBalls,6)
        tmp.blue = random.sample(BlueBalls,1)[0]
        c = costf(tmp,domain)
        if best < c :
            best = c
            bestRecord = tmp
    print best
    print bestRecord
    return bestRecord

def hillClimb(domain,costf):
    tmp = DataLoader.Result("")
    tmp.red = random.sample(RedBalls,6)
    tmp.blue = random.sample(BlueBalls,1)[0]
    while 1:
        neighbors = []
        for j in range(len(domain)):
            if tmp.blue > domain[j].blue:
                n = DataLoader.Result("")
                n.blue = tmp.blue-1
                for i in range(len(tmp.red)):
                    n.red[i] = tmp.red[i]-1
                neighbors.append(n)
            if tmp.blue < domain[j].blue:
                n = DataLoader.Result("")
                n.blue = tmp.blue+1
                for i in range(len(tmp.red)):
                    n.red[i] = tmp.red[i]+1
                neighbors.append(n)
        current = costf(tmp,domain)
        best = current
        for j in range(len(neighbors)):
            cost = costf(neighbors[j],domain)
            if cost > best:
                best = cost
                tmp = neighbors[j]

        if best == current:
            break
    print best
    print tmp
    return tmp

def annealingoptimize(domain,costf,T=10000,cool=0.85,step=1):
    tmp = DataLoader.Result("")
    tmp.red = random.sample(RedBalls,6)
    tmp.blue = random.sample(BlueBalls,1)[0]
    best = 0
    while T>0.1:
        i = random.randint(0,7)
        j = random.randint(0,len(domain)-1)
        dir = random.randint(-step,step)
        tmpB = copy.deepcopy(tmp)
        if i < 6 :
            tmpB.red[i] += dir
        else:
            tmpB.blue += dir
        ea = costf(tmp,domain)
        eb = costf(tmpB,domain)
        best = ea
        if (eb>ea or random.random()<pow(math.e,-(ea-eb)/T)):
            tmp = tmpB
            best = eb
        T = T*cool
    print best
    print tmp
    return tmp

def geneticoptimize(domain,costf,popsize=50,step=1,mutprob=0.2,elite=0.2,maxiter=100):
    # 变异
    def mutate(vec):
        """
        :type vec: Result
        """
        i = random.randint(0,len(domain)-1)
        j = random.randint(0,7)
        dir = random.randint(-step,step)
        if j < 6:
            vec.red[j] += dir
        else:
            vec.blue += dir
        return vec

    # 交叉
    def crossover(r1,r2):
        i = random.randint(0,6)
        r = DataLoader.Result()
        r.red = r1.red[0:i]+r2.red[i:]
        r.blue = r2.blue
        return r

    # 构造初始种群
    pop=[]
    for i in range(popsize):
        vec=domain[random.randint(0,len(domain)-1)]
        pop.append(vec)

    # 每一代的胜出者数量
    topelite = int(elite*popsize)

    # 主循环
    for i in range(maxiter):
        scores = [(costf(v,domain),v) for v in pop]
        scores.sort(reverse=True)
        ranked = [v for (s,v) in scores]

        # 从纯粹的胜出者开始
        pop = ranked[0:topelite]

        #添加变异和配对后的胜出者
        while len(pop)<popsize:
            if random.random()<mutprob:
                # 变异
                c=random.randint(0,topelite)
                pop.append(mutate(ranked[c]))
            else:
                # 交叉
                c1=random.randint(0,topelite)
                c2=random.randint(0,topelite)
                pop.append(crossover(ranked[c1],ranked[c2]))
    for item in scores:
        print item[0]
        print item[1]
    return scores[0][1]


domain = DataLoader.loadBallData("2014.txt")
randomoptimize(domain,analyseBallData,10000)
hillClimb(domain,analyseBallData)
annealingoptimize(domain,analyseBallData)
geneticoptimize(domain,analyseBallData)