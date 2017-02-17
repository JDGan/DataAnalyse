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
