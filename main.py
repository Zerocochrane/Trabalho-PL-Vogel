import collections
from collections import defaultdict

demandDict = {}
supplyDict = {}
costsDict = {}
demandTotal = 0
supplyTotal = 0
dummyDemand = 0
dummySupply = 0
numFabricas = input("Digite quantas fontes de suprimento: ")
numLojas = input("Digite quantas fontes de destino: ")

# Recebe os valores do usuario e os coloca nos dicionarios
ding = 27 - numFabricas
for i in range(27, ding, -1):
    n = raw_input("Digite a quantidade de material disponivel na fonte " + str(28-i) + " : ")
    supplyTotal = supplyTotal + int(n)
    supplyDict[chr(i+63)] = int(n)

for i in range(int(numLojas)):
    m = input("Digite a quantidade de material que a loja " + str(i+1) + " quer : ")
    demandTotal = demandTotal + int(m)
    demandDict[chr(i+65)] = int(m)

if demandTotal < supplyTotal:
    t = supplyTotal - demandTotal
    demandTotal = demandTotal + t
    demandDict[chr(numLojas+65)] = t
    dummyDemand = 1

if supplyTotal < demandTotal:
    t = demandTotal - supplyTotal
    supplyTotal = supplyTotal + t
    supplyDict[chr(90-numFabricas)] = t
    dummySupply = 1


dong = 27 - numFabricas
for i in range(27, dong, -1):
    temp = {}
    for j in range(int(numLojas)):
        b = input("Digite o custo entre os caminhos " + chr(i+63) + " - " + chr(j+65) + ": ")
        temp[chr(j+65)] = int(b)
    if dummyDemand == 1:
        temp[chr(numLojas+65)] = 99999999
    costsDict[chr(i+63)] = temp

if dummySupply == 1:
    temp = {}
    for i in range(int(numLojas)):
        temp[chr(i+65)] = 99999999
    costsDict[chr(90-numFabricas)] = temp

cols = sorted(demandDict.iterkeys())
res = dict((k, defaultdict(int)) for k in costsDict)
g = {}
for x in supplyDict:
    g[x] = sorted(costsDict[x].iterkeys(), key=lambda g: costsDict[x][g])
for x in demandDict:
    g[x] = sorted(costsDict.iterkeys(), key=lambda g: costsDict[g][x])
 
while g:
    d = {}
    for x in demandDict:
        d[x] = (costsDict[g[x][1]][x] - costsDict[g[x][0]][x]) if len(g[x]) > 1 else costsDict[g[x][0]][x]
    s = {}
    for x in supplyDict:
        s[x] = (costsDict[x][g[x][1]] - costsDict[x][g[x][0]]) if len(g[x]) > 1 else costsDict[x][g[x][0]]
    f = max(d, key=lambda n: d[n])
    t = max(s, key=lambda n: s[n])
    t, f = (f, g[f][0]) if d[f] > s[t] else (g[t][0], t)
    v = min(supplyDict[f], demandDict[t])
    res[f][t] += v
    demandDict[t] -= v
    if demandDict[t] == 0:
        for k, n in supplyDict.iteritems():
            if n != 0:
                g[k].remove(t)
        del g[t]
        del demandDict[t]
    supplyDict[f] -= v
    if supplyDict[f] == 0:
        for k, n in demandDict.iteritems():
            if n != 0:
                g[k].remove(f)
        del g[f]
        del supplyDict[f]
 
for n in cols:
    print "\t", n,
print
cost = 0

for g in sorted(costsDict):
    print g, "\t",
    for n in cols:
        y = res[g][n]
        if y != 0:
            print y,
        if costsDict[g][n] != 99999999:
            cost += y * costsDict[g][n]
        print "\t",
    print

print "\n\nTotal Cost = ", cost
