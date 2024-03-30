from mpi4py import MPI
import random
import sys
import os
import math

# EJECUTAR
# py RedesNeuronales2.py

# MEJORAR CADA WORKER SE ENCARGA DE VARIAS CAPAS DE LA CAPA OCULTA
# SE VAN ENVIANDO DATOS COMO EN UN PROCESADOR DIVIDIDO EN VARIAS ETAPAS


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
        
        self.capas=[tam_entrada] + tam_capas_ocultas + [tam_salida]
        
        # Inicializar los pesos de manera aleatoria
        self.pesos=[]
        for i in range(len(self.capas) - 1):
            pesos_capa = [[random.uniform(-1, 1) for _ in range(self.capas[i + 1])] for _ in range(self.capas[i])]
            self.pesos.append(pesos_capa)

    # Propagación hacia adelante (forward propagation)
    def forward(self,entrada):
        self.salidas=[entrada]
        # Recorre todas las capas (menos la de entrada) 
        for i in range(len(self.capas)-1):
            entradas_capa=self.salidas[-1]
            salidas_capa=[0 for _ in range(self.capas[i+1])]
            # Recorre todos los nodos de la capa actual
            for j in range(self.capas[i+1]):    
                suma=0
                # Suma todos los nodos de la capa anterior
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
                
        # Recorre todas las capas (menos la de salida) en orden inverso
        for i in range(len(self.capas) - 2, -1, -1):
            nuevos_errores=[0 for _ in range(self.capas[i])]
            # Recorre todos los nodos de la capa actual
            for j in range(self.capas[i]):
                suma=0
                # Suma todos los nodos de la capa anterior
                for k in range(self.capas[i+1]):            
                    suma+=errores[k]*self.pesos[i][j][k]
                nuevos_errores[j]=suma*sigmoide_derivado(self.salidas[i][j])

                # Actualiza los nodos
                for k in range(self.capas[i+1]):
                    self.pesos[i][j][k]+=learning_rate*errores[k]*self.salidas[i][j]

            errores = nuevos_errores

def main():
    # (altura, peso, IMC)
    datos_entrenamiento = [ [1.70, 60, 20.8],
                            [1.80, 90, 27.8],
                            [1.65, 55, 20.2],
                            [1.55, 70, 29.1],
                            [1.90, 100, 27.6],
                            [1.75, 65, 21.2],
                            [1.60, 50, 19.5],
                            [1.85, 80, 23.4],]
    
    # (altura, peso)
    datos_prueba = [[1.72, 68],
                    [1.90, 85],
                    [1.60, 50],]    
    datos_prueba_tam=len(datos_prueba)
    # peso[Kg]/altura^2[m]
    datos_prueba_IMC=[(datos_prueba[i][1]/datos_prueba[i][0]**2) for i in range(datos_prueba_tam)]

    # ----------------------------------------------------------------------------------------
    # --- Normalizar los datos ---------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    alturasD = [data[0] for data in datos_entrenamiento]
    pesosD = [data[1] for data in datos_entrenamiento]
    imcsD = [data[2] for data in datos_entrenamiento]

    alturaD_min = min(alturasD)
    alturaD_max = max(alturasD)
    pesoD_min = min(pesosD)
    pesoD_max = max(pesosD)
    imcD_min = min(imcsD)
    imcD_max = max(imcsD)

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
    tam_capas_ocultas=[10,10]   # Tamaño de las capas ocultas (ejemplo)
    tam_salida=1                # Salida: IMC
    
    learning_rate=0.1           # Aprendizaje
    repeticiones=100            # Numero de repeticiones en el entrenamiento

    RedN=RedNeuronal(tam_entrada,tam_capas_ocultas,tam_salida)
    print("Tamaños de las capas ocultas: {}, numero de repeticiones: {}".format(tam_capas_ocultas, repeticiones))

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
    print("\nTiempo de ejecucion Total: {}s".format(timeEnd-timeStart))


main()
