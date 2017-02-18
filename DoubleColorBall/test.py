# coding=utf-8

import Analyser , time
from DataCenter import load_ball_data_from_file

print time.clock()
dataSourceFileNames = [
"2016.txt",
"2015.txt",
"2014.txt",
"2013.txt",
"2012.txt",
"2011.txt",
"2010.txt",
"2009.txt",
"2008.txt",
"2007.txt",
"2006.txt",
"2005.txt",
"2004.txt",
"2003.txt",]

dataSourceFileNames.reverse()
domain = []
for name in dataSourceFileNames:
    domain += load_ball_data_from_file(name)

print time.clock()
# 通过下面的算法计算出最佳表现或最差表现的双色球号码
# 随机算法
# b = Analyser.random_optimize(domain,Analyser.analyse_ball_data)
# 坡度算法
# b = Analyser.hill_climb(domain,Analyser.analyse_ball_data)
# 快速退火算法
# b = Analyser.annealing_optimize(domain,Analyser.analyse_ball_data)
# 遗传算法
# b = Analyser.genetic_optimize(domain, Analyser.analyse_ball_data)

bestResults = Analyser.genetic_optimize(domain
, Analyser.analyse_ball_data
, Analyser.generateRandomBallData
# , Analyser.randomSubDataSet
, False)

for i in range(10):
    b = bestResults[i]
    print b[1] , " +$:%d" % b[0] , "-$:%d" % (len(domain) * 2)
print time.clock()

# 分析历史数据，尝试用前面中奖数最少的号码计算所有奖金和，结果显示，全部都是比较少的奖金，无法实现突破
# sample = []
# for i in range(13):
#     sample += load_ball_data_from_file(dataSourceFileNames[i])
#
# rs = genetic_optimize(sample,analyse_ball_data,False)
# for d in rs:
#     v = analyse_ball_data(d[1],domain)
#     print d[1] , ": %d" % d[0] , v

# print time.clock()
