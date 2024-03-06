import random

class Cruce:
    def __init__(self, p):
        self.p=p    # int
    
    def cruce_monopuntoBin(self, selec):
        """
        selec:  Individuo[]
        """
        ret=[] # Individuo
        n=len(selec)
        if n%2==1:
            ret.append(selec[n-1])
            n-=1
        
        long_genes = []
        corte_max=-1
        for gen in selec[0].genes:
            long_genes.append(len(gen))
            corte_max+=len(gen)

        i=0
        while i<n:
            ind1=selec[i]
            ind2=selec[i+1]

            if random.random() < self.p :                
                corte=random.randint(0,corte_max)
                #print(i, "Cruzados en:",corte)
                cont=0
                j=0
                
                for k in range(corte+1):
                    #print("I1:", ind1.genes[cont][j],"I2:",ind2.genes[cont][j])                    
                    tmp=ind1.genes[cont][j]
                    ind1.genes[cont][j] = ind2.genes[cont][j]
                    ind2.genes[cont][j] = tmp
                    j+=1
                    if j == long_genes[cont]:
                        cont+=1
                        j = 0
            ret.append(ind1)
            ret.append(ind2)
            i+=2
					

        return ret
    
    def cruce_uniforme():
        # TODO
        return ""