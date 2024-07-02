# Python program showing 
# abstract base class work 
from abc import ABC, abstractmethod 
from collections import deque
from typing import List, Tuple


import math



class Funcion(ABC):
    xMax=[]      # double[]. Valores maximos de los elementos de los individuos
    xMin=[]      # double[]. Valores minimos
    opt=False        # booleano. maximizar: True, minimizar: False

    @abstractmethod
    def fitness(self,nums): 
        pass
    
    @abstractmethod
    def cmp(self,a,b): 
        pass
    @abstractmethod
    def cmpBool(self,a,b): 
        pass

    @abstractmethod
    def cmpPeor(self,a,b): 
        pass
    @abstractmethod
    def cmpPeorBool(self,a,b): 
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

    def cmpBool(self, a, b): 
        if a>b: return True
        else: return False

    def cmpPeor(self, a, b): 
        if a<b: return a
        else: return b

    def cmpPeorBool(self, a, b): 
        if a<b: return True
        else: return False

class Funcion2(Funcion):

    def __init__(self):
        self.opt=False
        self.xMax=[0,0]
        self.xMin=[-10,-6.5]
    
    def fitness(self, nums):    
        #f(x,y)=sen(y)*exp()    
        return  math.sin(nums[1])*math.pow(math.exp(1-math.cos(nums[0])),2) + \
                math.cos(nums[0])*math.pow(math.exp(1-math.sin(nums[1])),2) + \
                ((nums[0]-nums[1])**2)
    
    def cmp(self, a, b): 
        if a<b: return a
        else: return b

    def cmpBool(self, a, b): 
        if a<b: return True
        else: return False

    def cmpPeor(self, a, b): 
        if a>b: return a
        else: return b

    def cmpPeorBool(self, a, b): 
        if a>b: return True
        else: return False

class Funcion3(Funcion):

    def __init__(self):
        self.opt=False
        self.xMax=[10,10]
        self.xMin=[-10,-10]
    
    def fitness(self, nums):        
        exp=abs(1-(math.sqrt(nums[0]**2+nums[1]**2))/math.pi)
        ret=math.sin(nums[0])*math.cos(nums[1])*math.exp(exp)
        return -abs(ret)
    
    def cmp(self, a, b): 
        if a<b: return a
        else: return b

    def cmpBool(self, a, b): 
        if a<b: return True
        else: return False

    def cmpPeor(self, a, b): 
        if a>b: return a
        else: return b

    def cmpPeorBool(self, a, b): 
        if a>b: return True
        else: return False

class Funcion4(Funcion):

    def __init__(self, num_genes):
        self.opt=False
        self.d=num_genes
        self.xMax=[]
        self.xMin=[]
        for i in range(num_genes):
            self.xMax.append(math.pi)
            self.xMin.append(0)
    
    
    def fitness(self, nums):        
        ret=0.0        
        for i in range(1,self.d+1):		
            sin1=math.sin(nums[i-1])                           
            radians=(i*(nums[i-1]**2))/math.pi
            comp=math.sin(radians)
            ret+=sin1*(comp**20)

        return ret*-1
    
    def cmp(self, a, b): 
        if a<b: return a
        else: return b

    def cmpBool(self, a, b): 
        if a<b: return True
        else: return False

    def cmpPeor(self, a, b): 
        if a>b: return a
        else: return b

    def cmpPeorBool(self, a, b): 
        if a>b: return True
        else: return False


class FuncionA(Funcion):

    def __init__(self, aviones, pistas, tipo_avion, TEL):
        self.sep = [[1, 1.5, 2],
                    [1, 1.5, 1.5],
            		[1, 1, 1]]
        
        self.aviones=aviones
        self.pistas=pistas
		
        self.tipo_avion=tipo_avion
        self.TEL=TEL
    
    # TODO COMPROBAR
    def fitness(self, avion):
        """
        avion: List[int]
        """
        # -10 es el tiempo inicial para que el primer avion en llegar no tenga separacion 
        tla=[deque([(2, -10.0)]) for _ in range(self.pistas)]

        fitness=0.0
        n=len(avion)
        for i in range(n):
            new_tla=0 
            menor_tla=24.0
            index_pista=0
            
            for j in range(self.pistas):
                # Tiempo de Llegada Asignado (TLA) para la pista j + la separacion de esta pista (SEP)
                # o el Tiempo Estimada de Llegada (TEL)
                new_tla=max(tla[j][-1][1]+self.sep[tla[j][-1][0]][self.tipo_avion[avion[i]]], 
                            self.TEL[j][avion[i]])
               
                if new_tla<menor_tla:
                    menor_tla=new_tla
                    index_pista=j

            tla[index_pista].append((self.tipo_avion[avion[i]], menor_tla))

            menor_tel=24.0
            for j in range(self.pistas):
                if self.TEL[j][avion[i]]<menor_tel:
                    menor_tel=self.TEL[j][avion[i]]

            fitness+=(menor_tla-menor_tel)**2

        return fitness
    
    def cmp(self, a, b): 
        if a<b: return a
        else: return b

    def cmpBool(self, a, b): 
        if a<b: return True
        else: return False

    def cmpPeor(self, a, b): 
        if a>b: return a
        else: return b

    def cmpPeorBool(self, a, b): 
        if a>b: return True
        else: return False