import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from mpi4py import MPI
import random
import sys
import os
import math

# EJECUTAR
# mpiexec -np 3 python RedesNeuronalesMPI2_1.py

"""
BUSQUEDA DE LA MEJOR TASA DE APRENDIZAJE Y NUMERO DE REPETICIONES
"""



def GUI(learning_rate,errores,repeticiones):    
    x=[lr*100 for lr in learning_rate]
    
    # Crear la figura y GridSpec
    fig = plt.figure(figsize=(10, 6))
    gs = GridSpec(2, 1, figure=fig)

    # Grafico 1 (arriba a la izquierda)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x, errores, color='b', linestyle='-')    
    ax1.set_xlabel('Learning Rate (%)')
    ax1.set_ylabel('Errores')
    ax1.set_title('Mejores')
    ax1.grid(True)

    # Grafico 2 (abajo a la izquierda)
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(x, repeticiones, color='b', linestyle='-')     
    ax2.set_xlabel('Learning Rate (%)')
    ax2.set_ylabel('Repeticiones')
    ax2.set_title('Mejores')
    ax2.grid(True)

        
    
    plt.tight_layout() # Ajustar la disposición de los subplots    
    plt.show() # Mostrar los gráficos

def lee(archivo):
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".Otros","ficheros","RedNeu", archivo+".txt")

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

# Le pasas una array de float y calcula el valor minimo y su indice (numero de repeticiones)
def minimo_val(fila):
    ret=float("inf")
    index=-1
    n=len(fila)
    for i in range(n):
        if ret>fila[i]: 
            ret=fila[i]
            index=i
    return ret, index


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

    datos_entrenamiento=[]  # Entrenamiento
    tam_datos=0             # Tam. Entrenamiento
    datos_prueba=[]         # Datos de Prueba
    datos_prueba_IMC=[]     # Etiquetas (Para calcular el fallo)

    datos_entrenamiento_normalizados=[]
    datos_prueba_normalizados=[]

    tam_entrada=0           # Entrada: Altura y peso
    tam_capas_ocultas=[]    # Tamaño de las capas ocultas (ejemplo)
    tam_salida=0            # Salida: IMC
    learning_rate=0.0       # Aprendizaje
    repeticiones_maximas=0  # Repeticiones

    pesos=[]

    # ----------------------------------------------------------------------------------------
    # --- INIT -------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    if myrank==MASTER:
        #datos_entrenamiento=lee("datos80")
        datos_entrenamiento=lee("datos2042")   
        tam_datos=len(datos_entrenamiento)
    
        
        datos_prueba=[[1.52, 53.0, 22.94], [1.58, 72.0, 28.84], [1.92, 101.0, 27.4], [1.62, 66.0, 25.15], [1.96, 97.0, 25.25], [1.77, 70.0, 22.34], [1.8, 70.0, 21.6], [1.78, 61.0, 19.25], [1.72, 82.0, 27.72], [1.66, 67.0, 24.31], [1.59, 65.0, 25.71], [1.72, 77.0, 26.03], [1.62, 76.0, 28.96], [1.6, 62.0, 24.22], [1.92, 93.0, 25.23], [1.93, 70.0, 18.79], [1.68, 84.0, 29.76], [1.73, 57.0, 19.05], [1.98, 80.0, 20.41], [1.69, 61.0, 21.36], [1.69, 85.0, 29.76], [1.9, 107.0, 29.64], [1.87, 91.0, 26.02], [1.9, 106.0, 29.36], [1.75, 56.0, 18.29], [1.69, 74.0, 25.91], [1.69, 66.0, 23.11], [1.58, 70.0, 28.04], [1.78, 62.0, 19.57], [1.81, 66.0, 20.15], [1.94, 103.0, 27.37], [1.94, 85.0, 22.58], [1.83, 68.0, 20.31], [1.8, 98.0, 30.25], [1.54, 53.0, 22.35], [1.97, 70.0, 18.04], [1.8, 81.0, 25.0], [1.57, 65.0, 26.37], [1.7, 80.0, 27.68], [1.98, 103.0, 26.27], [1.77, 77.0, 24.58], [1.66, 76.0, 27.58], [1.71, 90.0, 30.78], [1.97, 106.0, 27.31], [1.99, 102.0, 25.76], [1.64, 60.0, 22.31], [1.75, 76.0, 24.82], [1.68, 76.0, 26.93], [1.86, 92.0, 26.59], [1.8, 73.0, 22.53]]
        # ALEATORIOS, E IGUALES PARA TODOS LOS WORKERS (altura, peso) 
        """datos_prueba=[]    
        numAleatorios=50
        numeros_unicos = random.sample(range(0, tam_datos + 1), numAleatorios)
        for i in numeros_unicos:
            datos_prueba.append(datos_entrenamiento[i])"""
        
        
        
        datos_prueba_tam=len(datos_prueba)
        # peso[Kg]/altura^2[m]
        datos_prueba_IMC=[(datos_prueba[i][1]/datos_prueba[i][0]**2) for i in range(datos_prueba_tam)]

        
        
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
        

        datos_prueba_normalizados = [
            [normalizar_dato(data[0], alturaD_min, alturaD_max), 
            normalizar_dato(data[1], pesoD_min, pesoD_max),
            normalizar_dato(data[2], imcD_min, imcD_max)]
            for data in datos_prueba]
    
    
        # --- Definir la red neuronal --------------------------------------------------------
        tam_entrada=2               # Entrada: Altura y peso
        tam_capas_ocultas=[5 for _ in range(1)]   # Tamaño de las capas ocultas (ejemplo)
        tam_salida=1                # Salida: IMC

        """RedN=RedNeuronal(tam_entrada,tam_capas_ocultas,tam_salida, pesos=None)
        pesos=RedN.pesos"""
        
        pesos=[[[-0.8862127498365708, 0.044455804130351106, -0.24315451980692337, 0.5944257250911558, -0.8659641504083082], [-0.12964407937954947, -0.5388623969967568, 0.9305994808483475, 0.6820897761878244, 0.45941731041235445]], [[-0.6545128025905118], [-0.980373941703389], [-0.7317483501902959], [-0.9176893589970425], [0.7127493647202121]]]

        precision=1
        learning_rate=[]
        learning_rateMax=0.5
        tam=int((learning_rateMax*100)/numWorkers)
        mod=int((learning_rateMax*100)%numWorkers)        
        izq=1

        for i in range(1,mod+1):
            f=[]
            pos=izq
            while izq<=pos+tam:
                f.append(izq/100)
                izq+=precision
            #comm.send([j/100 for j in range(izq, izq+tam)],dest=i)
            comm.send(f,dest=i)
            learning_rate.append(f)
            
        for i in range(mod+1,numWorkers+1):
            f=[]
            pos=izq
            while izq<pos+tam:
                f.append(izq/100)
                izq+=precision
            #comm.send([j/100 for j in range(izq, izq+tam)],dest=i)
            comm.send(f,dest=i)
            learning_rate.append(f)

        
        #learning_rate=0.1            # Aprendizaje
        repeticiones_maximas=100      # Numero de repeticiones en el entrenamiento

        print("Tam. Capas Ocultas: {}, numero de repeticiones: {}".format(tam_capas_ocultas, repeticiones_maximas))
    else:
        learning_rate=comm.recv(source=MASTER)
    
    timeStart = MPI.Wtime()
    
    
    datos_entrenamiento_normalizados=comm.bcast(datos_entrenamiento_normalizados,root=MASTER)
    tam_datos=comm.bcast(tam_datos,root=MASTER)
    datos_prueba_normalizados=comm.bcast(datos_prueba_normalizados,root=MASTER)
    datos_prueba_IMC=comm.bcast(datos_prueba_IMC,root=MASTER)

    tam_entrada=comm.bcast(tam_entrada,root=MASTER)
    tam_capas_ocultas=comm.bcast(tam_capas_ocultas,root=MASTER)
    tam_salida=comm.bcast(tam_salida,root=MASTER)
    repeticiones_maximas=comm.bcast(repeticiones_maximas,root=MASTER)    
    pesos=comm.bcast(pesos,root=MASTER)
    
    
    
    """imcD_min=comm.bcast(imcD_min,root=MASTER)
    imcD_max=comm.bcast(imcD_max,root=MASTER)"""

    


    if myrank==MASTER:
        lr=[]
        for x in learning_rate:
            for y in x:
                lr.append(y)
        errores=[]
        repeticiones=[]

        for i in range(1,numWorkers+1):
            data=comm.recv(source=i)
            """print("WORKER ", i)"""
            for x in data:
                """print(x)"""
                errores.append(x[0])
                repeticiones.append(x[1])
        
        
        timeEnd = MPI.Wtime()
        print("Tiempo de Entrenamiento: {}s\n".format(timeEnd-timeStart))

        """print("LR=\n", lr)
        print("Errores=\n",errores)
        print("Reps=\n",repeticiones)"""
        GUI(lr, errores, repeticiones)
        


    else:
        M=[]        
        minVals=[]
        for tasa in learning_rate:
            fila=[]
            
            RedN=RedNeuronal(tam_entrada,tam_capas_ocultas,tam_salida, pesos)
            for _ in range(repeticiones_maximas):
                for data in datos_entrenamiento_normalizados:                    
                    entrada=data[:2]
                    etiqueta=[data[2]]
                    RedN.entrenar(entrada,etiqueta,tasa)
                
                fallo=0
                for data in datos_prueba_normalizados:
                    prediccion=RedN.forward(data[0:2])      
                    fallo+=abs(prediccion[0]-data[2])                
                fila.append(fallo)

            M.append(fila)
            minVals.append(minimo_val(fila))
        comm.send(minVals, dest=MASTER)

        """print("WORKER",myrank)
        for x in M:
            print(x)
        print()"""
        
        
        




   


    


main()
