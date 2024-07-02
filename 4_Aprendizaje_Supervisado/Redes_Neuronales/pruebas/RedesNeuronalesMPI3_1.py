import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from mpi4py import MPI
import random
import sys
import os
import math


# EJECUTAR
# mpiexec -np 3 python RedesNeuronalesMPI3_1.py


""" 
SE PODRIA USAR gather PERO ES MEJOR RECIBIR DE UNO EN UNO PARA NO AUMENTAR EL ESPACIO

"Fine tunning" NO ES PERO LA IDEA ES PARECIDA
    CREAR VARIOS PROCESOS, CADA PROCESO SE ENCARGA DE UNA PARTE
    DE LOS DATOS Y AL FINALIZAR LOS ENTRENAMIENTOS EL MASTER LOS JUNTA
    HACIENDO LA MEDIA PARA COMPROBAR COMO FUNCIONA.

TAMBIEN SE PUEDE MEZCLAR CON LA PRUEBA ANTERIOR PARA BUSCAR UNA
    TASA DE APRENDIZAJE BUENA Y ASI MEJORAR LA PREDICCION FINAL.

COMPROBAR CON DISTINTAS COMBINACIONES DE POBLACIONES:
    - POBLACIONES ORDENADAS 
        (CADA WORKER SE ENCARGA DE UNA POBLACION CON UNOS PARAMETROS PARECIDOS)
    - POBLACIONES DEORDENADAS
        (CADA WORKER SE ENCARGA DE POBLACION ALEATORIA)

    Da mejores resultados con valores deordenaros, pero puede que no sea general, es decir,
        puede que con otro tipo de datos de entrada no mejore
        
    - MISMA POBLACION (DISTINTOS PESOS INCIALES, TASA DE APRENDIZAJE)

COMBINACIONES DE learning_rates ? 
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

# Funcion de activacion
def sigmoide(x):
    return 1/(1+math.exp(-x))
#Derivada (para el entrenamiento)
def sigmoide_derivado(x):
    return x*(1-x)


class RedNeuronal:
    def __init__(self, tam_entrada, tam_capas_ocultas, tam_salida, pesos):
        self.tam_entrada=tam_entrada
        self.tam_capas_ocultas=tam_capas_ocultas
        self.tam_salida=tam_salida
        
        self.capas=[tam_entrada]+tam_capas_ocultas+[tam_salida]
        
        if pesos==None: # Inicializar los pesos de manera aleatoria            
            self.pesos=[]
            for i in range(len(self.capas)-1):
                pesos_capa = [[random.uniform(-1, 1) for _ in range(self.capas[i + 1])] for _ in range(self.capas[i])]
                self.pesos.append(pesos_capa)
        else: self.pesos=pesos
        
        

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
    MASTER=0
    comm=MPI.COMM_WORLD
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    # ----------------------------------------------------------------------------------------
    # --- VARIABLES A COMPARTIR --------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    datos_entrenamiento_normalizados=[]

    tam_entrada=0           # Entrada: Altura y peso
    tam_capas_ocultas=[]    # Tamaño de las capas ocultas (ejemplo)
    tam_salida=0            # Salida: IMC
    learning_rate=0.0       # Aprendizaje
    repeticiones=0

    pesos=[]

    # ----------------------------------------------------------------------------------------
    # --- INIT -------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    if myrank==MASTER:
        datos_entrenamiento=lee("datos80")
        #datos_entrenamiento=lee("datos2042S")   
        tam_datos=len(datos_entrenamiento)
         
               
        # --- Normalizar los datos -----------------------------------------------------------       
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
        

       
    
        # --- Definir la red neuronal --------------------------------------------------------
        tam_entrada=2               # Entrada: Altura y peso
        tam_capas_ocultas=[10 for _ in range(3)]   # Tamaño de las capas ocultas (ejemplo)
        tam_salida=1                # Salida: IMC


        # PESOS IGUALES PARA TODAS LAS REDES
        RedN=RedNeuronal(tam_entrada,tam_capas_ocultas,tam_salida, pesos=None)
        pesos=RedN.pesos        
        
        
        
        learning_rate=0.1       
        repeticiones=100      # Numero de repeticiones en el entrenamiento

        tam=tam_datos//numWorkers
        mod=tam_datos%numWorkers
        izq=0

        

        for i in range(1,mod+1):            
            comm.send(datos_entrenamiento_normalizados[izq:izq+tam+1],dest=i)
            izq+=tam+1
            
        for i in range(mod+1,numWorkers+1):
            comm.send(datos_entrenamiento_normalizados[izq:izq+tam],dest=i)
            izq+=tam

        
    else:
        # Reciben su poblacion para entrenar
        datos_entrenamiento_normalizados=comm.recv(source=MASTER)
        tam_datos=len(datos_entrenamiento_normalizados)
        
    
    timeStart = MPI.Wtime()
    
    tam_entrada=comm.bcast(tam_entrada,root=MASTER)
    tam_capas_ocultas=comm.bcast(tam_capas_ocultas,root=MASTER)
    tam_salida=comm.bcast(tam_salida,root=MASTER)
    pesos=comm.bcast(pesos,root=MASTER)

    repeticiones=comm.bcast(repeticiones,root=MASTER)   
    learning_rate=comm.bcast(learning_rate,root=MASTER)     
    

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
        timeEntrStart = MPI.Wtime()  
    
        if myrank==MASTER:          
            
            
            RedN=RedNeuronal(tam_entrada,x,tam_salida, None)

            # Inicializa los pesos a 0 para la suma
            for i in range(len(RedN.pesos)):
                for j in range(len(RedN.pesos[i])):
                    for k in range(len(RedN.pesos[i][j])):
                        RedN.pesos[i][j][k]=0
            
            for i in range(1,numWorkers+1):
                data=comm.recv(source=i) 
                if data==-1: break

                for i in range(len(RedN.pesos)):
                    for j in range(len(RedN.pesos[i])):
                        for k in range(len(RedN.pesos[i][j])):
                            RedN.pesos[i][j][k]+=data[i][j][k]/numWorkers         
                
               
                
                        
                
            

        else: 
            
            
            RedN=RedNeuronal(tam_entrada,x,tam_salida, None)
            
            for rep in range(repeticiones):
                for data in datos_entrenamiento_normalizados:                 
                    entrada=data[:2]
                    etiqueta=[data[2]]
                    
                    RedN.entrenar(entrada,etiqueta,learning_rate)

                if myrank==1 and procesar[cont]==rep:  
                    timeEntrEnd= MPI.Wtime()        
                    print("{}\tTiempo de ejecucion: {}".format(procesar[cont],timeEntrEnd-timeEntrStart))
                    ruta=os.path.join(rutaDir,'RedNeuronal_MPI{}_{}x{}.txt'.format(numWorkers,len(x),x[0]))          
                    with open(ruta, 'a') as archivo:                      
                        archivo.write(str(timeEntrEnd-timeEntrStart) + ', ')
                    cont+=1
            comm.send(RedN.pesos, dest=MASTER) 
            
                
            


    
    

        
        
        




   


    


main()
