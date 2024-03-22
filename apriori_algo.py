import sys
import os
import math
from itertools import chain, combinations
input = lambda : sys.stdin.readline().rstrip()

# Setting database
database = []
elements = []
itemset = []
only_itemset = []
copy_itemset = []

min_support = 0
total_transaction = 0
new_length = 0

# Setting Input
min_support_input = sys.argv[1]
file_in = sys.argv[2]
file_out = sys.argv[3]

# Open input.txt
print("Opening input")
with open(file_in, 'r') as reader:
    for row in reader:
        transaction = list(map(int, row.split('\t')))
        total_transaction += 1
        for i in transaction:
            if i not in elements:
                elements.append(i)
                itemset.append([i, 1])
                
                itemset.sort(key=lambda x:x[0])
            else:
                idx = elements.index(i)
                itemset[idx][1] += 1
        database.append(transaction)

# Initial Itemset
print("Setting initial itemset")
elements.sort()
min_support = int(min_support_input) * 0.01 * total_transaction
print("Minimum support :", min_support)
itemset = list(filter(lambda x : x[1] >= min_support, itemset))

# Apriori Algorithm
print("Running apriori algorithm")
new_L = []
k=1
while True:
    k+=1
    L=list(combinations(elements,k))
    for i in L:
        temp = list(i)
        temp_count = 0
        for j in database:
            if set(temp) <= set(j):
                temp_count += 1
        if temp_count >= min_support:
            temp.append(temp_count)
            new_L.append(temp)

    if len(new_L)<=1 or k==min_support:
        break
    itemset+=new_L
    new_length += len(new_L)
    new_L = []

# Create subsets without count
for i in itemset:
    only_itemset.append(i[:-1])
    copy_itemset.append(i[:-1])

total_cnt = 0
f = open(file_out, 'w')
# Calculate Associate & Confidence
print("Calculate Associate & confidence")
for i in only_itemset:
    for j in copy_itemset:
        if set(i) <= set(j):
            continue
        elif sorted(i+j) not in copy_itemset:
            continue
        else:
            union = sorted(i+j)
            idx = only_itemset.index(union)
            associate = itemset[idx][len(union)] / total_transaction * 100
            i_idx = only_itemset.index(i)
            confidence = itemset[idx][len(union)] / itemset[i_idx][len(i)] * 100
            asc = '{:.2f}'.format(round(associate,2))
            conf = '{:.2f}'.format(round(confidence,2))
            total_cnt += 1
            # print(set(i), set(j), asc , conf, sep="\t")
            f.write(str(set(i))+'\t'+str(set(j))+'\t'+str(asc)+'\t'+str(conf)+'\n')
f.truncate(f.tell()-2)
f.close()
print("Output Createing Complete!")
print("Total Count:", total_cnt)
