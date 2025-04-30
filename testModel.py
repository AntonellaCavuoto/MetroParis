# testo il modello
from model.fermata import Fermata
from model.model import Model
model = Model()
model.buildGraph()
print("Num nodi:", model.getNumNodi())
print("Num archi:", model.getNumArchi())

print("***")
f = Fermata(2, "Abbesses", 2.33855, 48.8843)
nodesBFS = model.getBFSNodesFromTree(f)
# for n in nodesBFS:
#     print(n)

print("***")
nodesDFS = model.getDFSNodesFromTree(f)
# for n in nodesDFS:
#     print(n)

print("***")
nodesBFSEdges = model.getBFSNodesFromEdges(f)
# for n in nodesBFSEdges:
#     print(n)

print("***")
nodesDFSEdges = model.getDFSNodesFromEdges(f)
# for n in nodesDFSEdges:
#     print(n)

model.buildGraphPesato()
archiMaggiori = model.getArchiPesoMaggiore()
for a in archiMaggiori:
    print(a)


