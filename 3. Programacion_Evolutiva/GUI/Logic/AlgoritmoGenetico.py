import sys
import os
import random
import math
import queue

# internet de las cosas

sys.path.append(os.path.abspath("View"))
sys.path.append(os.path.abspath("Model"))

import Cruce 
import Mutacion
import Funcion
import Seleccion
from Model import Individuo
from Model import IndividuoReal
# TODO QUITAR EN UCM
from View import MainWindow


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

        if funcion_idx==0: self.funcion=Funcion.Funcion1()
        elif funcion_idx==1: self.funcion=Funcion.Funcion2()
        elif funcion_idx==2: self.funcion=Funcion.Funcion3()
        elif funcion_idx==3: self.funcion=Funcion.Funcion4(self.num_genes)
        else:            
            self.lee_archivos()
        
        self.seleccion_idx=seleccion_idx
        self.seleccion=Seleccion.Seleccion(tam_poblacion, self.funcion.opt)
        
        self.cruce_idx=cruce_idx
        self.cruce=Cruce.Cruce(prob_cruce,self.tam_elite, self.aviones)    
        
        self.mutacion_idx=mutacion_idx
        self.mutacion=Mutacion.Mutacion(prob_mut, self.aviones, self.tam_elite, 3, self.funcion)

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
        
        self.funcion = Funcion.FuncionA(self.aviones, self.pistas, self.tipo_avion, self.TEL)    
        
        

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
		
        self.MW.Plot2D(self.progreso_generaciones, self.mejor_ind, self.aviones)

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
		
        self.MW.Plot2D(self.progreso_generaciones, self.mejor_ind, self.aviones)

        return self.mejor_total

    def init_poblacion(self):
        if self.funcion_idx<4: 
            self.poblacion=[Individuo.Individuo(self.num_genes, self.tam_genes, self.funcion.xMax, self.funcion.xMin, 
                                                ind=None) for _ in range(self.tam_poblacion)]
        else: 
            self.poblacion=[IndividuoReal.IndividuoReal(aviones=self.aviones,vInd=None) for _ in range(self.tam_poblacion)]

    
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
            self.selec_elite.append(Individuo.Individuo(num=None,tam_genes=None,xMax=None,xMin=None,
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
            self.selec_elite.append(IndividuoReal.IndividuoReal(aviones=None,
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