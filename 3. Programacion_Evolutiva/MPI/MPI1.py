from mpi4py import MPI # UCM NO FUNCIONA (NO ESTA LA BIBLIOTECA, TAMPOCO MATPLOT)
import sys
import os
import random
import math
import queue

from abc import ABC, abstractmethod 
from collections import deque
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

#mpiexec -np 6 python MPI1.py

def GUI(fits):    
    # Create figure and axes
    #fig, axs = plt.subplots(2, 2, figsize=(18, 12), gridspec_kw={'width_ratios': [1, 2]})
    n=len(fits)
    # Define data for the first plot
    x1 = [i for i in range(1, n + 1)]  
    # Define data for the second plot       

    # Crear la figura y GridSpec
    fig = plt.figure(figsize=(10, 6))
    gs = GridSpec(1, 1, figure=fig)

    # Grafico 1 (arriba a la izquierda)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x1, fits, color='b', linestyle='-')    
    ax1.set_xlabel('Generaciones Master')
    ax1.set_ylabel('Fitness')
    ax1.set_title('2D-Plot"')
    ax1.grid(True)

    
    
    
    plt.tight_layout() # Ajustar la disposición de los subplots    
    plt.show() # Mostrar los gráficos

# -----------------------------------------------------------------------------------------------
# --- INDIVIDUO ---------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------


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

class IndividuoReal:
    def __init__(self, aviones, vInd):
        self.v=[]
        self.fitness=0.0

        if vInd is not None:         
            for i in range(len(vInd)):
                self.v.append(vInd[i])
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

# -----------------------------------------------------------------------------------------------
# --- FUNCION -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------


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

# -----------------------------------------------------------------------------------------------
# --- SELECCION ---------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

class Pair():
    def __init__(self, key, value):
        self.key=key
        self.value=value

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key=key

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value=value

    def __str__(self):
        return "(" + str(self.key) + ", " + str(self.value) + ")"

class Seleccion:
    def __init__(self, tam_poblacion, opt):        
        self.tam_poblacion=tam_poblacion    # int  
        self.opt=opt                        # Boolean
    
    
    def busquedaBinaria(self, x, prob_acumulada):
        i=0
        j=self.tam_poblacion-1
        while i<j:
            m=(j+i)//2
            if x>prob_acumulada[m]: i=m+1
            elif x<prob_acumulada[m]: j=m
            else: return m
        return i

    def ruletaBin(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        for _ in range(tam_seleccionados):
            rand=random.random()
            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                     ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
        return seleccionados

    def ruletaReal(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        for _ in range(tam_seleccionados):
            rand=random.random()
            seleccionados.append(IndividuoReal(aviones=None,
                                           vInd=poblacion[self.busquedaBinaria(rand, prob_acumulada)].v))
        return seleccionados
    
    
    def torneoDeterministicoBin(self, poblacion, k, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
            for j in range(k):        
                randomIndex=random.randint(0,self.tam_poblacion-1)
                randomFitness=poblacion[randomIndex].fitness
                if randomFitness>max:
                    max=randomFitness
                    indexMax=randomIndex 
                if randomFitness<min:
                    min=randomFitness
                    indexMin=randomIndex                
            
            if self.opt==True: ind=indexMax
            else: ind=indexMin

            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                     ind=poblacion[ind]))

        return seleccionados
    
    
    def torneoDeterministicoReal(self, poblacion, k, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
            for j in range(k):        
                randomIndex=random.randint(0,self.tam_poblacion-1)
                randomFitness=poblacion[randomIndex].fitness
                if randomFitness>max:
                    max=randomFitness
                    indexMax=randomIndex 
                if randomFitness<min:
                    min=randomFitness
                    indexMin=randomIndex                
            
            if self.opt==True: ind=indexMax
            else: ind=indexMin

            seleccionados.append(IndividuoReal(aviones=None,
                                               vInd=poblacion[ind].v))

        return seleccionados



    def torneoProbabilisticoBin(self, poblacion, k, p, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
            for j in range(k):        
                randomIndex=random.randint(0,self.tam_poblacion-1)
                randomFitness=poblacion[randomIndex].fitness
                if randomFitness>max:
                    max=randomFitness
                    indexMax=randomIndex 
                if randomFitness<min:
                    min=randomFitness
                    indexMin=randomIndex                
            
            if self.opt==True: 
                if random.random()<=p: ind=indexMax
                else: ind=indexMin
            else: 
                if random.random()<=p: ind=indexMin
                else: ind=indexMax

            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                     ind=poblacion[ind]))

        return seleccionados
    
    def torneoProbabilisticoReal(self, poblacion, k, p, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max=float('-inf')
            min=float('+inf')
            indexMax=-1
            indexMin=-1
            for j in range(k):        
                randomIndex=random.randint(0,self.tam_poblacion-1)
                randomFitness=poblacion[randomIndex].fitness
                if randomFitness>max:
                    max=randomFitness
                    indexMax=randomIndex 
                if randomFitness<min:
                    min=randomFitness
                    indexMin=randomIndex                
            
            if self.opt==True: 
                if random.random()<=p: ind=indexMax
                else: ind=indexMin
            else: 
                if random.random()<=p: ind=indexMin
                else: ind=indexMax

            seleccionados.append(IndividuoReal(aviones=None,
                                               vInd=poblacion[ind].v))

        return seleccionados
    

    def estocasticoUniversalBin(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
		
        incr=1.0/tam_seleccionados
        rand=random.random()*incr
        for i in range(tam_seleccionados):       			
            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                     ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
			
            rand+=incr		

        return seleccionados
    
    def estocasticoUniversalReal(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
		
        incr=1.0/tam_seleccionados
        rand=random.random()*incr
        for i in range(tam_seleccionados):       			
            seleccionados.append(IndividuoReal(aviones=None,
                                               vInd=poblacion[self.busquedaBinaria(rand, prob_acumulada)].v))
			
            rand+=incr		

        return seleccionados

    
    def truncamientoBin(self, poblacion, prob_seleccion, trunc, tam_seleccionados):
        seleccionados=[]
        
        pairs=[]
        for i in range(tam_seleccionados): 
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))
		
        pairs=sorted(pairs, key=lambda x: x.value, reverse=False)
        x=0
        num=int(1.0/trunc)
        n=len(pairs)-1
        for i in range(int((tam_seleccionados)*trunc)+1):		
            j=0
            while j<num and x<tam_seleccionados:            
                seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                         ind=pairs[n-i].get_key()))
                j+=1
                x+=1
			
		
        return seleccionados
    
    def truncamientoReal(self, poblacion, prob_seleccion, trunc, tam_seleccionados):
        seleccionados=[]
        
        pairs=[]
        for i in range(tam_seleccionados): 
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))
		
        pairs=sorted(pairs, key=lambda x: x.value, reverse=False)
        x=0
        num=int(1.0/trunc)
        n=len(pairs)-1
        for i in range(int((tam_seleccionados)*trunc)+1):		
            j=0
            while j<num and x<tam_seleccionados:            
                seleccionados.append(IndividuoReal(aviones=None,
                                                   vInd=pairs[n-i].get_key().v))
                j+=1
                x+=1
			
		
        return seleccionados
    
    
    def restosBin(self, poblacion, prob_seleccion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        
        x=0
        num=0
        aux=0.0		
        for i in range(tam_seleccionados):		
            aux=prob_seleccion[i]*(tam_seleccionados)
            num=int(aux)
			
            for j in range(num):
                seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                               ind=poblacion[i]))
                x+=1
				
		
        resto=[]
        func=random.randint(0,4) # Cambiar
        # SE SUMA LA PARTE DE elitismo PORQUE SINO SE RESTA 2 VECES, 
        # EN LA PARTE DE restos() Y LA FUNCION RANDOM
        if func==0: resto=self.ruletaBin(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==1: resto=self.torneoDeterministicoBin(poblacion, 3, tam_seleccionados-x)	
        elif func==2: resto=self.torneoProbabilisticoBin(poblacion, 3, 0.9, tam_seleccionados-x)
        elif func==3: resto=self.estocasticoUniversalBin(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==4: resto=self.truncamientoBin(poblacion, prob_acumulada, 0.5, tam_seleccionados-x) 
        else: resto=self.rankingBin(poblacion, prob_seleccion, 2, tam_seleccionados-x)
        
        for ind in resto:
            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                           ind=ind))
		

        return seleccionados
    
    def restosReal(self, poblacion, prob_seleccion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
        
        x=0
        num=0
        aux=0.0		
        for i in range(tam_seleccionados):		
            aux=prob_seleccion[i]*(tam_seleccionados)
            num=int(aux)
			
            for j in range(num):
                seleccionados.append(IndividuoReal(aviones=None,
                                                   vInd=poblacion[i].v))
                x+=1
				
			
        resto=[]
        func=random.randint(0,4) # Cambiar
        # SE SUMA LA PARTE DE elitismo PORQUE SINO SE RESTA 2 VECES, 
        # EN LA PARTE DE restos() Y LA FUNCION RANDOM
        if func==0: resto=self.ruletaReal(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==1: resto=self.torneoDeterministicoReal(poblacion, 3, tam_seleccionados-x)	
        elif func==2: resto=self.torneoProbabilisticoReal(poblacion, 3, 0.9, tam_seleccionados-x)
        elif func==3: resto=self.estocasticoUniversalReal(poblacion, prob_acumulada, tam_seleccionados-x)
        elif func==4: resto=self.truncamientoReal(poblacion, prob_acumulada, 0.5, tam_seleccionados-x) 
        else: resto=self.rankingReal(poblacion, prob_seleccion, 2, tam_seleccionados-x)
        
        for ind in resto:
            seleccionados.append(IndividuoReal(aviones=None,
                                               vInd=ind.v))
		

        return seleccionados


    
    def rankingBin(self, poblacion, prob_seleccion, beta, tam_seleccionados):
        seleccionados=[]

        pairs=[]
		
        for i in range(tam_seleccionados):
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))

        pairs.sort(key=lambda p: p.value, reverse=True)

        val=0.0
        acum=0.0
        prob_acumulada=[] # tam_selec

        for i in range(1,tam_seleccionados+1):		
            val=(beta-(2*(beta-1)*((i-1)/(tam_seleccionados-1.0))))/tam_seleccionados
            acum+=val
            prob_acumulada.append(acum)
				
		
        rand=0.0
        for i in range(tam_seleccionados):        
            rand = random.random()
            seleccionados.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                           ind=pairs[self.busquedaBinaria(rand, prob_acumulada)].get_key()))		
		
        return seleccionados
    
    def rankingReal(self, poblacion, prob_seleccion, beta, tam_seleccionados):
        seleccionados=[]

        pairs=[]
		
        for i in range(tam_seleccionados):
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))

        pairs.sort(key=lambda p: p.value, reverse=True)

        val=0.0
        acum=0.0
        prob_acumulada=[] # tam_selec

        for i in range(1,tam_seleccionados+1):		
            val=(beta-(2*(beta-1)*((i-1)/(tam_seleccionados-1.0))))/tam_seleccionados
            acum+=val
            prob_acumulada.append(acum)
				
		
        rand=0.0
        for i in range(tam_seleccionados):        
            rand = random.random()
            seleccionados.append(IndividuoReal(aviones=None,
                                               vInd=pairs[self.busquedaBinaria(rand, prob_acumulada)].get_key().v))		
		
        return seleccionados

# -----------------------------------------------------------------------------------------------
# --- CRUCE -------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

class Cruce:
    def __init__(self, p, tam_elite, aviones):
        self.p=p    # int
        self.tam_elite=tam_elite
        self.aviones=aviones
    
    def cruce_monopuntoBin(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)]
        if n%2==1:
            ret[n-1]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[n-1])
            n-=1
        
        long_genes=[len(selec[0].genes[i].v) for i in range(len(selec[0].genes))]
        corte_maximo=-1
        for l in long_genes:
            corte_maximo+=l
        i=0

        ind1=[]
        ind2=[]
        while i<n:
            ind1=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i])
            ind2=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i+1])
            
            rand=random.random()
            if rand<self.p:                                               
                corte=random.randint(1,corte_maximo)
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
                        
            
            ret[i]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind1)
            ret[i+1]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind2)            
            i += 2     
               
        
        
        return ret
    
    def cruce_uniformeBin(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)]
        if n%2==1:
            ret[n-1]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[n-1])
            n-=1
        
        long_genes=[len(selec[0].genes[i].v) for i in range(len(selec[0].genes))]
        corte_maximo=-1
        for l in long_genes:
            corte_maximo+=l
        i=0

        long_genes=[len(selec[0].genes[i].v) for i in range(len(selec[0].genes))]
        cont=0 
        l=0
        for c in long_genes:
            l+=c
            long_genes[cont]=c
            cont+=1
        
        i=0      
        j=0
        k=0
        ind1=None
        ind2=None
        tmp=0
        while i<n:
            ind1=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i])
            ind2=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i+1])

            
            if random.random()>self.p:
                cont=0
                j=0

                for k in range(l):				
                    if random.random()<0.5:
                        tmp=ind1.genes[cont].v[j]
                        ind1.genes[cont].v[j]=ind2.genes[cont].v[j]
                        ind2.genes[cont].v[j]=tmp
                    
                    j+=1
                    if j==long_genes[cont]:
                        cont+=1
                        j=0

					
				
            
			
            ret[i]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind1)
            ret[i+1]=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind2)            
            i+=2     
               
        
        
        return ret
    
    def PMX(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal(aviones=None,
                                   vInd=selec[n-1].v) 
            n-=1 # Descarta al ultimo si es impar
		
		
		 
        i=0
        k=0
        ind1=None
        ind2=None
        """
        Se intercambian desde [corte1, corte2)
        """
        corte1=0
        corte2=0
        while i<n:
            ind1=IndividuoReal(aviones=None,
                               vInd=selec[i].v)
            ind2=IndividuoReal(aviones=None,
                               vInd=selec[i+1].v)
            if random.random()<self.p:                
                pareja1={} # {int, int}
                pareja2={} 

                corte1=int(random.random()*(self.aviones-2))
                corte2=corte1+int(random.random()*(self.aviones-corte1))
				
                # Se intercambia el intervalo a cortar
                # y se añade a un diccionario para hacer PMX
                for j in range(corte1,corte2):				
                    temp=ind1.v[j]
                    ind1.v[j] = ind2.v[j];					
                    ind2.v[j] = temp;		
					
                    pareja1[ind1.v[j]]=ind2.v[j]
                    pareja2[ind2.v[j]]=ind1.v[j]
				
                # Recorre los individuos por el final del intervalo a cortar
                for j in range(self.aviones-(corte2-corte1)):
                    # Si el elemento del Padre1 no esta en el intervalo copiado
                    # del Padre2 se deja como esta y avanza al siguiente.
                    # Si esta en el intervalo, se busca 
                    # el elemento correspondiente con los diccionarios
                    if ind1.v[(corte2+j)%self.aviones] in pareja1:                    
                        p=pareja1[ind1.v[(corte2+j)%self.aviones]]

                        while p in pareja1:                        
                            p=pareja1[p]						
                        ind1.v[(corte2+j)%self.aviones]=p

                    if ind2.v[(corte2+j)%self.aviones] in pareja2:
                        p=pareja2[ind2.v[(corte2+j)%self.aviones]]

                        while p in pareja2:                        
                            p=pareja2[p]						
                        ind2.v[(corte2+j)%self.aviones]=p

				
			
            ret[i]=IndividuoReal(aviones=None,
                               vInd=ind1.v)
            ret[i+1]=IndividuoReal(aviones=None,
                               vInd=ind2.v)
            i+=2
			
		
        return ret
    
    def OX(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal(aviones=None,
                                   vInd=selec[n-1].v) 
            n-=1 # Descarta al ultimo si es impar

        i=0
        k=0
        ind1=None
        ind2=None
        """
        Se intercambian desde [corte1, corte2)
        """
        corte1=0
        corte2=0
        while i<n:
            ind1=IndividuoReal(aviones=None,
                               vInd=selec[i].v)
            ind2=IndividuoReal(aviones=None,
                               vInd=selec[i+1].v)

            if random.random()<self.p:
                corte1 = (int) (random.random() * (self.aviones - 2))
                corte2 = corte1 + (int) (random.random() * (self.aviones - corte1))
                set1={""}
                set2={""}
                
                # Se añaden los elementos del padre opuesto
                for j in range(corte1,corte2):                
                    set1.add(ind2.v[j])
                    set2.add(ind1.v[j])
                

                # Hijo 1
                j=corte2
                cont=j
                while j%self.aviones!=corte1:
                    if ind1.v[cont] not in set1:
                        ind1.v[j]=ind1.v[cont]
                        j=(j+1)%self.aviones
                    
                    cont=(cont+1)%self.aviones

                # Hijo 2
                j=corte2
                cont=j
                while j%self.aviones!=corte1:
                    if ind2.v[cont] not in set2:
                        ind2.v[j]=ind2.v[cont]
                        j=(j+1)%self.aviones
                    
                    cont=(cont+1)%self.aviones
                
                
                # Se intercambian la zona del intervalo
                for j in range(corte1,corte2):                
                    temp=ind1.v[j]
                    ind1.v[j]=ind2.v[j]
                    ind2.v[j]=temp
                
                

                

            
            ret[i]=IndividuoReal(aviones=None,
                               vInd=ind1.v)
            ret[i+1]=IndividuoReal(aviones=None,
                               vInd=ind2.v)
            i+=2
        
        return ret
    
    # TODO REVISAR
    def OX_PP(self, selec, pp):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal(aviones=None,
                                   vInd=selec[n-1].v) 
            n-=1 # Descarta al ultimo si es impar

        i=0
        k=0
        ppi=0
        ind1=None
        ind2=None
        validos=[0 for _ in range(self.aviones-pp)]
        while i<n:
            ind1=IndividuoReal(aviones=None,
                               vInd=selec[i].v)
            ind2=IndividuoReal(aviones=None,
                               vInd=selec[i+1].v)

            if random.random()<self.p:    

                puntos={""}                
                puntosList=[0 for _ in range(pp)]
                set1={""}
                set2={""}
                
                # Se eligen "pp" puntos al azar
                punto=0
                for j in range(pp):                
                    punto = int(random.random()*(self.aviones-1))
                    while punto in puntos:
                        punto=int(random.random()*(self.aviones-1))
                    
                    puntos.add(punto)
                    puntosList[j]=punto

                    set1.add(ind2.v[punto])
                    set2.add(ind1.v[punto])
                

                # Hijo 1
                k=0
                for j in range(self.aviones):                
                    if ind1.v[j] not in set1:                    
                        validos[k]=ind1.v[j]
                        k+=1
                    
                ppi=0
                k=0
                for j in range(self.aviones):                
                    if j not in puntos:                    
                        ind1.v[j]=validos[k]
                        k+=1               


                # Hijo 2
                k=0
                for j in range(self.aviones):
                    if ind2.v[j] not in set2:                    
                        validos[k]=ind2.v[j]
                        k+=1
                    
                ppi=0
                k=0
                for j in range(self.aviones):
                    if j not in puntos:                    
                        ind2.v[j]=validos[k]
                        k+=1
                
                for j in range(pp):                    
                    temp=ind1.v[puntosList[j]]
                    ind1.v[puntosList[j]]=ind2.v[puntosList[j]]
                    ind2.v[puntosList[j]]=temp

                
                
                

            
            ret[i]=IndividuoReal(aviones=None,
                               vInd=ind1.v)
            ret[i+1]=IndividuoReal(aviones=None,
                               vInd=ind2.v)
            i+=2
        
        return ret
    
    def CX(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] # = [n + tam_elite] no hace falta? TODO

        if n%2==1 :
            ret[n-1]=IndividuoReal(aviones=None,
                                   vInd=selec[n-1].v) 
            n-=1 # Descarta al ultimo si es impar
		
		
		 
        i=0
        ind1=None
        ind2=None
        while i<n:
            ind1=IndividuoReal(aviones=None,
                               vInd=selec[i].v)
            ind2=IndividuoReal(aviones=None,
                               vInd=selec[i+1].v)

            if random.random()<self.p:
                pareja1={}
                for j in range(self.aviones):                
                    pareja1[ind1.v[j]]=ind2.v[j]
                
                set={""}

                # Añade al Set los elementos del ciclo
                a=ind1.v[0]
                set.add(a)
                a=pareja1.get(a)
                while a not in set:                
                    set.add(a)
                    a=pareja1.get(a)
                
                # Intercambio de los que no estan en el set
                for j in range(self.aviones):
                    if ind1.v[j] not in set:                    
                        temp=ind1.v[j]
                        ind1.v[j]=ind2.v[j]
                        ind2.v[j]=temp
                
                    
                
                
				
			
            ret[i]=IndividuoReal(aviones=None,
                               vInd=ind1.v)
            ret[i+1]=IndividuoReal(aviones=None,
                               vInd=ind2.v)
            i+=2
			
		
        return ret
    
    def CO(self, selec):
        n=len(selec)
        ret=[(None) for _ in range(n)] 

        if n%2==1 :
            ret[n-1]=IndividuoReal(aviones=None,
                                   vInd=selec[n-1].v) 
            n-=1 # Descarta al ultimo si es impar
		
		
        i=0
        k=0
        e=0
        ind1=None
        ind2=None
        corte1=0
        while i<n:
            ind1=IndividuoReal(aviones=None,
                               vInd=selec[i].v)
            ind2=IndividuoReal(aviones=None,
                               vInd=selec[i+1].v)

            if random.random()<self.p:
                listaDinamica=[i for i in range(0,self.aviones)]

                # Codificacion ind1                
                for j in range(self.aviones):                
                    k=0
                    e=1
                    while (listaDinamica[k]!=ind1.v[j]):
                        if listaDinamica[k]!=-1: e+=1
                        k+=1
                    
                    ind1.v[j]=e
                    listaDinamica[k]=-1
                

                # Codificacion ind2
                listaDinamica=[i for i in range(0,self.aviones)]
                for j in range(self.aviones):                
                    k=0
                    e=1
                    while listaDinamica[k]!=ind2.v[j]:
                        if listaDinamica[k]!=-1: e+=1
                        k+=1
                    
                    ind2.v[j]=e
                    listaDinamica[k]=-1
                

                corte1=int(random.random()*self.aviones)

                for j in range(corte1):                
                    temp=ind1.v[j]
                    ind1.v[j]=ind2.v[j]
                    ind2.v[j]=temp
                

                # Descodificacion ind1
                listaDinamica=[i for i in range(0,self.aviones)]
                for j in range(self.aviones):                
                    k=-1
                    e=0
                    while e<ind1.v[j]:
                        k+=1
                        if listaDinamica[k]!=-1: e+=1
                    
                    ind1.v[j]=listaDinamica[k]
                    listaDinamica[k]=-1
                

                # Descodificacion ind2
                listaDinamica=[i for i in range(0,self.aviones)]
                for j in range(self.aviones):                
                    k=-1
                    e=0
                    while e<ind2.v[j]:
                        k+=1
                        if listaDinamica[k]!=-1: e+=1
                    
                    ind2.v[j]=listaDinamica[k]
                    listaDinamica[k]=-1
                
				
			
            ret[i]=IndividuoReal(aviones=None,
                               vInd=ind1.v)
            ret[i+1]=IndividuoReal(aviones=None,
                               vInd=ind2.v)
            i+=2
			
		
        return ret

# -----------------------------------------------------------------------------------------------
# --- MUTACION ----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------


class Mutacion:
    def __init__(self, p, aviones, tam_elite, heur, funcion):
        self.p=p
        self.aviones=aviones
        self.tam_elite=tam_elite
        self.permutaciones=[]
        self.heur=heur
        self.dfs(heur,0,[],[0 for i in range(heur)])
        #print(self.permutaciones)
        self.funcion=funcion
    

    def mut_basicaBin(self, selec):
        ret=[]
        for ind in selec:
            act=Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind)
            for c in range(len(ind.genes)):
                for j in range(len(ind.genes[c].v)):
                    if random.random()<self.p:
                        act.genes[c].v[j]=(act.genes[c].v[j]+1)%2
            ret.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=act))
        return ret
    

    def inversion(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
		
        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal(aviones=None,
                              vInd=poblacion[i].v);	
            			
            if random.random()<self.p:
                corte1=int(random.random()*(len(act.v)-2))
                corte2=corte1+int(random.random()*(len(act.v)-corte1))
                separacion=(corte2-corte1+1)
                for k in range(separacion//2):
                    temp=act.v[corte1+k]
                    act.v[corte1+k]=act.v[corte2-k]
                    act.v[corte2-k]=temp
			
            ret.append(IndividuoReal(aviones=None,
                                     vInd=act.v))
		
        return ret


    def intercambio(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
		
        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal(aviones=None,
                              vInd=poblacion[i].v);	
            			
            if random.random()<self.p:
                punto1=int(random.random()*(len(act.v)-2))
                punto2=punto1+int(random.random()*(len(act.v)-1-punto1))
                
                temp=act.v[punto1]
                act.v[punto1]=act.v[punto2]
                act.v[punto2]=temp
                
			
            ret.append(IndividuoReal(aviones=None,
                                     vInd=act.v))
		
        return ret
    

    def insercion(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
        
        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal(aviones=None,
                              vInd=poblacion[i].v);	
            
            if random.random()<self.p:
                antiguaPosicion=int(random.random()*(len(act.v)-1))
                nuevaPosicion=antiguaPosicion
                while nuevaPosicion==antiguaPosicion:
                    nuevaPosicion = int(random.random()*(len(act.v)-1))

                    
				
                if nuevaPosicion>antiguaPosicion:
                    tmp=act.v[antiguaPosicion]
                    for k in range(antiguaPosicion,nuevaPosicion):
                        act.v[k]=act.v[k+1]
					
                    act.v[nuevaPosicion]=tmp				
                else:
                    tmp=act.v[antiguaPosicion]
                    #for (int k = antiguaPosicion; k > nuevaPosicion ; k--) {
                    for k in range(antiguaPosicion, nuevaPosicion,-1):					
                        act.v[k]=act.v[k-1]
					
                    act.v[nuevaPosicion]=tmp
					
			
            ret.append(IndividuoReal(aviones=None,
                                     vInd=act.v))
		
        return ret
    

    def heuristica(self, poblacion):
        tam_poblacion=len(poblacion)
        ret=[] # = new Individuo[tam_poblacion];
		
        rand=0
		
        cont=0
		
        elegidos_indx=[0 for _ in range(self.heur)]
        elegidos_vals=[0 for _ in range(self.heur)]	
		
        set_elegidos={""}
		
        mejor_fit=float("inf")
        mejor=[0 for _ in range(self.aviones)]
        tmp=[0 for _ in range(self.aviones)]
        

        act=None
        for i in range(tam_poblacion):                                
            act=IndividuoReal(aviones=None,
                              vInd=poblacion[i].v);	
            
            if random.random()<self.p:
                cont=0
                set_elegidos.clear()
                mejor_fit=float("inf")

                while cont<self.heur:
                    numero = random.randint(0,self.aviones-1)
                    if numero not in set_elegidos:
                        set_elegidos.add(numero)
                        elegidos_indx[cont]=numero
                        elegidos_vals[cont]=act.v[numero]
                        cont+=1
                    

                cont=0
                tmp=act.v
                # Recorre las permutaciones
                for l in self.permutaciones:                
                    # Cambia los valores
                    for x in l: 
                        tmp[elegidos_indx[x]]=elegidos_vals[x]
                    
                    
                    fit=self.funcion.fitness(tmp);		
                    cont+=1
                    if fit<mejor_fit:
                        mejor_fit=fit
                        mejor=tmp
                
                

                ret.append(IndividuoReal(aviones=None,
                                        vInd=mejor))
            else: 
                ret.append(IndividuoReal(aviones=None,
                                        vInd=act.v))
            
					
			
            
		
        return ret  
        
    def dfs(self, n, k, act, visitados):
        if k==n:
            aux=[]            
            for x in act:
                aux.append(x)
            
            self.permutaciones.append(aux)
            return

        for i in range(n):            
            if visitados[i]==1: continue
            
            visitados[i]=1
            act.append(i)
            self.dfs(n,k+1,act,visitados)
            act.pop(len(act)-1)
            visitados[i]=0
        

# -----------------------------------------------------------------------------------------------
# --- ALGORITMO GENETICO ------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

# value=1 Max, cualquier otro valor => Min
class PQ(queue.PriorityQueue):
    def __init__(self, value):
        super().__init__()
        self.value=1
        if value==1: self.value=-1

    def push(self, id, fit):
        super().put((self.value*fit, id))

    def top_fit(self):
        fit, _ = self.queue[0]  
        return self.value*fit
    
    def top_id(self):
        _, id = self.queue[0]  
        return id
    
    def pop(self):
        _, id = super().get()
        return id
    
    def size(self):
        return self.qsize()

class AlgoritmoGenetico():
    def __init__(self,MW):
        self.MW=MW                  # Class: MainWindow
        
        
        self.funcion=None           # Funcion
        self.seleccion=None         # Seleccion
        self.cruce=None             # Cruce
        self.mutacion=None          # Mutacion

        self.poblacion=[]           # Individuo[]
        self.tam_genes=[]           # int[]

        self.tam_poblacion=0        # int
        self.generaciones=0         # int
        self.num_genes=0            # int
        self.prob_cruce=0.0         # double (0.1)
        self.prob_mut=0.0           # double (0-1)

        self.precision=0.0          # double (1, 0.01, 0.001, ...)
        self.elitismo=0             # int (0-100%)

        self.mejor_total=0.0        # double
        self.mejor_ind=None         # Individuo
        self.fitness_total=0        # double
        self.prob_seleccion=[]      # double
        self.prob_seleccionAcum=[]  # double[]

        self.elitQ=None   

        # AEROPUERTO
        self.aviones=0
        self.pistas=0
        self.vuelos_id=[]
        self.TEL=[] # 2D array
        self.tipo_avion=[]


        self.progreso_generaciones=[[] for _ in range(4)]

    # Funcion que inicializa las variables a los valores seleccionados en la interfaz
    def set_valores(self,tam_poblacion, generaciones, seleccion_idx, cruce_idx, prob_cruce, mutacion_idx,
                    prob_mut, precision, funcion_idx, num_genes, elitismo):
        
        self.poblacion=[]
        self.tam_poblacion=tam_poblacion    
        self.generaciones=generaciones      
        self.prob_cruce=prob_cruce        
        self.prob_mut=prob_mut    

        self.num_genes=num_genes # 2
        
        self.elitismo=elitismo  
        self.tam_elite=int((tam_poblacion*(elitismo/100.0)))  

        self.funcion_idx=funcion_idx

        if funcion_idx==0: self.funcion=Funcion1()
        elif funcion_idx==1: self.funcion=Funcion2()
        elif funcion_idx==2: self.funcion=Funcion3()
        elif funcion_idx==3: self.funcion=Funcion4(self.num_genes)
        else:            
            self.lee_archivos()
        
        self.seleccion_idx=seleccion_idx
        self.seleccion=Seleccion(tam_poblacion, self.funcion.opt)
        
        self.cruce_idx=cruce_idx
        self.cruce=Cruce(prob_cruce,self.tam_elite, self.aviones)    
        
        self.mutacion_idx=mutacion_idx
        self.mutacion=Mutacion(prob_mut, self.aviones, self.tam_elite, 3, self.funcion)

        if funcion_idx!=-1: self.elitQ=PQ(0) # 
        else: self.elitQ=PQ(1) # Cola prioritaria de maximos para almacenar los menores y asi comparar rapidamente
        self.selec_elite=[]

        if funcion_idx<4: self.tam_genes=self.tamGenes(precision)
        
        self.mejor_total=float('+inf')
        if self.funcion_idx<4:
            if self.funcion.opt==True: self.mejor_total=float('-inf')
            else: self.mejor_total=float('+inf')
        

    def lee_archivos(self):
        vuelos_txt="data/"
        TEL_txt="data/"

        # LEE DE LOS TXT
        if self.funcion_idx==4:
            self.aviones=12
            self.pistas=3
            vuelos_txt+="vuelos1.txt"
            TEL_txt+="TEL1.txt"
        elif self.funcion_idx==5:
            self.aviones=25
            self.pistas=5
            vuelos_txt+="vuelos2.txt"
            TEL_txt+="TEL2.txt"
        elif self.funcion_idx==6:
            self.aviones=100
            self.pistas=10
            vuelos_txt+="vuelos3.txt"
            TEL_txt+="TEL3.txt"
        
        i=0
        self.vuelos_id=[None for _ in range(self.aviones)]
        self.tipo_avion = [0 for _ in range(self.aviones)]
        self.TEL = [[0 for _ in range(self.aviones)] for _ in range(self.pistas)]
        
        try:
            # Open the file
            with open(vuelos_txt, 'r') as vuelos_reader, open(TEL_txt, 'r') as TEL_reader:
                for line in vuelos_reader:
                    tokens=line.split()
                    self.vuelos_id[i]=tokens[0]
                    if tokens[1]=="W": self.tipo_avion[i]=0
                    elif tokens[1]=="G": self.tipo_avion[i]=1
                    else: self.tipo_avion[i]=2
                    
                    i+=1

                i=0
                for line in TEL_reader:
                    tokens=line.split("\t")
                    j=0
                    for t in tokens:
                        self.TEL[i][j]=int(t)
                        j+=1
                    
                    i+=1
        except IOError as e:
            print("Error al leer archivos:", e)
        
        self.funcion = FuncionA(self.aviones, self.pistas, self.tipo_avion, self.TEL)    
        
        

    def tamGenes(self, precision):   
        ret = []
        for i in range(self.num_genes):
            ret.append(self.tamGen(precision, self.funcion.xMin[i], self.funcion.xMax[i]))
        return ret

    def tamGen(self, precision, min, max):
        return math.ceil((math.log10(((max-min)/precision)+1)/math.log10(2)))

    def ejecuta(self):
        if self.funcion_idx<4: return self.ejecutaBin()
        else: return self.ejecutaReal()

    def ejecutaBin(self):
        selec=[]

        self.init_poblacion()    
        self.evaluacion_poblacionBin()                
        
        while self.generaciones > 0:
            selec=self.seleccion_poblacionBin(5)
            
            self.poblacion=self.cruce_poblacionBin(selec)
            self.poblacion=self.mutacion_poblacionBin(self.poblacion)

            for i in range(self.tam_elite):
                self.poblacion.append(self.selec_elite[i])
            
            self.evaluacion_poblacionBin()            
            
            self.generaciones-=1
		
        #self.MW.Plot2D(self.progreso_generaciones, self.mejor_ind, self.aviones)

        return self.mejor_total

    def ejecutaReal(self):
        selec=[]

        self.init_poblacion()    
        self.evaluacion_poblacionReal()                
        
        while self.generaciones > 0:
            selec=self.seleccion_poblacionReal(5)
            
            self.poblacion=self.cruce_poblacionReal(selec)
            self.poblacion=self.mutacion_poblacionReal(self.poblacion)

            for i in range(self.tam_elite):
                self.poblacion.append(self.selec_elite[i])
            
            self.evaluacion_poblacionReal()            
            
            self.generaciones-=1
		
        #self.MW.Plot2D(self.progreso_generaciones, self.mejor_ind, self.aviones)

        return self.mejor_total

    def init_poblacion(self):
        if self.funcion_idx<4: 
            self.poblacion=[Individuo(self.num_genes, self.tam_genes, self.funcion.xMax, self.funcion.xMin, 
                                                ind=None) for _ in range(self.tam_poblacion)]
        else: 
            self.poblacion=[IndividuoReal(aviones=self.aviones,vInd=None) for _ in range(self.tam_poblacion)]
        

    
    def evaluacion_poblacionBin(self):        
        self.fitness_total=0
        self.prob_seleccion=[0 for _ in range(self.tam_poblacion)]
        self.prob_seleccionAcum=[0 for _ in range(self.tam_poblacion)]
        if self.funcion.opt==True: 
            mejor_generacion = float('-inf')
            peor_generacion = float('+inf')
        else: 
            mejor_generacion = float('+inf')
            peor_generacion = float('-inf')


        
        for i in range(self.tam_poblacion):            
            self.poblacion[i].calcular_fenotipo()
			
		
        fit=0.0
        indexMG=0        
        for i in range(self.tam_poblacion):
            fit=self.funcion.fitness(self.poblacion[i].fenotipo)
            self.poblacion[i].fitness=fit
            self.fitness_total+=fit

            if self.elitQ.size()<self.tam_elite: self.elitQ.push(i, fit)
            elif(self.tam_elite!=0 and self.funcion.cmpBool(fit, self.elitQ.top_fit())):
                self.elitQ.pop()
                self.elitQ.push(i, fit)
			
            

            #if fit>mejor_generacion: mejor_generacion=fit
            if(self.funcion.cmpBool(fit, mejor_generacion)) :
                mejor_generacion=fit;	                
                indexMG=i
            peor_generacion=self.funcion.cmpPeor(peor_generacion, fit)
			
        self.selec_elite=[]
        for _ in range(self.tam_elite):
            self.selec_elite.append(Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
                                                        ind=self.poblacion[self.elitQ.pop()]))
            

        #if mejor_generacion>self.mejor_total: self.mejor_total=mejor_generacion
        if(self.funcion.cmpBool(mejor_generacion, self.mejor_total)):
            self.mejor_total=mejor_generacion;	
            self.mejor_ind=self.poblacion[indexMG]
		


        self.progreso_generaciones[0].append(self.mejor_total)
        self.progreso_generaciones[1].append(mejor_generacion)
        self.progreso_generaciones[2].append((self.fitness_total/self.tam_poblacion))
        
        
        

        acum=0.0
        if peor_generacion<0: peor_generacion*=-1

        if self.funcion.opt==False:
            self.fitness_total=self.tam_poblacion*1.05*peor_generacion-self.fitness_total
            for i in range(self.tam_poblacion):
                self.prob_seleccion[i]=1.05*peor_generacion-self.poblacion[i].fitness
                self.prob_seleccion[i]/=self.fitness_total
                acum += self.prob_seleccion[i]
                self.prob_seleccionAcum[i]=acum			
        else:
            self.fitness_total = self.tam_poblacion*1.05*peor_generacion+self.fitness_total
            for i in range(self.tam_poblacion):
                self.prob_seleccion[i]=1.05*peor_generacion+self.poblacion[i].fitness
                self.prob_seleccion[i]/=self.fitness_total
                acum+=self.prob_seleccion[i]
                self.prob_seleccionAcum[i]=acum
        
        # Whitley recomienda valores próximos a 1.5
            # Valores mayores ocasionarían superindividuos
            # Valores menores frenarían la búsqueda sin ningún beneficio
        self.progreso_generaciones[3].append(self.tam_poblacion*self.prob_seleccion[indexMG])

    def evaluacion_poblacionReal(self):        
        self.fitness_total=0
        self.prob_seleccion=[0 for _ in range(self.tam_poblacion)]
        self.prob_seleccionAcum=[0 for _ in range(self.tam_poblacion)]

        
        mejor_generacion=float('+inf')
        peor_generacion=float('-inf')

		
        fit=0.0
        indexMG=0        
        for i in range(self.tam_poblacion):
            fit=self.funcion.fitness(self.poblacion[i].v)
            self.poblacion[i].fitness=fit
            self.fitness_total+=fit

            if self.elitQ.size()<self.tam_elite: self.elitQ.push(i, fit)
            elif(self.tam_elite!=0 and self.funcion.cmpBool(fit, self.elitQ.top_fit())):
                self.elitQ.pop()
                self.elitQ.push(i, fit)
			
            

            #if fit>mejor_generacion: mejor_generacion=fit
            if(self.funcion.cmpBool(fit, mejor_generacion)) :
                mejor_generacion=fit;	                
                indexMG=i
            peor_generacion=self.funcion.cmpPeor(peor_generacion, fit)
			
        self.selec_elite=[]
        for _ in range(self.tam_elite):
            self.selec_elite.append(IndividuoReal(aviones=None,
                                                  vInd=self.poblacion[self.elitQ.pop()].v))
            

        #if mejor_generacion>self.mejor_total: self.mejor_total=mejor_generacion
        if(self.funcion.cmpBool(mejor_generacion, self.mejor_total)):
            self.mejor_total=mejor_generacion;	
            self.mejor_ind=self.poblacion[indexMG]
		


        self.progreso_generaciones[0].append(self.mejor_total)
        self.progreso_generaciones[1].append(mejor_generacion)
        self.progreso_generaciones[2].append((self.fitness_total/self.tam_poblacion))
        
        
        
        acum=0.0
        if peor_generacion<0: peor_generacion*=-1

        self.fitness_total=self.tam_poblacion*1.05*peor_generacion-self.fitness_total
        for i in range(self.tam_poblacion):
            self.prob_seleccion[i]=1.05*peor_generacion-self.poblacion[i].fitness
            self.prob_seleccion[i]/=self.fitness_total
            acum += self.prob_seleccion[i]
            self.prob_seleccionAcum[i]=acum	
        
        # Whitley recomienda valores próximos a 1.5
            # Valores mayores ocasionarían superindividuos
            # Valores menores frenarían la búsqueda sin ningún beneficio
        self.progreso_generaciones[3].append(self.tam_poblacion*self.prob_seleccion[indexMG])
        
    
    def seleccion_poblacionBin(self, k):         
        ret=[]
        
        if self.seleccion_idx==0: 
            ret=self.seleccion.ruletaBin(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==1: 
            ret=self.seleccion.torneoDeterministicoBin(self.poblacion, k, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==2: 
            ret=self.seleccion.torneoProbabilisticoBin(self.poblacion, k, 0.9, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==3: 
            ret=self.seleccion.estocasticoUniversalBin(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==4: 
            ret=self.seleccion.truncamientoBin(self.poblacion, self.prob_seleccion, 0.5, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==5: 
            ret=self.seleccion.restosBin(self.poblacion, self.prob_seleccion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        else: 
            ret=self.seleccion.rankingBin(self.poblacion, self.prob_seleccion, 2, self.tam_poblacion-self.tam_elite)
        return ret

    def seleccion_poblacionReal(self, k):         
        ret=[]
        
        if self.seleccion_idx==0: 
            ret=self.seleccion.ruletaReal(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==1: 
            ret=self.seleccion.torneoDeterministicoReal(self.poblacion, k, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==2: 
            ret=self.seleccion.torneoProbabilisticoReal(self.poblacion, k, 0.9, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==3: 
            ret=self.seleccion.estocasticoUniversalReal(self.poblacion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==4: 
            ret=self.seleccion.truncamientoReal(self.poblacion, self.prob_seleccion, 0.5, self.tam_poblacion-self.tam_elite)
        elif self.seleccion_idx==5: 
            ret=self.seleccion.restosReal(self.poblacion, self.prob_seleccion, self.prob_seleccionAcum, self.tam_poblacion-self.tam_elite)
        else: 
            ret=self.seleccion.rankingReal(self.poblacion, self.prob_seleccion, 2, self.tam_poblacion-self.tam_elite)
        return ret

      
    def cruce_poblacionBin(self, selec):
        ret=[]
        if self.cruce_idx==0: return self.cruce.cruce_monopuntoBin(selec)
        elif self.cruce_idx==1: return self.cruce.cruce_uniformeBin(selec)
        else:
            print("Cruce Binario, Solo hay cruce Mono-Punto y Uniforme")
            exit(1)
    
    # TODO
    def cruce_poblacionReal(self, selec):
        ret=[]
        
        if self.cruce_idx==2: return self.cruce.PMX(selec) # PMX
        elif self.cruce_idx==3: return self.cruce.OX(selec) # OX
        elif self.cruce_idx==4: return self.cruce.OX_PP(selec,3)
        elif self.cruce_idx==5: return self.cruce.CX(selec)
        elif self.cruce_idx==6: return self.cruce.CO(selec)      
        else:
            print("Cruce Real, No tiene cruce Mono-Punto o Uniforme")
            exit(1)
        
        
    def mutacion_poblacionBin(self, selec):
        ret=[]    
        
        if self.mutacion_idx==0: return self.mutacion.mut_basicaBin(selec)
        else:
            print("Mutacion Binaria, Solo hay mutacion basica")
            exit(1)
    
    def mutacion_poblacionReal(self, selec):
        ret=[]    
        
        if self.mutacion_idx==1: return self.mutacion.insercion(selec) # Insercion
        elif self.mutacion_idx==2: return self.mutacion.intercambio(selec) # Intercambio
        elif self.mutacion_idx==3: return self.mutacion.inversion(selec) # Inversion
        elif self.mutacion_idx==4: return self.mutacion.heuristica(selec) # Heuristica
        else:
            print("Cruce Real, No hay Mutacion Basica")
            exit(1)


# -----------------------------------------------------------------------------------------------
# --- MAIN --------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------


def main():
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion

    
    
    seleccion_opt = ["Ruleta", 
                     "Torneo Determinista", 
                     "Torneo Probabilístico", 
                     "Estocástico Universal",
                     "Truncamiento",
                     "Restos",
                     "Ranking"]
        
    cruce_opt = ["Básica", 
                 "Uniforme",
                 "PMX",
                 "OX",
                 "OX-PP",
                 "CX",
                 "CO"]
    
    mutacion_opt = ["Básica",
                    "Insercion",
                    "Intercambio",
                    "Inversion",
                    "Heuristica"]

    funcion_opt = ["F1: Calibracion y Prueba",
                   "F2: Mishra Bird",
                   "F3: Holder table",
                   "F4: Michalewicz (Binaria)",
                   "Aeropuerto 1",
                   "Aeropuerto 2",
                   "Aeropuerto 3"]
    
    # DATOS A COMPARTIR
    tam_poblacion=0
    generaciones=0
    num_genes=0
    seleccion_idx=0
    cruce_idx=0
    prob_cruce=0.0
    mut_idx=0
    prob_mut=0.0 
    precision=0.00 
    funcion_idx=0
    elitismo=0 

    poblacion=[]           # Individuo[]
   

    mejor_total=0.0        

    # 
    tam_seleccionados=0
    num_torneo=5 

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    if myrank==MASTER:
        tam_poblacion=1000
        generaciones=1000

        # 0: Ruleta | 1: Torneo Determinista  | 2: Torneo Probabilístico | 3: Estocástico Universal 
        #           | 4: Truncamiento  | 5: Restos | 6: Ranking
        seleccion_idx=1
        # 0: Basica | 1: Uniforme | 
        # 2: PMX    | 3: OX       | 4: OX-PP | 5: CX | 6: CO
        cruce_idx=2 
        prob_cruce=0.6
        # 0: Basica    | 
        # 1: Insercion | 2: Intercambio | 3: Inversion | 4: Heuristica
        mut_idx=2
        # Binario: 0.05 | Real: 0.3
        prob_mut=0.3 
        precision=0.01
        # 0: Funcion 1    | 1: Funcion 2    | 2: Funcion 3    | 3: Funcion 4
        # 4: Aeropuerto 1 | 5: Aeropuerto 2 | 6: Aeropuerto 3 | 
        funcion_idx=6
        num_genes=2
        elitismo=0

        print("\nFuncion: {}\t Seleccion: {}\t Cruce: {} (p:{})\tMutacion:{} (p:{})".format(funcion_opt[funcion_idx],
                                                                      seleccion_opt[seleccion_idx],
                                                                      cruce_opt[cruce_idx],
                                                                      prob_cruce,
                                                                      mutacion_opt[mut_idx],
                                                                      prob_mut))
    
        print("Tam. Poblacion: {}\t Num. Generaciones: {}\t Elitismo: {}%".format(tam_poblacion*numWorkers,
                                                                             generaciones,
                                                                             elitismo))

    totalTimeStart = MPI.Wtime()

    tam_poblacion=comm.bcast(tam_poblacion, root=MASTER)
    generaciones=comm.bcast(generaciones, root=MASTER)
    seleccion_idx=comm.bcast(seleccion_idx, root=MASTER)
    cruce_idx=comm.bcast(cruce_idx, root=MASTER)
    prob_cruce=comm.bcast(prob_cruce, root=MASTER)
    mut_idx=comm.bcast(mut_idx, root=MASTER)
    prob_mut=comm.bcast(prob_mut, root=MASTER)
    precision=comm.bcast(precision, root=MASTER)
    funcion_idx=comm.bcast(funcion_idx, root=MASTER)
    num_genes=comm.bcast(num_genes, root=MASTER)
    elitismo=comm.bcast(elitismo, root=MASTER)      
    

    if myrank==MASTER:
        mejor_total=float("inf")
        progreso=[]
        while generaciones>0:
            
            
            for _ in range(numWorkers):
                # ENVIA EL MEJOR
                data=comm.recv(source=MPI.ANY_SOURCE) 
                if mejor_total>data: mejor_total=data 

            progreso.append(mejor_total)            
            generaciones-=1
        totalTimeEnd = MPI.Wtime()
        print("Valor Optimo: {}\n".format(progreso[-1]))
        print("Tiempo de ejecucion total: {}\n".format(totalTimeEnd-totalTimeStart))

        GUI(progreso)

        
        
    else: # WORKER
        AG=AlgoritmoGenetico(None)
        AG.set_valores( tam_poblacion, 
                        generaciones, 
                        seleccion_idx,
                        cruce_idx, 
                        prob_cruce,
                        mut_idx, 
                        prob_mut,
                        precision, 
                        funcion_idx, 
                        num_genes, 
                        elitismo)

        if AG.funcion_idx<4: 
            print("TODO")
            """selec=[]

            self.init_poblacion()    
            self.evaluacion_poblacionBin()                
            
            while self.generaciones > 0:
                selec=self.seleccion_poblacionBin(5)
                
                self.poblacion=self.cruce_poblacionBin(selec)
                self.poblacion=self.mutacion_poblacionBin(self.poblacion)

                for i in range(self.tam_elite):
                    self.poblacion.append(self.selec_elite[i])
                
                self.evaluacion_poblacionBin()            
                
                self.generaciones-=1
            
            #self.MW.Plot2D(self.progreso_generaciones, self.mejor_ind, self.aviones)

            return self.mejor_total"""
        else:     
            selec=[]
            poblacion=[]

            AG.init_poblacion()    
            AG.evaluacion_poblacionReal()                
            
            while generaciones>0:
                selec=AG.seleccion_poblacionReal(5)
                
                AG.poblacion=AG.cruce_poblacionReal(selec)
                AG.poblacion=AG.mutacion_poblacionReal(AG.poblacion)

                for i in range(AG.tam_elite):
                    AG.poblacion.append(AG.selec_elite[i])
                
                AG.evaluacion_poblacionReal()

                # ENVIA EL MEJOR
                comm.send(AG.mejor_total, dest=MASTER)  

                          
                
                generaciones-=1
            
            

            #return self.mejor_total

        

    
    
    
    


main()