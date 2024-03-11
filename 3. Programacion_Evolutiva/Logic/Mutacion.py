import sys
import os
import random

sys.path.append(os.path.abspath("Model"))

from Model import Individuo

class Mutacion:
    def __init__(self, p):
        self.p=p
    
    def mut_basicaBin(self, selec):
        ret=[]
        for ind in selec:
            act=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind)
            for c in range(len(ind.genes)):
                for j in range(len(ind.genes[c].v)):
                    if random.random()<self.p:
                        act.genes[c].v[j]=(act.genes[c].v[j]+1)%2
            ret.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=act))
        return ret
