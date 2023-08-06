""" Remove double instances of cells (and the unused vertices) """
import sys
import os
""" import modules from larcc/lib """
sys.path.insert(0, os.path.expanduser('~/projects/lar-cc/lib/py'))
from larcc import *
from mapper import evalStruct

""" Generation of Struct object and transform to LAR model pair """
cubes = larCuboids([10,10,10],True)
V = cubes[0]
FV = cubes[1][-2]
CV = cubes[1][-1]
bcells = boundaryCells(CV,FV)
BV = [FV[f] for f in bcells]
VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS((V,BV))))

block = Model((V,BV))
struct = Struct(10*[block, t(10,0,0)])
struct = Struct(10*[struct, t(0,10,0)])
struct = Struct(3*[struct, t(0,0,10)])
W,FW = struct2lar(struct)

VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS((W,FW))))

""" Remove the double instances of cells """
cellDict = defaultdict(list)
for k,cell in enumerate(FW):
   cellDict[tuple(cell)] += [k]
FW = [list(key) for key in cellDict.keys() if len(cellDict[key])==1]

VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS((W,FW))))

""" Remove the unused vertices """
print "len(W) =",len(W)
V,FV = larRemoveVertices(W,FW)
print "len(V) =",len(V)

