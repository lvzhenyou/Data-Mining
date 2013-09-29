from readfile import *
from find_length_1 import *
from build_projection import *
import copy

def check(p, add, table, situation):   ## check after adding a new item to the sequence, if the min_sup can be satisfied, test pass
    count = 0
    F = 0
    for i in range(0, len(table)):
        F = 0
        for e in table[i]:
            if situation==1:    ## situation 1: if add == e[0]; <{prefix, prefix}>
                if e[0] == add:
                    count += 1
                break
            if situation==2:    ## situation 2: if prefix == e[0] or e[0]==0; <{prefix, add}> 
                if (p==e[0] or e[0]==0) and len(e) > 1 and e[1] == add:
                    count += 1
                    break
            if situation==3:    ## situation 3: if predix != e[0] and e[0]!=0; <{prefix},{add}>
                if e==table[i][0] and p!=e[0] and e[0]!=0 and add in e:
                    count += 1
                    F = 1
                if F!=1 and e!=table[i][0] and add in e:
                    count += 1
                    break
    return count

def sequence(prefix, t, min0, totalLen, cp, counts):
    res = []
    checkset = {}   ## store check results, avoid duplicate check
    l1 = len(prefix)
    p1 = prefix[l1-1]
    l2 = len(p1)
    p = p1[l2-1]    ## get the last item in the prefix
    s = 0
    for i in range(0, len(t)):  ## for each sequence set in the whole table
        for e in t[i]:          ## for each sequence in the sequence set
            for x in e:         ## for each item in the sequence
                if x > 0:
                    s = 0
                    if x==p and e==t[i][0] and x==e[0]:                       ## situation 1 ({prefix, prefix}): if the current item equals to p, and they are both in t[i][0]
                        count = check(p, x, t, 1)
                        s = 1
                    elif x!=p and e==t[i][0] and (p==e[0] or e[0]==0):        ## situation 2 ({prefix, x}): if current item not equals to p and they are both in t[i][0]
                        if str(x)+'_' not in checkset.keys():
                            count = check(p, x, t, 2)
                            checkset[str(x)+'_'] = count
                        else:
                            count = checkset[str(x)+'_']
                        s = 2
                    elif ((e==t[i][0] and p!=e[0] and e[0]!=0) or (e!=t[i][0])): ## situation 3 ({prefix}{x}): x in t[i][0] but !=p and e[0] is not 0 or p, or x not in t[i][0]
                        if e[0]!=p:   
                            if str(x) not in checkset.keys():
                                count = check(p, x, t, 3)
                                checkset[str(x)] = count
                            else:
                                count = checkset[str(x)]
                            s = 3
                        else:  
                            count1 = check(p, x, t, 3)
                            count2 = check(p, x, t, 2)
                            s = 4
                    
                    if s!=4 and count/totalLen >= min0[cp]:    ## check if minsup(x) >= minsup(p)
                        np = copy.deepcopy(prefix)
                        if s==1 or s==2:
                            np[l1-1].append(x)
                        if s==3:
                            np.append([x])
                        if np not in res:
                            res.append(np)
                            if str(np) not in counts.keys():
                                counts[str(np)] = count
                    if s==4:                                    ## situation such as for p=10, [0,20][10,60], when x = 10
                        if count1/totalLen >= min0[cp]:
                            np = copy.deepcopy(prefix)
                            np.append([x])
                            if np not in res:
                                res.append(np)
                                if str(np) not in counts.keys():
                                    counts[str(np)] = count1
                        if count2/totalLen >= min0[cp]:
                            np = copy.deepcopy(prefix)
                            np[l1-1].append(x)
                            if np not in res:
                                res.append(np)
                                if str(np) not in counts.keys():
                                    counts[str(np)] = count2
    return res

def getKey(prefix):
    if len(prefix)==1:
        p = prefix[0]
        l = len(p)
        return str([prefix[0][0:l-1]])
    else:
        l = len(prefix)
        p = prefix[0:l-1]
        if len(prefix[l-1]) == 1:
            return str(p)
        else:
            p1 = prefix[l-1]
            l1 = len(prefix[l-1])
            p.append(p1[0:l1-1])
            return str(p)
            

def prefix_scan(prefix, length, table, min0, totalLen, cp, counts, SDC, min1):     ## prefix: a list, [[x]], the current building prefix [in the prefix list which need to be explored]; 
    result = {1:[prefix]}   ## for every input prefix, create length-1 sequence with this prefix, ignore the [real prefix must in set] here first
    index = 0
    projection_db = {}
    while length <= len(result):
        prefix = result[length][index]      ## get the next prefix with length
        l1 = len(prefix)
        p1 = prefix[l1-1]   ## get the last itemset in the sequence
        l2 = len(p1)        ## the length of the last itemset
        p = p1[l2-1]        ## get the last item in the prefix
        if length==1:
            t = build_projection(table, p, 0, None, SDC, min1)              ## init the project database
            projection_db[str(prefix)] = t
            length_2 = sequence(prefix, t, min0, totalLen, cp, counts)      ## find all length-2 sequences
            if len(length_2) > 0:   
                result[length+1] = length_2
            else:
                break;      ## if length-2 sequence is empty, then break and return
        else:
            t = {}
            key = getKey(prefix)
            if l2 > 1:      ## if the last itemset contains more than one element
                t = build_projection(projection_db[str(key)], p, 2, p1[l2-2], SDC, min1)
            else:           ## if the last itemset contains only one element
                t = build_projection(projection_db[str(key)], p, 1, None, SDC, min1)    ## build project database for <{prefix},{x}>
            if len(t)!=0:
                projection_db[str(prefix)] = t
                if length+1 not in result.keys():
                    res = sequence(prefix, t, min0, totalLen, cp, counts)
                    if len(res) > 0:
                        result[length+1] = res
                else:
                    res = sequence(prefix, t, min0, totalLen, cp, counts)
                    if len(res) > 0:
                        for x in res:
                            result[length+1].append(x)

        if index == len(result[length])-1:  ## if this prefix is the last one in the current length
            length += 1
            index = 0
        else:
            index += 1
     
    for i in result.keys():     ## remove sequences which do not contain cp
        for e in result[i]:
            F = 0
            for x in e:
                if cp in x:
                    F = 1
                    break
        if F==0:
            result[i].remove(e)
    result = {x:result[x] for x in result.keys() if result[x]}
    return result

