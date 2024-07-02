from mpi4py import MPI
import random
import sys
import os
import math

# EJECUTAR
# py RedesNeuronales.py

"""
Red Neuronal multicapa.

1 Capa de entrada, 2 variables = 2 nodos. Altura y Peso, para predecir el IMC
1 Capa de salida, 1 variable = 1 nodo. IMC
X Capas ocultas con Y nodos cada una.
"""


def lee(archivo):
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".Otros","ficheros","4.RedNeu", archivo+".txt")

    with open(path, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')      
    for i in range(0, len(datos), 3):
        altura=float(datos[i])
        peso=float(datos[i+1])
        IMC=float(datos[i+2])

        array.append([altura,peso,IMC])

    #print("\n",array)        
    
    return array


# Normalizar los datos de altura y peso
def normalizar_dato(val,m,M):
    return (val-m)/(M-m)
# Desnormalizar el IMC
def desnormalizar_dato(val,m,M):
    return val*(M-m)+m

"""# Normalizar los datos de altura y peso
def normalizar_muchos_datos(vals,m,M):
    n=len(vals)
    return [(vals[i]-m[i])/(M[i]-m[i]) for i in range(n)]
# Desnormalizar el IMC
def normalizar_muchos_datos(vals,m,M):
    n=len(vals)
    return [vals[i]*(M[i]-m[i])+m[i] for i in range(n)]"""


# Funcion de activacion
def sigmoide(x):
    return 1/(1+math.exp(-x))
#Derivada (para el entrenamiento)
def sigmoide_derivado(x):
    return x*(1-x)


class RedNeuronal:
    def __init__(self, tam_entrada, tam_capas_ocultas, tam_salida):
        self.tam_entrada=tam_entrada
        self.tam_capas_ocultas=tam_capas_ocultas
        self.tam_salida=tam_salida
        
        self.capas=[tam_entrada]+tam_capas_ocultas+[tam_salida]
        
        # Inicializar los pesos de manera aleatoria
        self.pesos=[]
        for i in range(len(self.capas)-1):
            pesos_capa = [[random.uniform(-1, 1) for _ in range(self.capas[i + 1])] for _ in range(self.capas[i])]
            self.pesos.append(pesos_capa)
        
        

    # Propagación hacia adelante (forward propagation)
    def forward(self,entrada):
        self.salidas=[entrada]
        # Recorre todas las capas (menos la de salida) 
        for i in range(len(self.capas)-1):
            entradas_capa=self.salidas[-1]
            salidas_capa=[0 for _ in range(self.capas[i+1])]
            # Recorre todos los nodos de la capa siguiente
            for j in range(self.capas[i+1]):    
                suma=0
                # Suma todos los nodos de la capa actual con los pesos
                for k in range(self.capas[i]):            
                    suma+=entradas_capa[k]*self.pesos[i][k][j]
                salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
            
            self.salidas.append(salidas_capa)
        
        # Devuelve el ultimo elemento        
        return self.salidas[-1] 

    # Retropropagación (backpropagation)
    def entrenar(self, entrada, etiqueta, learning_rate):
        self.forward(entrada)
        errores=[]
        for i in range(self.tam_salida):
            errores.append((etiqueta[i]-self.salidas[-1][i])*sigmoide_derivado(self.salidas[-1][i]))
                        
        # Recorre todas las capas (menos la de entrada) en orden inverso
        for i in range(len(self.capas) - 2, -1, -1):
            nuevos_errores=[0 for _ in range(self.capas[i])]
            # Recorre todos los nodos de la capa actual
            for j in range(self.capas[i]):
                suma=0
                # Suma todos los nodos de la capa siguiente (sin orden inverso, es decir, la derecha)
                for k in range(self.capas[i+1]):            
                    suma+=errores[k]*self.pesos[i][j][k]
                nuevos_errores[j]=suma*sigmoide_derivado(self.salidas[i][j])

                # Actualiza los nodos
                for k in range(self.capas[i+1]):
                    self.pesos[i][j][k]+=learning_rate*errores[k]*self.salidas[i][j]

            errores = nuevos_errores

def main():

    datos_entrenamiento=lee("datos80")
    #datos_entrenamiento=lee("datos2042")  
    

    # ----------------------------------------------------------------------------------------
    # --- Normalizar los datos ---------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    alturasD=[data[0] for data in datos_entrenamiento]
    pesosD=[data[1] for data in datos_entrenamiento]
    imcsD=[data[2] for data in datos_entrenamiento]

    alturaD_min=min(alturasD)
    alturaD_max=max(alturasD)
    pesoD_min=min(pesosD)
    pesoD_max=max(pesosD)
    imcD_min=min(imcsD)
    imcD_max=max(imcsD)

    datos_entrenamiento_normalizados = [
        [normalizar_dato(data[0], alturaD_min, alturaD_max), 
         normalizar_dato(data[1], pesoD_min, pesoD_max), 
         normalizar_dato(data[2], imcD_min, imcD_max)]
        for data in datos_entrenamiento]
    
    

    tam_entrada=2               # Entrada: Altura y peso
    tam_salida=1                # Salida: IMC
    learning_rate=0.005         # Aprendizaje
    repeticiones=10001            # Numero de repeticiones en el entrenamiento

    procesar_ocultas=[]
    """procesar_ocultas=[[2,2],[2],[5],[1,1,1,1,1]]"""
    
    procesar_ocultas.append([5 for _ in range(1)])   
    procesar_ocultas.append([10 for _ in range(2)])   
    procesar_ocultas.append([10 for _ in range(10)])   
    procesar_ocultas.append([50 for _ in range(5)])   
    procesar_ocultas.append([100 for _ in range(25)])   
    
    procesar=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000]
    cont=0

    rutaDir=os.path.dirname(os.path.abspath(__file__))
    

    for x in procesar_ocultas:
        cont=0
        RedN=RedNeuronal(tam_entrada,x,tam_salida)        
        print("Entrenamiento:",x)
        timeEntrStart = MPI.Wtime()

        for rep in range(repeticiones):
            for data in datos_entrenamiento_normalizados:
                entrada=data[:2]
                etiqueta=[data[2]]
                RedN.entrenar(entrada,etiqueta,learning_rate)
            if procesar[cont]==rep:                
                timeEntrEnd= MPI.Wtime()        
                print("{}\tTiempo de ejecucion: {}".format(procesar[cont],timeEntrEnd-timeEntrStart))
                ruta=os.path.join(rutaDir,'RedNeuronal{}x{}.txt'.format(len(x),x[0]))          
                with open(ruta, 'a') as archivo:                      
                    archivo.write(str(timeEntrEnd-timeEntrStart) + ', ')
                cont+=1
        print()   
        


    
    
    
    
    
    


main()
