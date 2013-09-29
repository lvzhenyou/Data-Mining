import copy
from readfile import *

def find_length_1(table0, datalist, min_sup):
    C = {}
    cnt = 0
    length = len(table0)                    ## the size of the table
    while cnt < len(datalist):              ## iterate for each item
        cur = datalist[cnt]
        for i in range(0,length):      ## for each sequence set in the whole table 
            for e in table0[i]:             ## for each sequence in the sequence set
                if cur in e:                ## for each item in the sequence
                    if cur in C.keys():
                        C[cur] += 1
                    else:
                        C[cur] = 1
                    break
        cnt += 1
    return C

def checkSDC(t, p, SDC, min1):
    length = len(t)
    for i in range(0, length):
        for e in t[i]:
            indexE = t[i].index(e)
            for x in e:
                if x!=p and x!=0 and abs(min1[p]-min1[x])>SDC:
                    indexX = e.index(x)
                    e[indexX] = -1
            t[i][indexE] = [j for j in e if j!=-1]
    for i in range(0, length):
        t[i] = [x for x in t[i] if x]
    return t

def renew_table_Sk(table0, p, min1, SDC):
    t = copy.deepcopy(table0)
    S0 = {}
    index = 0
    for i in range(0, len(t)):		## for each sequence in the whole table
        F = 0
        for e in t[i]:				## for each sequence in the sequence set
            if p in e:
                F = 1
                break
        if F == 1:
            S0[index] = t[i]
            index += 1
    return checkSDC(S0, p, SDC, min1)
##------------------renew table to obtain Sk, test pass---------------
# Add sequence which contains p into S;
# SDC filter, remove items that does not satisfy the SDC restriction 

