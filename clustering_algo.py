import sys
input = lambda : sys.stdin.readline().rstrip()

# input interface
file_in = sys.argv[1]
n = int(sys.argv[2])
Eps = int(sys.argv[3])
MinPts = int(sys.argv[4])

# Setting database
database = []
database2 = []
clusters = [[]]
result = []

# Open input.txt
print("Opening input")
with open(file_in, 'r') as reader:
    for row in reader:
        obj = list(map(float, row.split('\t')))
        obj[0] = int(obj[0])
        obj.append(0)
        database.append(obj)

# RangeQuery Function
def RangeQuery(p, Eps):
    inRange = []
    for i in range(len(database)):
        if (((database[i][1]-p[1])**2+(database[i][2]-p[2])**2)<=(Eps**2)):
            inRange.append(database[i][0])
    return inRange

# DBSCAN algorithm
for k in range(len(database)):
    # print("Number K:", k)
    if database[k][3] != 0: # Skip if defined
        continue
    N = RangeQuery(database[k], Eps) 
    # print("N: ", N)
    if len(N) < int(MinPts):
        database[k][3] = -1 # Assign to Noise
        continue
    clusters.append([])
    c = len(clusters)-1
    database[k][3] = c
    S = N[:]
    # print("S: ", S)
    S.remove(k)
    for q in S:
        if database[q][3] == -1:
            database[q][3] = c
        if database[q][3] != 0:
            continue
        N = RangeQuery(database[q], Eps)
        database[q][3] = c
        if len(N) < int(MinPts):
            continue
        S += N

for i in database:
    if i[3]==-1:
        continue
    clusters[i[3]].append(i[0])
clusters.pop(0)
# print("Clusters: ", clusters)
if len(clusters) > n:
    clusters.sort(key=lambda c: len(c), reverse=True)

for i in range(n):
    output_name = 'input' + file_in[5] + '_cluster_' + str(i) + '.txt'
    f = open(output_name, 'w')
    for j in clusters[i]:
        f.write(str(j) + '\n')
    f.truncate(f.tell()-2)
    f.close()

print("Complete!")