import random
import sys
import os
sys.path.append(os.path.abspath("Model"))
import Individuo

class Seleccion:
    def __init__(self, tam_poblacion, opt):        
        self.tam_poblacion=tam_poblacion    # int  
        self.opt=opt                        # Boolean
    
    
    def busqueda_binaria(self, x, prob_acumulada):
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
            seleccionados.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=poblacion[self.busqueda_binaria(rand, prob_acumulada)]))
        return seleccionados

    def tornedoDeterministico(self, poblacion, tam_seleccionados, k):
        seleccionados=[]
        indexMax=0
        for i in range(tam_seleccionados):    
            max = float('-inf')
            indexMax = -1
            for j in range(k):        
                randomIndex=random.randint(0,self.tam_poblacion-1)
                randomFitness=poblacion[randomIndex].fitness
                if randomFitness>max:
                    max=randomFitness
                    indexMax=randomIndex              

            seleccionados.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=poblacion[indexMax]))

        return seleccionados



    
    def torneo_probabilistico():
        # TODO
        return ""
    
    def estocastico_universal():
        # TODO
        return ""
