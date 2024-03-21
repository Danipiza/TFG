import random
import sys
import os
#sys.path.append(os.path.abspath("Model"))
import Individuo

#import Pair

class Pair():
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = key

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return "(" + str(self.key) + ", " + str(self.value) + ")"

#sys.path.append(os.path.abspath("Utils"))
#from Utils import Pair

class Seleccion:
    def __init__(self, tam_poblacion, opt):        
        self.tam_poblacion=tam_poblacion    # int  
        self.opt=opt                        # Boolean
    
    
    def busquedaBinaria(self, x, prob_acumulada):
        i,j = 0,self.tam_poblacion-1
        while i<j:
            m=(j+i)//2
            if x>prob_acumulada[m]: i=m+1
            elif x<prob_acumulada[m]: j=m
            else: return m
        return i

    def ruleta(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados = []
        for _ in range(tam_seleccionados):
            rand = random.random()
            seleccionados.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
        return seleccionados
    
    # TODO
    def tornedoDeterministico(self, poblacion, tam_seleccionados, k):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max = float('-inf')
            min = float('+inf')
            indexMax = -1
            indexMin = -1
            for j in range(k):        
                randomIndex=random.randint(0,self.tam_poblacion-1)
                randomFitness=poblacion[randomIndex].fitness
                if randomFitness>max:
                    max=randomFitness
                    indexMax=randomIndex 
                if randomFitness<min:
                    min=randomFitness
                    indexMax=randomIndex                
            
            if self.opt==True: ind=indexMax
            else: ind=indexMin

            seleccionados.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=poblacion[ind]))

        return seleccionados



    # TODO
    def torneoProbabilistico(self, poblacion, k, p, tam_seleccionados):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max = float('-inf')
            min = float('+inf')
            indexMax = -1
            indexMin = -1
            for j in range(k):        
                randomIndex=random.randint(0,self.tam_poblacion-1)
                randomFitness=poblacion[randomIndex].fitness
                if randomFitness>max:
                    max=randomFitness
                    indexMax=randomIndex 
                if randomFitness<min:
                    min=randomFitness
                    indexMax=randomIndex                
            
            if self.opt==True: 
                if random.random()<=p: ind=indexMax
                else: ind=indexMin
            else: 
                if random.random()<=p: ind=indexMin
                else: ind=indexMax

            seleccionados.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=poblacion[ind]))

        return seleccionados
    

    def estocasticoUniversal(self, poblacion, prob_acumulada, tam_seleccionados):
        seleccionados=[]
		
        incr=1.0/tam_seleccionados
        rand=random.random()*incr
        for i in range(tam_seleccionados):       			
            seleccionados.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=poblacion[self.busquedaBinaria(rand, prob_acumulada)]))
			
            rand += incr		

        return seleccionados

    # TODO
    def truncamiento(self, poblacion, prob_seleccion, trunc, tam_seleccionados):
        seleccionados=[]

		#Pair<Individuo, Double>[] pairs = new Pair[tam_seleccionados];
        pairs=[]
        for i in range(tam_seleccionados): 
            pairs.append(Pair(poblacion[i], prob_seleccion[i]))
		
        pairs = sorted(pairs, key=lambda x: x.value, reverse=False)
		#Arrays.sort(pairs, Comparator.comparingDouble(p -> p.getValue()));

        x=0
        num= int(1.0/trunc)
        n=len(pairs)-1
        for i in range(int((tam_seleccionados) * trunc)):		
            j=0
            while j<num and x<tam_seleccionados:            
                seleccionados.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=pairs[n-i].get_key()))
                j+=1
                x+=1
			
		
		
        return seleccionados
    
    # TODO
    def restos(self, poblacion, prob_seleccion, prob_acumulada, tam_seleccionados):
            # TODO
            return ""
    # TODO
    def ranking(self):
            # TODO
            return ""
