import random
import time
import sys
import os
import math

# Importar las bibliotecas con los archivos
sys.path.append(os.path.abspath("Logic"))
sys.path.append(os.path.abspath("Model"))
sys.path.append(os.path.abspath("Utils"))
import Cruce
import Mutacion
import Funcion
import Seleccion
import Individuo



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

funcion=None
seleccion=None
cruce=None
mutacion=None

poblacion=[]
tam_poblacion=0
generaciones=0
num_genes=0
tam_genes=[]
tam_individuo=0
precision=0.0

fitness_total = 0
prob_seleccion = [0.0] * tam_poblacion
prob_seleccionAcum = [0.0] * tam_poblacion

mejor_total=0


def init_poblacion():   
    global poblacion    
    poblacion = [Individuo.Individuo(num_genes, tam_genes,[10,10],[-10,-10]) for _ in range(tam_poblacion)]


# funcion 
def evalua_poblacion():
    global tam_poblacion, poblacion
    global fitness_total, prob_seleccion, prob_seleccionAcum
    global mejor_total

    fitness_total = 0
    prob_seleccion = [0.0] * tam_poblacion
    prob_seleccionAcum = [0.0] * tam_poblacion
    
    mejor_generacion=0

    for i in range(tam_poblacion):
        poblacion[i].calcular_fenotipos()
        poblacion[i].fitness = funcion.fitness(poblacion[i].fenotipos)
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


#global poblacion, prob_seleccionAcum, tam_poblacion
def selecciona_poblacion():     
    #return seleccion.ruleta(poblacion,prob_seleccionAcum,tam_poblacion)
    return seleccion.torneo_deterministico(poblacion,3,tam_poblacion)

def cruza_poblacion(seleccion):          
    return cruce.cruce_monopuntoBin(seleccion)

#global poblacion
def muta_poblacion():    
    return mutacion.mut_basicaBin(poblacion)

def tamGenes() : # int[] 
    global tam_individuo
    ret = [0 for _ in range(num_genes)]
    print(ret)
    
    for i in range (num_genes):  
        ret[i] = tamGen(precision, funcion.minimos[i], funcion.maximos[i])
        tam_individuo += ret[i]     

    return ret


def tamGen(precision, min, max) :
    return math.ceil((math.log10(((max - min) / precision) + 1) / math.log10(2)))


def set_valores():
    global tam_poblacion, generaciones, num_genes, tam_genes, precision
    global funcion, seleccion, cruce, mutacion
    
    
    tam_poblacion=100
    generaciones=100    
    

    funcion=Funcion.Funcion1([10.0,10.0],[-10.0,-10.0])
    seleccion = Seleccion.Seleccion(tam_poblacion, True)  
    cruce=Cruce.Cruce(0.6) 
    mutacion=Mutacion.Mutacion(0.05) 

    precision = 0.001
    num_genes=2
    tam_genes=tamGenes() 
    print(tam_genes)


def ejecuta():    
    global poblacion

    set_valores()

    
    start_time = time.time()
     
    init_poblacion()
    evalua_poblacion()    
    for i in range(generaciones):
        selec = selecciona_poblacion()    
        #print_poblacion(selec)
        poblacion = cruza_poblacion(selec)    
        #print_poblacion(poblacion)
        poblacion = muta_poblacion()
        #print_poblacion(poblacion)
        evalua_poblacion()
    

    end_time = time.time()
    print("Tiempo de ejecucion:",  end_time - start_time)
    #print_poblacion()
    

ejecuta()
print(mejor_total)