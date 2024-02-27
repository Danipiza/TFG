# Python program showing 
# abstract base class work 
from abc import ABC, abstractmethod 



class Funcion(ABC):
    maximos=[]      # double[]. Valores maximos de los elementos de los individuos
    minimos=[]      # double[]. Valores minimos
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

    def __init__(self, maximos, minimos):
        self.opt=True
        #self.maximos=[10.0 for i in range(tam_genes)]
        self.maximos=maximos
        self.minimos=minimos
    
    # overriding abstract method 
    def fitness(self, nums):        
        return (pow(nums[0], 2) + 2 * pow(nums[1], 2))
    
    # overriding abstract method 
    def cmp(self, a, b): 
        if a>b: return a
        else : return b

    # overriding abstract method 
    def cmpPeor(self, a, b): 
        if a<b: return a
        else : return b
