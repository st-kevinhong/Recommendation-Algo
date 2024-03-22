import sys
import os
import pandas as pd
import numpy as np
import math
input = lambda : sys.stdin.readline().rstrip()

# input interface
database_1 = sys.argv[1]
database_2 = sys.argv[2]
result = sys.argv[3]

# read train & test data
train = pd.read_csv(database_1, sep='\t')
test = pd.read_csv(database_2, sep='\t')

# ID3 calculation functions
def info(dataIn):
    counts = dataIn.iloc[:, -1].value_counts()
    prob = counts / len(dataIn)
    return -(prob * np.log2(prob)).sum()

def infoAfter(dataIn, attr):
    counts = dataIn[attr].value_counts()
    v = counts.index.values
    prob = counts / len(dataIn)
    newSub = list(map(lambda j: info(dataIn[dataIn[attr] == v[j]]), range(len(v))))
    return np.sum(prob*newSub)

def splitInfo(dataIn, attr):
    counts = dataIn[attr].value_counts()
    v = counts.index.values
    prob = counts / len(dataIn)
    return -(prob * np.log2(prob)).sum()

# formula
def gainRatio(dataIn, attr):
    return info(dataIn) - infoAfter(dataIn,attr) / splitInfo(dataIn,attr)

# get maximum of gainRatio
def denotator(dataIn):
  gainRatios = []
  for attr in dataIn.columns[:-1]:
      gainRatios.append(gainRatio(dataIn, attr))
  gainRatios = np.array(gainRatios)
  return dataIn.columns[gainRatios.argmax()]

# Node as dictionary form
Node = {'candidate' : '', 'attr' : '', 'child' : {}}

# Decision Tree Creation
def DT(dataIn, Node): #D as input
    # print("D:", D)
    # print("Node:", Node)
    newNode = {'candidate' : '', 'attr' : '','child' : {}}
    if dataIn.shape[1] == 0:
        return None

    elif dataIn.shape[1] == 1:
        x, counts = np.unique(dataIn, return_counts=True)
        index, _ = max(enumerate(counts), key=lambda x: x[1])
        return x[index]
  
    elif len(dataIn.iloc[:,-1].unique()) == 1:
        return np.unique(dataIn.values[:,-1:])[0]

    else:
        Node['candidate'] = denotator(dataIn)
        newNode['attr'] = Node['candidate']
        x = np.unique(dataIn[Node['candidate']])
        for c in x:
            Child_Node = newNode.copy()
            if len(Child_Node['child']) != 0:
                Child_Node['child'] = {}
            subset = dataIn[dataIn[Node['candidate']] == c]
            subset = subset.drop(columns=[Node['candidate']])
            (Node['child'])[c] = (DT(subset, Child_Node),len(subset))
    
    return Node

# Initialize Node for Decision Tree
Node = DT(train, Node)

# put test to predict
def Predict(dTree, test):
  if isinstance(dTree, tuple) and not isinstance(dTree[0], dict):
        return dTree[0] # leaf node - conclusion
  else:
    if isinstance(dTree, tuple):
        dTree = dTree[0]
    # Recursion to get into leaf node
    if test[dTree['candidate']] in dTree['child'].keys():
        next_node = dTree['child'][test[dTree['candidate']]]
        return Predict(next_node, test)
    else:
        max_key = max(dTree['child'].items(), key=lambda x: x[1][1])[0]
        return Predict(dTree['child'][max_key], test)

# addRow to test sets
addRow = [Predict(Node, row) for i, row in test.iterrows()]

# get file out
test[train.keys()[-1]] = np.array(addRow)
test.to_csv(result, mode='w', sep='\t', index=False)
