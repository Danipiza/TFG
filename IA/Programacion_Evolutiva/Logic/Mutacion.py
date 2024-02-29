import random

class Mutacion:
    def __init__(self, p):
        self.p=p
    
    def mut_basicaBin(self, selec):
        ret=[]

        for ind in selec:            
            for i in range(ind.num):
                for j in range(len(ind.genes[i])):
                    if random.random() < self.p:                        
                        ind.genes[i][j]=(ind.genes[i][j]+1)%2

            ret.append(ind)

        return ret
