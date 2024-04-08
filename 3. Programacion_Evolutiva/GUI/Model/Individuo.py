import random


class Gen:
    def __init__(self, l, v):
        self.v = []

        if v is not None: self.v=[(v[i]) for i in range(len(v))]
        else: self.v=[(random.randint(0,1)) for i in range(l)]

class Individuo:
    def __init__(self, num, tam_genes, xMax, xMin, ind):
        self.genes=[]
        self.xMax=[]
        self.xMin=[]
        if ind is not None:
            self.genes=[(Gen(l=None,v=ind.genes[i].v)) for i in range(len(ind.genes))]
            
            self.xMax=ind.xMax
            self.xMin=ind.xMin
        else:
            self.genes = [(Gen(tam_genes[i],v=None)) for i in range(num)]            
            self.xMax=xMax
            self.xMin=xMin

        self.fitness=0
        self.fenotipo=[]
        self.calcular_fenotipo()

    def bin2dec(self, gen):
        ret=0
        cont=1
        for i in range(len(gen.v)-1,-1,-1):
            if gen.v[i]==1:
                ret+=cont
            cont*=2
        
        return ret

    def calcular_fenotipo(self):
        self.fenotipo=[]    
        for i in range(len(self.genes)):
            self.fenotipo.append(self.calcular_fenotipo_cromosoma(i))
        

    def calcular_fenotipo_cromosoma(self, i):
        return self.xMin[i]+self.bin2dec(self.genes[i])*((self.xMax[i]-self.xMin[i])/((2**len(self.genes[i].v))-1))

    def print_individuo(self):
        for c in self.genes:
            for a in c.v:
                print(a, end=" ")
        print()