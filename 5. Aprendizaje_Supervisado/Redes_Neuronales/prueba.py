from mpi4py import MPI
import random
import os
import math
import time

"""
Tam. poblacion: 2042            Num. Repeticiones: 1
Capa Master: 2
Capa Oculta 1: 10
Capa Salida: 1
Tiempo de Entrenamiento: 3.544421600061469s

Tam. poblacion: 2042            Num. Repeticiones: 1
Capa Master: 2
Capa Oculta 1: 10
Capa Oculta 2: 10
Capa Salida: 1
Tiempo de Entrenamiento: 5.841621599975042s
"""


tiempoF=0
tiempoB=0
tiempoE=0
contF=0
contB=0
contE=0

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
        global tiempoF, contF
        self.salidas=[entrada]
        # Recorre todas las capas (menos la de salida) 
        for i in range(len(self.capas)-1):
            tStart=MPI.Wtime()

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
            tEnd=MPI.Wtime()
            tiempoF+=(tEnd-tStart)
            contF+=1
        
        # Devuelve el ultimo elemento        
        return self.salidas[-1] 

    # Retropropagación (backpropagation)
    def entrenar(self, entrada, etiqueta, learning_rate):
        global tiempoB, contB, tiempoE, contE
        self.forward(entrada)
        errores=[]
        for i in range(self.tam_salida):
            tStart=MPI.Wtime()

            errores.append((etiqueta[i]-self.salidas[-1][i])*sigmoide_derivado(self.salidas[-1][i]))

            tEnd=MPI.Wtime()
            tiempoE+=(tEnd-tStart)
            contE+=1
                        
        # Recorre todas las capas (menos la de entrada) en orden inverso
        for i in range(len(self.capas) - 2, -1, -1):
            tStart=MPI.Wtime()
            
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

            tEnd=MPI.Wtime()
            tiempoB+=(tEnd-tStart)
            contB+=1

def red_neuronal():
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
    tam_poblacion=len(datos_entrenamiento)    
    
    
    # (altura, peso)
    datos_prueba=[[1.72, 68],
                  [1.90, 85],
                  [1.60, 50]]    
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
         normalizar_dato(data[1], pesoD_min, pesoD_max)]
        for data in datos_prueba]
    
    # ----------------------------------------------------------------------------------------
    # --- Definir la red neuronal ------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    tam_entrada=2               # Entrada: Altura y peso
    tam_capas_ocultas=[10 for _ in range(2)]   # Tamaño de las capas ocultas (ejemplo)
    tam_salida=1                # Salida: IMC

    # Mejor => lr=0.05 rep=1000
    learning_rate=0.1           # Aprendizaje
    repeticiones=100              # Numero de repeticiones en el entrenamiento

    RedN=RedNeuronal(tam_entrada,tam_capas_ocultas,tam_salida)
    print("Tam. Poblacion: {}\tTam. Capas ocultas: {}\tNum. Repeticiones: {}\n".format(tam_poblacion, tam_capas_ocultas, repeticiones))

    # ----------------------------------------------------------------------------------------
    # --- Entrenamiento ----------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------
    

    timeStart = MPI.Wtime()
    print("\nEntrenamiento:")

    for _ in range(repeticiones):
        for data in datos_entrenamiento_normalizados:
            entrada=data[:2]
            etiqueta=[data[2]]
            RedN.entrenar(entrada,etiqueta,learning_rate)
    timeEntrEnd = MPI.Wtime()
    print("Tiempo de ejecución del entrenamiento: {}s\n".format(timeEntrEnd-timeStart))


    # ----------------------------------------------------------------------------------------
    # --- Entrenamiento ----------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    timePredStart=MPI.Wtime()
    print("Predicciones:")
    
    for i in range(datos_prueba_tam):
        prediccion_normalizada=RedN.forward(datos_prueba_normalizados[i])        
        prediccion=desnormalizar_dato(prediccion_normalizada[0],imcD_min,imcD_max)
       
        print(  f"Altura: {datos_prueba[i][0]:.2f}m. Peso: {datos_prueba[i][1]:.2f}kg. "
                f"IMC Predicho: {prediccion:.3f}. IMC Real: {datos_prueba_IMC[i]:.3f}. Fallo: {abs(prediccion-datos_prueba_IMC[i]):.3f}")

    timeEnd=MPI.Wtime()
    print("Tiempo de ejecucion Predicciones: {}s".format(timeEnd-timePredStart))
    print("\nTiempo de ejecucion Total: {}s\n".format(timeEnd-timeStart))
    
    print("Tiempo de forward medio: {}".format(tiempoF/contF))
    print("Tiempo de backpropagation medio: {}".format(tiempoB/contB))
    print("Tiempo de error medio: {}\n".format(tiempoE/contE))
    



def main():
    repeticiones=1
    tam_poblacion=2042

    capas=4
    """
    tiempoF=5.758284188196001e-06
    tiempoB=1.0545260192801458e-05
    tiempoE=2.688095571033576e-07

    tiempoF=0.000005758284188196001
    tiempoB=0.000010545260192801458
    tiempoE=0.000000268809557103357
    """
    """tiempoF=0.000001
    tiempoB=0.000002
    tiempoE=0.0000008"""
    tiempoF=5.758284188196001e-06
    tiempoB=1.0545260192801458e-05
    tiempoE=2.688095571033576e-07

    aux=""
    for i in range(1,capas-1):
        aux+="Capa Oculta {}: {}\n".format(i,10)
    print("Tam. poblacion: {}\t\tNum. Repeticiones: {}".format(tam_poblacion, repeticiones))
    print("Capa Master: {}\n{}Capa Salida: {}".format(2,aux,1))

    timeEntrStart = MPI.Wtime()
    for _ in range(repeticiones):
        for _ in range(tam_poblacion):
            for _ in range(capas-1):
                time.sleep(tiempoF)
            time.sleep(tiempoE)
            for _ in range(capas-1):
                time.sleep(tiempoB)

    timeEntrEnd = MPI.Wtime()
    print("Tiempo de Entrenamiento: {}s\n".format(timeEntrEnd-timeEntrStart))
    

#red_neuronal()

main()