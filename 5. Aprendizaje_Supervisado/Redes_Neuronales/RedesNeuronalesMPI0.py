from mpi4py import MPI
import random
import os
import math

# EJECUTAR
# mpiexec -np 5 python RedesNeuronalesMPI0.py

# MEJORAR CADA WORKER SE ENCARGA DE VARIAS CAPAS DE LA CAPA OCULTA
# SE VAN ENVIANDO DATOS COMO EN UN PROCESADOR DIVIDIDO EN VARIAS ETAPAS


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
        
        self.capas=[tam_entrada] + tam_capas_ocultas + [tam_salida]
        
        # Inicializar los pesos de manera aleatoria
        self.pesos=[]
        for i in range(len(self.capas) - 1):
            pesos_capa = [[random.uniform(-1, 1) for _ in range(self.capas[i + 1])] for _ in range(self.capas[i])]
            self.pesos.append(pesos_capa)

    # Propagación hacia adelante (forward propagation)
    def forward(self,entrada):
        self.salidas=[entrada]
        # Recorre todas las capas (menos la de salida) 
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
                
        # Recorre todas las capas (menos la de entrada) en orden inverso
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
    comm=MPI.COMM_WORLD
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1 

    # (altura, peso, IMC)
    #datos_entrenamiento = lee("datos80")
    datos_entrenamiento = lee("datos2042")

    # (altura, peso)
    datos_prueba = [[1.72, 68],
                    [1.90, 85],
                    [1.60, 50]]
    datos_prueba_tam = len(datos_prueba)
    # peso[Kg]/altura^2[m]
    datos_prueba_IMC = [(datos_prueba[i][1] / datos_prueba[i][0] ** 2) for i in range(datos_prueba_tam)]

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

    tam_entrada = 2  # Entrada: Altura y peso
    tam_capas_ocultas = [10 for _ in range(2)]  # Tamaño de las capas ocultas (ejemplo)
    tam_salida = 1  # Salida: IMC

    # Mejor => lr=0.05 rep=1000
    learning_rate = 0.1  # Aprendizaje
    repeticiones = 100  # Numero de repeticiones en el entrenamiento

    RedN = RedNeuronal(tam_entrada, tam_capas_ocultas, tam_salida)
    if myrank == 0:
        print("Tamaños de las capas ocultas: {}, numero de repeticiones: {}".format(tam_capas_ocultas, repeticiones))

    # ----------------------------------------------------------------------------------------
    # --- Entrenamiento MPI ------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------
	# Se dividen entre los proceso los datos de entrenamiento
    timeStart=MPI.Wtime()
    if myrank==0:
        print("\nEntrenamiento:")

    tamProc=len(datos_entrenamiento_normalizados)//numProc
    izq=myrank*tamProc
    der=izq+tamProc

    for _ in range(repeticiones):
        for data in datos_entrenamiento_normalizados[izq:der]:
            entrada=data[:2]
            etiqueta=[data[2]]
            RedN.entrenar(entrada,etiqueta,learning_rate)

    # Sincronizar los pesos actualizados y sumarlos
    updated_weights=comm.gather(RedN.pesos, root=0)    
    if myrank == 0:
        for i in range(1, numProc):
            for j in range(len(updated_weights[i])):
                for k in range(len(updated_weights[i][j])):
                    for l in range(len(updated_weights[i][j][k])):
                        RedN.pesos[j][k][l]+=updated_weights[i][j][k][l]

    timeEntrEnd=MPI.Wtime()
    if myrank==0:
        print("Tiempo de ejecucion del entrenamiento: {}s\n".format(timeEntrEnd-timeStart))

    # ----------------------------------------------------------------------------------------
    # --- Predicciones ----------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    timePredStart=MPI.Wtime()
    #if myrank == 0:
    print("Predicciones Proceso {}:".format(myrank))

    local_predictions = []

    for i in range(datos_prueba_tam):
        local_prediccion_normalizada = RedN.forward(datos_prueba_normalizados[i])
        local_predictions.append(desnormalizar_dato(local_prediccion_normalizada[0], imcD_min, imcD_max))

    # Recolectar todas las predicciones
    for pred in local_predictions:            
        print(
            f"Altura: {datos_prueba[i][0]:.2f}m. Peso: {datos_prueba[i][1]:.2f}kg. "
            f"IMC Predicho: {pred:.3f}. IMC Real: {datos_prueba_IMC[i]:.3f}. Fallo: {abs(pred - datos_prueba_IMC[i]):.3f}"
        )

    timeEnd = MPI.Wtime()
    print("Tiempo de ejecucion Predicciones: {}s".format(timeEnd - timePredStart))
    print("\nTiempo de ejecucion Total: {}s".format(timeEnd - timeStart))


if __name__ == "__main__":
    main()
