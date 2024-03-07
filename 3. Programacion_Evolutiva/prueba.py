import sys
import os
import random
import math

"""
inicializar()
evaluar()
while()
    seleccionar()
    cruce()
    mutacion()
    evaluar()
"""

poblacion=[]
tam_poblacion=5
generaciones=20
prob_cruce=0.6
prob_mut=0.05
precision=0.01

tam_individuo=0
num_genes=2
tam_genes = [0 for _ in range(num_genes)]
maximos=[10,10]
minimos=[-10,-10]

class Individuo:  
    def __init__(self, num_genes, tam_genes, xMax, xMin, genes, fenotipos):
        self.num_genes = num_genes      # Numero de genes (int)
        self.tam_genes = tam_genes      # Tamaño de cada gen (int[])
        self.xMax=xMax                  # Valores maximos de cada gen
        self.xMin=xMin                  # Valores minimos de cada gen
        
        if genes!=None: self.genes = genes              # Array de bits, con todos los genes
        else: 
            self.genes=[]
            for i in range(self.num_genes):
                row = []
                for j in range(tam_genes[i]):
                    row.append(random.randint(0, 1))  
                self.genes.append(row)

        if fenotipos!=None: self.fenotipos=fenotipos    # Valor real
        else: 
            self.fenotipos = [(0.0) for _ in range(num_genes)]
            self.calcular_fenotipos()        

        self.fitness=0                                  # Valor de aptitud del individuo
        
       
        
    # Convierte a decimal un array de bits
    def bin2dec(self, gen):
        ret=0
        cont=1
        for i in range(len(gen) - 1, -1, -1):
            if gen[i]==1:
                ret+=cont                       
            cont*=2

        return ret	
    # Calcula los valores reales de cada gen del individuo
    def calcular_fenotipos(self):
        for i in range(self.num_genes):
            self.fenotipos[i]=(self.calcular_fenotipo(i))                  	
    # Calcula el valor real de un gen
    def calcular_fenotipo(self, i):
        return (self.xMin[i] + self.bin2dec(self.genes[i]) * ((self.xMax[i] - self.xMin[i]) / (pow(2, len(self.genes[i])) - 1)))



    # Imprime el individuo
    def print(self):
        for i in range(self.num_genes):
            for j in range(self.tam_genes[i]): 
                print(self.genes[i][j], end=" ")
            if i!=self.num_genes-1 : print(" | ", end="")
        print(" Fenotipo:{}".format(self.fitness))


def tamGenes() :    
    global tam_individuo    
    for i in range (num_genes):  
        tam_genes[i] = tamGen(minimos[i], maximos[i])
        tam_individuo += tam_genes[i]     


def tamGen(min, max) :
    return math.ceil((math.log10(((max - min) / precision) + 1) / math.log10(2)))

# Init
tamGenes()
for i in range(tam_poblacion):
    poblacion.append(Individuo(num_genes,tam_genes,maximos,minimos,genes=None,fenotipos=None))

# Evaluar
def fitness(nums):        
    return (pow(nums[0], 2) + 2 * pow(nums[1], 2))

mejor_total=0
fitness_total=0.0
prob_seleccion=[]
prob_seleccionAcum=[]

def eval():
    global mejor_total
    global fitness_total,prob_seleccion,prob_seleccionAcum

    mejor_generacion=0

    fitness_total = 0
    prob_seleccion = [(0.0) for _ in range(tam_poblacion)] 
    prob_seleccionAcum = [(0.0) for _ in range(tam_poblacion)] 


    for i in range(tam_poblacion):
        poblacion[i].calcular_fenotipos()
        poblacion[i].fitness = fitness(poblacion[i].fenotipos)
        fitness_total += poblacion[i].fitness
        if mejor_generacion < poblacion[i].fitness:
            mejor_generacion=poblacion[i].fitness

    if mejor_total<mejor_generacion :
        mejor_total=mejor_generacion

    tmp=0.0
    acum=0.0
    for i in range(tam_poblacion):
        tmp = poblacion[i].fitness / fitness_total
        prob_seleccion[i] = tmp
        acum += tmp
        prob_seleccionAcum[i] = acum  

eval()

def seleccion(tam_seleccionados, k):
    seleccionados=[]    # Individuo[]	
    randomFitness=0.0
    indexMax=0
    max=0.0
    
    for i in range(tam_seleccionados):				    
        max=-1.79769E+308	         			
        indexMax=-1	
        for j in range(k):                                  				
            randomIndex=random.randint(0,tam_poblacion-1)                				
            randomFitness = poblacion[randomIndex].fitness
            
            if randomFitness > max :					
                max = randomFitness					
                indexMax = randomIndex				
            		
        
        seleccionados.append(poblacion[indexMax])	

    
    return seleccionados # Individuo[]

def cruce(selec):
    print("TODO")

def mutacion(selec):
    print("TODO")

"""for ind in poblacion:
    ind.print()
print("Seleccionados")
for ind in seleccion(5,3):
    ind.print()"""


#print(prob_seleccionAcum)
while generaciones>0:
    # Seleccion
    selec=seleccion(5,3)

    # Cruce
    selec=cruce(selec)

    # Mutacion
    poblacion=mutacion(selec)
    # Evaluar
    eval()

    generaciones-=1
