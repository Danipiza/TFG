import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from mpi4py import MPI
import random
import sys
import os
import math

# EJECUTAR
# py RedesNeuronales2_1.py

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
    # (altura, peso, IMC)
    """datos_entrenamiento = [ [1.70, 60, 20.8],
                            [1.80, 90, 27.8],
                            [1.65, 55, 20.2],
                            [1.55, 70, 29.1],
                            [1.90, 100, 27.6],
                            [1.75, 65, 21.2],
                            [1.60, 50, 19.5],
                            [1.85, 80, 23.4],]"""
    #datos_entrenamiento=lee("datos80")
    datos_entrenamiento=lee("datos2042")    
    
    
    # (altura, peso)
    datos_prueba=[[1.52, 53.0, 22.94], [1.58, 72.0, 28.84], [1.92, 101.0, 27.4], [1.62, 66.0, 25.15], [1.96, 97.0, 25.25], [1.77, 70.0, 22.34], [1.8, 70.0, 21.6], [1.78, 61.0, 19.25], [1.72, 82.0, 27.72], [1.66, 67.0, 24.31], [1.59, 65.0, 25.71], [1.72, 77.0, 26.03], [1.62, 76.0, 28.96], [1.6, 62.0, 24.22], [1.92, 93.0, 25.23], [1.93, 70.0, 18.79], [1.68, 84.0, 29.76], [1.73, 57.0, 19.05], [1.98, 80.0, 20.41], [1.69, 61.0, 21.36], [1.69, 85.0, 29.76], [1.9, 107.0, 29.64], [1.87, 91.0, 26.02], [1.9, 106.0, 29.36], [1.75, 56.0, 18.29], [1.69, 74.0, 25.91], [1.69, 66.0, 23.11], [1.58, 70.0, 28.04], [1.78, 62.0, 19.57], [1.81, 66.0, 20.15], [1.94, 103.0, 27.37], [1.94, 85.0, 22.58], [1.83, 68.0, 20.31], [1.8, 98.0, 30.25], [1.54, 53.0, 22.35], [1.97, 70.0, 18.04], [1.8, 81.0, 25.0], [1.57, 65.0, 26.37], [1.7, 80.0, 27.68], [1.98, 103.0, 26.27], [1.77, 77.0, 24.58], [1.66, 76.0, 27.58], [1.71, 90.0, 30.78], [1.97, 106.0, 27.31], [1.99, 102.0, 25.76], [1.64, 60.0, 22.31], [1.75, 76.0, 24.82], [1.68, 76.0, 26.93], [1.86, 92.0, 26.59], [1.8, 73.0, 22.53]]
    
    datos_prueba_tam=len(datos_prueba)
    # peso[Kg]/altura^2[m]
    datos_prueba_IMC=[(datos_prueba[i][1]/datos_prueba[i][0]**2) for i in range(datos_prueba_tam)]

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
    

    datos_prueba_normalizados = [
            [normalizar_dato(data[0], alturaD_min, alturaD_max), 
            normalizar_dato(data[1], pesoD_min, pesoD_max),
            normalizar_dato(data[2], imcD_min, imcD_max)]
            for data in datos_prueba]
    
    # ----------------------------------------------------------------------------------------
    # --- Definir la red neuronal ------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    tam_entrada=2               # Entrada: Altura y peso
    tam_capas_ocultas=[5 for _ in range(1)]   # Tamaño de las capas ocultas (ejemplo)
    tam_salida=1                # Salida: IMC
    
    pesos=[[[-0.8862127498365708, 0.044455804130351106, -0.24315451980692337, 0.5944257250911558, -0.8659641504083082], [-0.12964407937954947, -0.5388623969967568, 0.9305994808483475, 0.6820897761878244, 0.45941731041235445]], [[-0.6545128025905118], [-0.980373941703389], [-0.7317483501902959], [-0.9176893589970425], [0.7127493647202121]]]
    
    precision=1
    learning_rate=[]
    learning_rateMax=0.5
    tam=int((learning_rateMax*100))        
    izq=1

    while izq<=tam:
        learning_rate.append(izq/100)
        izq+=precision  

    repeticiones_maximas=10              # Numero de repeticiones en el entrenamiento

    print("Tamaños de las capas ocultas: {}, numero de repeticiones: {}".format(tam_capas_ocultas, repeticiones_maximas))
    
    timeStart=MPI.Wtime()

    M=[]
    errores=[]
    repeticiones=[]
    
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

        err, rep=minimo_val(fila)
        errores.append(err)
        repeticiones.append(rep)

    timeEnd=MPI.Wtime()
    
    GUI(learning_rate, errores, repeticiones)
           

    

    print("\nTiempo de ejecucion Total: {}s".format(timeEnd-timeStart))
    


main()
