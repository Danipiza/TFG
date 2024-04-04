import random

class GenReal:
    def __init__(self, l, v):
        self.v = []

        if v is not None: self.v=[(v[i]) for i in range(len(v))]
        else: self.v=[(random.randint(0,1)) for i in range(l)]

class IndividuoReal:
    def __init__(self, aviones, vInd):
        self.v=[]
        self.fitness=0.0

        if vInd is not None:            
            for i in range(len(vInd)):
                self.append(vInd[i])
        else:
            self.init(aviones)

      
          

    def init(self, aviones):
        self.v=[]
        for i in range(aviones):		
            self.v.append(i)
		
        # shuffle
        for i in range(aviones-1,0,-1):
            j=random.randint(0, i)  
            temp=self.v[i]
            self.v[i]=self.v[j]
            self.v[j]=temp
        			
	


    def print_individuo(self):
        for c in self.genes:
            for a in c.v:
                print(a, end=" ")
        print()