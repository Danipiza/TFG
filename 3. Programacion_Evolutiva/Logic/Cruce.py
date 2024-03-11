import sys
import os
import random

sys.path.append(os.path.abspath("Model"))


from Model import Individuo

class Cruce:
    def __init__(self, p):
        self.p=p    # int
    
    def cruce_monopuntoBin(self, selec):
        n=len(selec)
        ret=[]
        if n%2==1:
            ret.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[n-1]))
            n-=1
        
        long_genes=[len(selec[0].genes[i].v) for i in range(len(selec[0].genes))]
        corte_maximo=-1
        for l in long_genes:
            corte_maximo+=l
        i=0

        ind1=[]
        ind2=[]
        while i<n:
            ind1=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i])
            ind2=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i + 1])
            print("  (ANTES): ", end="") 
            ind1.print_individuo()
            print("  (ANTES): ", end="") 
            ind2.print_individuo()
            
            rand=random.random()
            if rand<self.p:                                               
                corte=random.randint(1,corte_maximo)
                print("({}) CORTA EN: {}".format(i,corte))
                cont=0
                j=0
                for k in range(corte):
                    tmp=ind1.genes[cont].v[j]
                    ind1.genes[cont].v[j]=ind2.genes[cont].v[j]
                    ind2.genes[cont].v[j]=tmp
                    j+=1
                    if j==long_genes[cont]:
                        cont+=1
                        j=0
            else: print("({}) NO CORTA".format(i))   
            
            print("(DESPUES): ", end="") 
            ind1.print_individuo()
            print("(DESPUES): ", end="") 
            ind2.print_individuo()
            
            ret.append(ind1)
            ret.append(ind2)
            i += 2               
        
        print("Cruce:")
        for ind in ret:
            ind.print_individuo()
        
        return ret
    
    def cruce_uniforme():
        # TODO
        return ""