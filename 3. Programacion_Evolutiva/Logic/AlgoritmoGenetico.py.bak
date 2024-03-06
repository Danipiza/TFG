import random
import time
import sys
import os
import math

# Importar las bibliotecas con los archivos

sys.path.append(os.path.abspath("Model"))
sys.path.append(os.path.abspath("Utils"))
import Cruce
import Mutacion
import Funcion
import Seleccion
from Model import Individuo



"""
Ejemplo del laberinto

inicializar()
evaluar()
while()
    seleccionar()
    cruce()
    mutacion()
    evaluar()

"""


class AlgoritmoGenetico:
    def __init__(self):
        self.funcion=None           # Funcion
        self.seleccion=None         # Seleccion
        self.cruce=None             # Cruce
        self.mutacion=None          # Mutacion

        self.poblacion=[]           # Individuo[]
        self.tam_genes=[]           # int[]
        self.tam_individuo=0        # int


        self.tam_poblacion=0        # int
        self.generaciones=0         # int
        self.num_genes=0            # int
        self.prob_cruce=0.0         # double (0.1)
        self.prob_mut=0.0           # double (0-1)

        self.precision=0.0          # double (1, 0.01, 0.001, ...)
        self.elitismo=0             # int (0-100%)

        self.mejor_total=0          # Individuo
        self.fitness_total=0        # double
        self.prob_seleccion=[]      # double
        self.prob_seleccionAcum=[]  # double[]
        

        

        
        
        

        

        """tam_poblacion,generaciones,
                    seleccion, cruce, prob_cruce,mutacion,prob_mut,
                    precision,funcion,num_genes,elitismo"""

        


    def set_valores(self):       
        
        self.tam_poblacion=100
        self.generaciones=100    
        

        self.funcion=Funcion.Funcion1([10.0,10.0],[-10.0,-10.0])
        self.seleccion = Seleccion.Seleccion(self.tam_poblacion, True)  
        self.cruce=Cruce.Cruce(0.6) 
        self.mutacion=Mutacion.Mutacion(0.05) 

        self.precision = 0.001
        self.num_genes=2
        self.tam_genes=self.tamGenes() 
        print(self.tam_genes)
    
    # TODO
    """def set_valores(self, tam_poblacion,generaciones,
                    seleccion, cruce, prob_cruce,mutacion,prob_mut,
                    precision,funcion,num_genes,elitismo):
        
        self.tam_poblacion=tam_poblacion
        self.generaciones=generaciones
        #self.seleccion=seleccion   
        #self.seleccion = Seleccion.Seleccion(self.tam_poblacion, True)
        
        #self.cruce=cruce
        #self.cruce=Cruce.Cruce(0.6) 
        #self.prob_cruce=prob_cruce
        #self.mutacion=Mutacion.Mutacion(0.05) 
        
        self.mutacion=mutacion
        self.prob_mut=prob_mut
        self.precision=precision
        #self.funcion=funcion
        #self.funcion=Funcion.Funcion1([10.0,10.0],[-10.0,-10.0])
        self.num_genes=num_genes
        self.elitismo=elitismo

        self.tam_genes=self.tamGenes() """

    def init_poblacion(self):   
        self.poblacion = [Individuo.Individuo(self.num_genes, self.tam_genes,[10,10],[-10,-10]) for _ in range(self.tam_poblacion)]


    # funcion 
    def evalua_poblacion(self):

        self.fitness_total = 0
        self.prob_seleccion = [0.0] * self.tam_poblacion
        self.prob_seleccionAcum = [0.0] * self.tam_poblacion
        
        mejor_generacion=0

        for i in range(self.tam_poblacion):
            self.poblacion[i].calcular_fenotipos()
            self.poblacion[i].fitness = self.funcion.fitness(self.poblacion[i].fenotipos)
            self.fitness_total += self.poblacion[i].fitness
            if mejor_generacion < self.poblacion[i].fitness:
                mejor_generacion=self.poblacion[i].fitness

        if self.mejor_total<mejor_generacion :
            self.mejor_total=mejor_generacion
        
        tmp=0.0
        acum=0.0
        for i in range(self.tam_poblacion):
            tmp = self.poblacion[i].fitness / self.fitness_total
            self.prob_seleccion[i] = tmp
            acum += tmp
            self.prob_seleccionAcum[i] = acum    


    
    def selecciona_poblacion(self):     
        #return seleccion.ruleta(poblacion,prob_seleccionAcum,tam_poblacion)
        return self.seleccion.torneo_deterministico(self.poblacion,3,self.tam_poblacion)

    def cruza_poblacion(self,seleccion):          
        return self.cruce.cruce_monopuntoBin(seleccion)

    def muta_poblacion(self):    
        return self.mutacion.mut_basicaBin(self.poblacion)

    def tamGenes(self) : # int[] 
        ret = [0 for _ in range(self.num_genes)]
        print(ret)
        
        for i in range (self.num_genes):  
            ret[i] = self.tamGen(self.funcion.minimos[i], self.funcion.maximos[i])
            self.tam_individuo += ret[i]     

        return ret


    def tamGen(self, min, max) :
        return math.ceil((math.log10(((max - min) / self.precision) + 1) / math.log10(2)))


    

    def printMejor(self):
        print(self.mejor_total)

    def ejecuta(self):    
        #global poblacion

        self.set_valores()

        
        start_time = time.time()
        
        self.init_poblacion()
        self.evalua_poblacion()    
        for i in range(self.generaciones):
            selec = self.selecciona_poblacion()    
            #print_poblacion(selec)
            self.poblacion = self.cruza_poblacion(selec)    
            #print_poblacion(poblacion)
            self.poblacion = self.muta_poblacion()
            #print_poblacion(poblacion)
            self.evalua_poblacion()
        

        end_time = time.time()
        print("Tiempo de ejecucion:",  end_time - start_time)
        #print_poblacion()
    
"""ag=AlgoritmoGenetico()
ag.ejecuta()
ag.printMejor()"""