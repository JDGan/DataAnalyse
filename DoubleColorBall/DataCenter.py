import re

def load_ball_data_from_file(filename):
    ret = []
    f = file(filename)
    for line in f:
        cs = line.split(" ")
        es = []
        for r in cs:
            if len(r) > 0:
                es.append(r)
        data = es[1]
        arr = re.split('[,|]', data)
        list = map(lambda x: int(x), arr)
        ret.append(list)
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
