# coding=utf-8
import time

# 桶算法

def tong(sample,t=10):
    a = time.clock()
    b = []
    for i in range(0,t):
         b.append(0)

    for s in sample:
         b[s] += 1

    for i in range(0,len(b)):
        v = b[i]
        for j in range(0,v):
            print i
    print time.clock()-a

# 冒泡算法
def maopao(sample):
    a = time.clock()
    for i in range(0,len(sample)-1):
        for j in range(0,len(sample)-i-1):
            if sample[j] > sample[j+1]:
                t = sample[j]
                sample[j] = sample[j+1]
                sample[j+1] = t
    print sample
    print time.clock()-a

# 快速排序
def kuaisu(sample):
    t = time.clock()
    def q_sort(left,right):
        if left > right:
            return
        i = left
        j = right
        temp = sample[left]
        while i!=j:
            while sample[j]>=temp and i<j:
                j-=1
            while sample[i]<=temp and i<j:
                i+=1
            if i<j:
                t = sample[i]
                sample[i] = sample[j]
                sample[j] = t
        sample[left] = sample[i]
        sample[i] = temp
        q_sort(left,i-1)
        q_sort(i+1,right)
    q_sort(0,len(sample)-1)
    print sample
    print time.clock()-t

# 扑克游戏
def poker_game(a = [1,2,3,4,5,6,7,8,9,10,11,12,13],b = [13,12,11,10,9,8,7,6,5,4,3,2,1]):
    desktop = []
    print "Game Start"
    def play_card(p=[],player = "no name"):
        if len(p)<=0:
            print player+" LOSE!"
            return False
        else:
            t = p[0]
            p.remove(t)
            gain_card = False
            print "%s plays %d"%(player,t)
            for i in range(0,len(desktop)):
                if desktop[i] == t:
                    p.append(t)
                    d = desktop[i:]
                    d.reverse()
                    p += d
                    del desktop[i:]
                    gain_card = True
                    print "%s gain"%player,d
                    break

            if not gain_card:
                desktop.append(t)
            print "Desktop is",desktop
            return True

    cur = a
    turn = 0
    name = "a"
    while play_card(cur,name):
        turn += 1
        print "Turn %d Over"%turn
        if turn%2 == 1:
            cur = b
            name = "b"
        else:
            cur = a
            name = "a"
    print "Game Over"
    return

# 火柴棍游戏
def sticks(count):
    t = time.clock()
    if count < 4:
        return []
    m = 1
    for i in range(0,count/6-1):
        m *= 10
    result = []

    def need_stick(value):
        dic = [6,2,5,5,4,5,6,3,7,6]
        c = 0
        v = value
        if v == 0 :
            return dic[0]
        while v/10!=0:
            c+=dic[v%10]
            v/=10
        c += dic[v]
        return c

    for i in range(0,m):
        for j in range(0,m):
            if count == need_stick(i)+need_stick(j)+need_stick(i+j)+4:
                result.append((i,j))
                # print "%d+%d=%d"%(i,j,i+j)
    print time.clock()-t
    print result

# 深度优先算法,比较有深度(实现全排列)
def depth_first_search():
    t = time.clock()
    r = []
    a = [0]*10
    book = [0]*10
    n=9

    def dfs(step=1):
        i=0
        if step == n+1:
            x = a[1]*100+a[2]*10+a[3]
            y = a[4]*100+a[5]*10+a[6]
            z = a[7]*100+a[8]*10+a[9]
            if x+y==z:
                r.append((x,y,z))
            return
        for i in range(1,n+1):
            if book[i]==0:
                a[step]=i
                book[i]=1
                dfs(step+1)
                book[i]=0
        return

    dfs()
    print time.clock()-t
    print r

m_step = 99999
def puzzle_castle(puz=[[0,0,1,0],[0,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],target=(3,2)):
    t = time.clock()
    n=len(puz)-1
    m=len(puz[0])-1
    def generate_arr (n,m):
        arr = []
        for i in range(0,n+1):
            arr.append([0]*(m+1))
        return arr

    book = generate_arr(n,m)
    a = puz
    next = [[0,1],[1,0],[0,-1],[-1,0]]
    (p,q) = target

    for pz in puz:
        print pz

    step_tracks = []
# 深度优先算法,比较有深度
    def dfs(x,y,step):
        global m_step
        tx = 0
        ty = 0
        k = 0
        if x==p and y==q:
            step_tracks.append((x,y))
            if step < m_step:
                m_step = step
                print "This is better:"
            print step_tracks
            step_tracks.remove((x,y))
            return
        for k in range(0,4):
            tx=x+next[k][0]
            ty=y+next[k][1]
            if tx<0 or tx>n or ty<0 or ty>m:
                continue
            if a[tx][ty]==0 and book[tx][ty]==0:
                book[tx][ty]=1
                step_tracks.append((x,y))
                dfs(tx,ty,step+1)
                step_tracks.remove((x,y))
                book[tx][ty]=0
        return

    book[0][0]=1
    dfs(0,0,0)
    print "step is %d"%m_step
    print time.clock()-t
    return

def load_puzzle_palace(file_name):
    f = file(file_name)
    arr = []
    for line in f:
        s_arr = [int(c) for c in line if c!='\n']
        arr.append(s_arr)
    return arr


class note:
    x = 0
    y = 0
    f = 0
    s = 0

def puzzle_palace(puz=[[0,0,1,0],[0,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],target=(3,2)):
    t = time.clock()
    n=len(puz)-1
    m=len(puz[0])-1
    def generate_arr (n,m):
        arr = []
        for i in range(0,n+1):
            arr.append([0]*(m+1))
        return arr

    book = generate_arr(n,m)
    a = puz
    next = [[0,1],[1,0],[0,-1],[-1,0]]
    (p,q) = target

    for pz in puz:
        print pz
    return


# testCases
# sample = [1,12,312,3,123,14,1234,123,123,53,25,24,13,1,3,23,12,3123,12,41,24,23,13,12,41,23,1,23,124,123,235,62,342,34,23,542,56,46,457,567,58,68,67,8,456,456,34,5634,52,34,1234,234,23,4,234,234,2,3423,42,34,25,4,56456,45,64,57,76,8,678,67,87,9,678,57,57456,34,34,5345,2,523,412,341,3,123,12,123,143,235,545,5,46,6667,7,8,8,9,7575,56,635,23534,575,6867,979,79,6,856,74,5785,4564]

# tong(sample,t=100000)
# maopao(sample)
# kuaisu(sample)
# poker_game()
# sticks(24)
# depth_first_search()

# arr = load_puzzle_palace("PuzzlePalace")
# puzzle_castle(arr,target=(20,19))