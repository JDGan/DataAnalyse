
import re

class Result:
    id = ""
    date = ""
    s_data = ""
    red = []
    blue = 0

    def __init__(self ,str = ""):
        self.red = [0 ,0 ,0 ,0 ,0 ,0]
        if str != "" :
            self.decodeString(str)

    def decodeSData(self):
        r_balls = self.s_data.split(",")
        if len(r_balls) == 6 :
            for i in range(0,len(r_balls)-1):
                self.red[i]=int(r_balls[i])
            b_balls = r_balls[5].split("|")

            if len(b_balls) == 2 :
                self.red[5] = int(b_balls[0])
                self.blue = int(b_balls[1])

    def decodeString(self ,str):
        cs = str.split(" ")
        es = []
        for r in cs:
            if (len(r)>0):
              es.append(r)

        if len(es) == 3:
            self.date = es[2].strip('\r\n')
            self.id = es[0]
            self.s_data = es[1]
            self.decodeSData()

    def __str__(self):
        return "%s %s %r %d"%(self.id,self.date,self.red,self.blue)

def loadBallData(fileName):
    results = []
    f = file(fileName)
    for line in f:
        r = Result(line)
        results.append(r)
    return results



def loadBallDataFromFile(filename):
    ret = []
    f = file(filename)
    for line in f:
        cs = line.split(" ")
        es = []
        for r in cs:
            if (len(r)>0):
              es.append(r)
        data = es[1]
        arr = re.split('[,|]',data)
        ret.append(arr)
    return ret

def formatBallDataFile(filename):
    s = ""
    f = file(filename)
    l = 0
    for line in f:
        if l == 0:
            s += line.split("	")[0]
            s += "    "
        elif l == 1:
            arr = line.split("	")
            newS = splitWithIndex(arr[0],2)
            s += ",".join(newS)
            s += "|"+arr[1]
        l += 1
        if l == 4:
            l = 0
    save(filename,s)
    return

def save(filename, contents):
  fh = open(filename, 'w')
  fh.write(contents)
  fh.close()

def splitWithIndex(string,i):
    arr = []
    newMX = i
    lastMX = 0
    while lastMX < len(string):
        s = string[lastMX:newMX]
        arr.append(s)
        lastMX = newMX
        newMX += i
    return arr

formatBallDataFile("2016.txt")
