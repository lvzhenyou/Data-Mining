import copy
from find_length_1 import *
from readfile import *

def build_projection( table0, prefix, situation, lastprefix, SDC, min1 ):  ## situation1: <{prefix},{x}>; situation2: <{prefix, x}>
    testT = {0: [[4, 33]], 1: [[33], [4], [22], [22]]}
    table = copy.deepcopy(table0)   ## protect the original table
    projected_db = {}
    cnt = 0
    index = 0
    #for i in range(0, len(table)):                      ## for each sequence set in the whole table
    for i in table.keys():                      ## for each sequence set in the whole table
        if situation==2 and len(table[i])>0 :           ## if we are looking for <{prefix,x}>
            e = table[i][0]                             ## check the first sequence in first sequence set
            if ((len(e)!= 1) and (prefix in e) and ((lastprefix in e and e.index(lastprefix)==0) or (0 in e))):
                if e.index(prefix) != len(e)-1:
                    projected_db[index] = [ [0] + e[2:len(e)]]
                    for x in range(1,len(table[i])):
                        projected_db[index].append(table[i][x])
                else:
                    if len(table[i]) > 1:               ## here, check if the number of sequences is larger than 1 first
                        projected_db[index] = [table[i][1]]
                        if len(table[i]) > 2:
                            for x in range(2, len(table[i])):
                                projected_db[index].append(table[i][x])
                index += 1
        if situation!=2 and len(table[i])>0:
            for e in table[i]:                          ## for each sequence in the sequence set
                if prefix in e:                         ## find the first place of the prefix
                    if situation==1:                    ## if we are looking for <{prefix},{x}>
                        if 0 in e:
                            continue
                    prefix_index = e.index(prefix)
                    if prefix_index < len(e):       ## if prefix belongs to the itemset
                        projected_db[index] = [ [0] + e[prefix_index+1:len(e)]]
                    e_index = table[i].index(e)
                    if e_index < len(table[i]):
                        if index not in projected_db.keys():
                            projected_db[index] = [table[i][e_index+1]]
                            for x in range(e_index+2, len(table[i])):
                                projected_db[index].append(table[i][x])
                        else:
                            for x in range(e_index+1, len(table[i])):
                                projected_db[index].append(table[i][x])
                        index += 1
                    break
            cnt += 1
    #return projected_db;
    return checkSDC( projected_db, prefix, SDC, min1)

##-------------build projected database, test pass -------------

