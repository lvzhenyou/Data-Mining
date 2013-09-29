import copy

def find_frequent_1_itemset(T): #simply count the num of each item
    C = {}
    for t in T:
        for i in t:
            if i in C.keys():
                C[i] += 1
            else:
                C[i] = 1
    return C

def candidate_gen(F):           #generate candidates C
    C = []
    k = len(F[0]) + 1
    for f1 in F:
        for f2 in F:
            if f1[k-2] < f2[k-2]:
                c = copy.copy(f1)
                c.append(f2[k-2])
                flag = True
                for i in range(0,k-1):
                    s = copy.copy(c)
                    s.pop(i)
                    if s not in F:
                        flag = False
                        break
                if flag and c not in C:
                    C.append(c)
    return C

def is_set_include(A,B):        # check if set B includes set A
    if len(A) > len(B):
        return False
    else:
        for a in A:
            if a not in B:
                return False
    return True

def apriori(T, minsup):
    C = []
    init = find_frequent_1_itemset(T)
    keys = init.keys()
    C.append(sorted(init, key=lambda key:key))  # sort according to keys
    print("C1 = ",C)
    n = len(T)
    F = [[]]
    for f in C[0]:
        if init[f] * 1.0/n >= minsup:
            F[0].append([f])
    print("F1 = ",F[0]) # all itemsets when k=1
    k = 1
    while F[k-1] != []:
        newC = candidate_gen(F[k-1])
        print('C{} = {}'.format(k+1,newC))
        C.append(newC)
        F.append([])    # add an empty set to F first
        for c in C[k]:
            count = 0
            for t in T: # for each itemset
                if is_set_include(c,t): # if set c is in set t
                    count += 1;
            if count * 1.0/n > minsup:
                F[k].append(c)
        print('F{} = {}'.format(k+1,F[k]))
        k += 1
    RES = []
    for f in F:
        for x in f:
            RES.append(x)
    return RES

T = [["Beef","Chicken","Milk"],["Beef","Cheese"],["Cheese","Boots"],["Beef","Chicken","Cheese"],["Beef","Chicken","Clothes","Cheese","Milk"],["Chicken","Clothes","Milk"],["Chicken","Milk","Clothes"]]

minsup = 0.3

RES = apriori(T,minsup)

