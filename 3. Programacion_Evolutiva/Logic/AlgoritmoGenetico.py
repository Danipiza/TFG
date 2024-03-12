import sys
import os
import random
import math


sys.path.append(os.path.abspath("View"))
sys.path.append(os.path.abspath("Model"))

import Cruce 
import Mutacion
import Funcion
import Seleccion
from Model import Individuo
from View import MainWindow

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


        self.progreso_generaciones=[[],[],[]]

    # Funcion que inicializa las variables a los valores seleccionados en la interfaz
    def set_valores(self,tam_poblacion, generaciones, seleccion_idx, cruce_idx, prob_cruce, mutacion_idx,
                    prob_mut, precision, funcion_idx, num_genes, elitismo):
        
        self.poblacion=[]
        self.tam_poblacion=tam_poblacion    
        self.generaciones=generaciones      
        self.prob_cruce = prob_cruce        
        self.prob_mut = prob_mut    

        self.num_genes=num_genes # 2
                

        self.funcion_idx=funcion_idx
        # TODO FUNCIONES
        if funcion_idx==0: self.funcion=Funcion.Funcion1()
        elif funcion_idx==1: self.funcion=Funcion.Funcion2()
        elif funcion_idx==2: self.funcion=Funcion.Funcion3()
        elif funcion_idx==3: self.funcion=Funcion.Funcion4(self.num_genes)
        else: self.funcion=Funcion.Funcion5(self.num_genes)
        
        self.seleccion_idx=seleccion_idx
        self.seleccion=Seleccion.Seleccion(tam_poblacion,True)
        
        self.cruce_idx=cruce_idx
        self.cruce=Cruce.Cruce(prob_cruce)    
        
        self.mutacion_idx=mutacion_idx
        self.mutacion=Mutacion.Mutacion(prob_mut)

        self.tam_genes=self.tamGenes(precision)
        #self.mejor_total = float('-inf')
        if self.funcion.opt==True: self.mejor_total = float('-inf')
        else: self.mejor_total = float('+inf')

        self.elitismo=elitismo        
        

    def tamGenes(self, precision):   
        ret = []
        for i in range(self.num_genes):
            ret.append(self.tamGen(precision, self.funcion.xMin[i], self.funcion.xMax[i]))
        return ret

    def tamGen(self, precision, min, max):
        return math.ceil((math.log10(((max-min)/precision)+1)/math.log10(2)))

    def ejecuta(self):
        selec=[]

        self.init_poblacion()    
        self.evaluacion_poblacion()
                
        
        while self.generaciones > 0:
            selec = self.seleccion_poblacion(self.tam_poblacion, 5)
            
            """print("Generacion:", self.generaciones)
            for ind in selec:
                ind.print_individuo()"""
            
            self.poblacion = self.cruce_poblacion(selec)
            self.poblacion = self.mutacion_poblacion(selec)
            
            self.evaluacion_poblacion()
            
            """print("Fin")
            for ind in self.poblacion:
                ind.print_individuo()"""
            
            self.generaciones-=1
        
            
        # TODO DESCOMENTAR
        #self.MW.Plot2D(self.progreso_generaciones)

        print(self.mejor_total)


    def init_poblacion(self):
        self.poblacion = [Individuo.Individuo(self.num_genes, self.tam_genes, self.funcion.xMax, self.funcion.xMin, ind=None) for _ in range(self.tam_poblacion)]


    # TODO 
        # DESPLAZAMIENTO
        # PRESION SELECTIVA
    def evaluacion_poblacion(self):
        
        self.fitness_total=0
        self.prob_seleccion = [(0) for _ in range(self.tam_poblacion)]
        self.prob_seleccionAcum = [(0) for _ in range(self.tam_poblacion)]
        if self.funcion.opt==True: 
            mejor_generacion = float('-inf')
            peor_generacion = float('+inf')
        else: 
            mejor_generacion = float('+inf')
            peor_generacion = float('-inf')
        mejor_generacionInd=None


        if self.funcion_idx<4:
            for i in range(self.tam_poblacion):            
                self.poblacion[i].calcular_fenotipo()
			
		


        fit=0.0
        #fitnessTotalAdaptado = 0.0
        for i in range(self.tam_poblacion):
            fit=self.funcion.fitness(self.poblacion[i].fenotipo)
            self.poblacion[i].fitness=fit
            self.fitness_total+=fit

            #if fit>mejor_generacion: mejor_generacion=fit
            if(self.funcion.cmpBool(fit, mejor_generacion)) :
                mejor_generacion=fit;	
                mejor_generacionInd=self.poblacion[i]
            peor_generacion=self.funcion.cmpPeor(peor_generacion,fit)
			

        #if mejor_generacion>self.mejor_total: self.mejor_total=mejor_generacion
        if(self.funcion.cmpBool(mejor_generacion, self.mejor_total)):
            self.mejor_total=mejor_generacion;	
            self.mejor_ind=mejor_generacionInd
		


        self.progreso_generaciones[0].append(self.mejor_total)
        self.progreso_generaciones[1].append(mejor_generacion)
        self.progreso_generaciones[2].append((self.fitness_total/self.tam_poblacion))
        

        acum=0.0
        if peor_generacion < 0: peor_generacion *= -1

        if self.funcion.opt==False:
            self.fitness_total = self.tam_poblacion * 1.05 * peor_generacion - self.fitness_total
            for i in range(self.tam_poblacion):
                self.prob_seleccion[i] = 1.05 * peor_generacion - self.poblacion[i].fitness
                self.prob_seleccion[i] /= self.fitness_total
                acum += self.prob_seleccion[i]
                self.prob_seleccionAcum[i] = acum			
        else:
            self.fitness_total = self.tam_poblacion * 1.05 * peor_generacion + self.fitness_total
            for i in range(self.tam_poblacion):
                self.prob_seleccion[i] = 1.05 * peor_generacion + self.poblacion[i].fitness
                self.prob_seleccion[i] /= self.fitness_total
                acum += self.prob_seleccion[i]
                self.prob_seleccionAcum[i] = acum
			
		

        """for i in range(self.tam_poblacion):
            self.prob_seleccion[i] = self.poblacion[i].fitness/self.fitness_total
            acum+=self.prob_seleccion[i]
            self.prob_seleccionAcum[i]=acum
        """

    def seleccion_poblacion(self, tam_seleccionados, k):         
        ret=[]
        if self.seleccion_idx==0: ret=self.seleccion.ruleta(self.poblacion, self.prob_seleccionAcum, tam_seleccionados)
        else: ret= self.seleccion.tornedoDeterministico(self.poblacion, tam_seleccionados, k)
        return ret

    def cruce_poblacion(self, selec):
        ret=[]
        if self.cruce_idx==0: ret=self.cruce.cruce_monopuntoBin(selec)
        return ret
        """n=len(selec)
        ret=[(None) for _ in range(n)]
        if n%2==1:
            ret[n-1] = Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[n-1])
            n-=1
        
        long_genes=[len(selec[0].genes[i].v) for i in range(len(selec[0].genes))]
        corte_maximo=-1
        for l in long_genes:
            corte_maximo+=l
        i=0

        ind1=[]
        ind2=[]
        while i<n:
            ind1=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i])
            ind2=Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=selec[i + 1])
            
            rand=random.random()
            if rand<self.prob_cruce:                                               
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
            
            
            ret[i] = Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind1)
            ret[i+1] = Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,ind=ind2)
            i += 2     
        
        return ret"""

    def mutacion_poblacion(self, selec):
        ret=[]
        #if self.mutacion_idx == 0: ret = self.mutacion.mut_basicaBin(selec)
        ret = self.mutacion.mut_basicaBin(selec)

        return ret


    
    
