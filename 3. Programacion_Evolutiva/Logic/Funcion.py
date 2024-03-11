# Python program showing 
# abstract base class work 
from abc import ABC, abstractmethod 

import math



class Funcion(ABC):
    xMax=[]      # double[]. Valores maximos de los elementos de los individuos
    xMin=[]      # double[]. Valores minimos
    opt=True        # booleano. maximizar: True, minimizar: False

    @abstractmethod
    def fitness(self,nums): 
        pass
    
    @abstractmethod
    def cmp(self,a,b): 
        pass

    @abstractmethod
    def cmpPeor(self,a,b): 
        pass

class Funcion1(Funcion):

    def __init__(self):
        self.opt=True
        self.xMax=[10,10]
        self.xMin=[-10,-10]
    
    def fitness(self, nums):        
        return ((nums[0]**2)+2*(nums[1]**2))
    
    def cmp(self, a, b): 
        if a>b: return a
        else: return b

    def cmpPeor(self, a, b): 
        if a<b: return a
        else: return b

class Funcion2(Funcion):

    def __init__(self):
        self.opt=True
        self.xMax=[0,0]
        self.xMin=[-10,-6.5]
    
    # TODO comprobar
    def fitness(self, nums):        
        return  math.sin(nums[1])*math.pow(math.exp(1-math.cos(nums[0])),2) + \
                math.cos(nums[0])*math.pow(math.exp(1-math.sin(nums[1])),2) + \
                ((nums[0]-nums[1])**2)
    
    def cmp(self, a, b): 
        if a<b: return a
        else: return b

    def cmpPeor(self, a, b): 
        if a>b: return a
        else: return b

class Funcion3(Funcion):

    def __init__(self):
        self.opt=True
        self.xMax=[10,10]
        self.xMin=[-10,-10]
    
    # TODO comprobar
    def fitness(self, nums):        
        exp = abs(1-(math.sqrt(nums[0]**2+nums[1]**2))/math.pi)
        ret = math.sin(nums[0])*math.cos(nums[1])*math.exp(exp)
        return -abs(ret)
    
    def cmp(self, a, b): 
        if a<b: return a
        else: return b

    def cmpPeor(self, a, b): 
        if a>b: return a
        else: return b


class Funcion4(Funcion):

    def __init__(self, num_genes):
        self.opt=True
        self.d=num_genes
        self.xMax=[]
        self.xMin=[]
        for i in range(num_genes):
            self.xMax.append(math.pi)
            self.xMax.append(0)
    
    # TODO comprobar
    def fitness(self, nums):        
        ret = 0.0        
        for i in range(1,self.d+1):		
            sin1=math.sin(nums[i-1])                           
            radians=(i*(nums[i-1]**2))/math.pi
            comp=math.sin(radians)
            ret+=sin1*(comp**20)

        return ret*-1
    
    def cmp(self, a, b): 
        if a<b: return a
        else : return b

    def cmpPeor(self, a, b): 
        if a>b: return a
        else : return b


class Funcion5(Funcion):

    def __init__(self,num_genes):
        self.opt=False
        self.d=num_genes
        self.xMax=[]
        self.xMin=[]
        for i in range(num_genes):
            self.xMax.append(math.pi)
            self.xMax.append(0)
    
    # TODO comprobar
    def fitness(self, nums):        
        ret = 0.0        
        for i in range(1,self.d+1):		
            sin1=math.sin(nums[i-1])                           
            radians=(i*(nums[i-1]**2))/math.pi
            comp=math.sin(radians)
            ret+=sin1*(comp**20)

        return ret*-1
    
    def cmp(self, a, b): 
        if a<b: return a
        else : return b

    def cmpPeor(self, a, b): 
        if a>b: return a
        else : return b
