import operator
import copy
from readfile import *
from find_length_1 import *
from prefix_scan import *

def getList(S, sorted_length, min_sup, length):
    l = []
    count = 0
    for x in sorted_length:
        count = 0
        for i in range(0, len(S)):
            for e in S[i]:
                if x in e:
                    count += 1
                    break
        if count/length >= min_sup[x]:
            l.append(x)
    return l

debug = 0
output = 1

if debug == 0:
    datafileName = "data.txt"
    parafileName = "para.txt"

    datalist = [x for x in range(1,50)]     ## data range: 1-49
    #datalist = [x*10 for x in range(1,10)]   ## data range: 10-90
    length = len(datalist)

    table0 = readData(datafileName)         ## table0 is a dictionary, index start with 1
    min_sup = readPara(parafileName)        ## min_sup is a list 

    SDC = min_sup[length]                   ## SDC is the last number in min_sup
    del min_sup[length]


    min0 = {datalist[i]:min_sup[i] for i in range(0, len(datalist))}                ## minimal support for each item, measured as float ( a dictionary )
    minForEach = find_length_1(table0, datalist, min0 )                             ## real support for each item, measured as count  ( a dictionary )
    min1 = {key:value/len(table0) for key, value in minForEach.items()}             ## real support for each item, measured as float ( a dictionary )
    length1 = { key: value for key, value in min1.items() if value >= min0[key] }   ## (frequent items) length1 is a dictionary 

    frequentItemsMinsup = {key:min0[key] for key in length1.keys()}
    sorted_length1 = sorted(frequentItemsMinsup, key=frequentItemsMinsup.get)	    ## sort the dict according to the value and return a list of keys

    res = {x:{} for x in sorted_length1}                            ## result format: {prefix: {length: [lists]}}
    counts = {str([[x]]):minForEach[x] for x in minForEach.keys()}  ## count for each result
    
    ##-------------------get sequence S that contains Ik and satisfy the SDC restriction--------------
    indexP = 0
    for p in sorted_length1:
        S = renew_table_Sk(table0, p, min1, SDC)    ## return sequences that contains p, also remove items that does not satisfy the SDC restriction

        #sorted_list = [x for x in sorted_length1 if x >= p]     ## find items that after p in the sorted_length1
        sorted_list = sorted_length1[indexP:]
        L = getList(S, datalist, min0, len(table0))          ## get a list of prefix

        #print("p={}, L={}".format(p,L))

        ##-----for S, find all frequent item set------
        for x in L:
            d = prefix_scan([[x]], 1, S, min0, len(table0), p, counts, SDC, min1)  ## for each prefix, run prefix_scan, the add to result
            for i in d.keys():
                if i not in res[p]:
                    res[p][i] = d[i]
                else:
                    for e in d[i]:
                        if e not in res[p][i]:
                            res[p][i].append(e)
        indexP += 1

    result = {x:[] for x in range(1,10)}
    if output == 1:
        for i in res.keys():            ## contain x
            for j in res[i].keys():     ## length j
                for e in res[i][j]:
                    if e not in result[j]:
                        result[j].append(e)

    for i in result.keys():
        if len(result[i]) > 0:
            print("Sequences of length {}, {} in total".format(i, len(result[i])))
            for e in result[i]:
                print("{}:{}".format(e, counts[str(e)]))
            print("\n")

##----------------------------------------------------


