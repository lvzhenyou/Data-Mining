import re

def readPara(fileName):             ## read para file, store the para data in a list
    testFile = open(fileName, 'r')
    line = testFile.readline()
    res = []
    while line:
        data = line.split(' ')
        res.append(float(data[2][:-1]))
        line = testFile.readline()
    testFile.close()
    return res

def readData(fileName):             ## read sequence data file, store the sequence in a dic
    testFile = open(fileName, 'r')
    line = testFile.readline()
    res = {}
    cnt = 0
    pat = re.compile(r"\{(.*?)\}",re.X) ## match partten
    while line:                         ## <{25, 37, 47}{48}>
        res[cnt] = []
        for x in pat.findall(line):     ## x in list ['25, 37, 47', '48']
            tmplist = []
            t = x.split(', ')
            for y in t:                 ## y in string '25, 37, 47'
                tmplist.append(int(y))
            res[cnt].append(tmplist)
        cnt = cnt + 1
        line = testFile.readline()
    testFile.close()
    return res

