import sys
import os
import random

sys.path.append(os.path.abspath("Model"))

from Model import Individuo

class Mutacion:
    def __init__(self, p, tam_elite):
        self.p=p
        self.tam_elite=tam_elite
    
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

    def inversion():
        # TODO
        return ""

    def intercambio():
        # TODO
        return ""
    
    def insercion():
        # TODO
        return ""
    

    
    def heuristica():
        # TODO
        return ""    
    def dfs():
        # TODO
        return ""