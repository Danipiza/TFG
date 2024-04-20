from mpi4py import MPI
import random
import sys
import os
import math

# EJECUTAR
# py RedesNeuronales1.py


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
    def __init__(self, tam_entrada, tam_oculta, tam_salida=None):
        self.tam_entrada=tam_entrada
        self.tam_oculta=tam_oculta

        self.entradas_oculta=[]
        self.salidas_oculta=[]
        self.salida=0.0

        # Inicializar los pesos de manera aleatoria        
        
        self.pesos_entrada_oculta=[[random.uniform(-1, 1) for _ in range(self.tam_oculta)] for _ in range(self.tam_entrada)]        
        self.pesos_salida_oculta=[random.uniform(-1, 1) for _ in range(self.tam_oculta)]
        

        """self.pesos_entrada_oculta=[[0.33586051475778667, 0.04865394057108752, 0.32946261101217966, 0.22869094964703596, 0.9771201021055296], [-0.6810104847358278, -0.06055518782126046, -0.6328324830100489, 0.7619612558605722, 0.8769042816683505]]
        self.pesos_salida_oculta=[0.6075948464616394, -0.6070452781745583, -0.30293535175767183, -0.2358202682424062, -0.5777739940220865]
        """

    # Propagacion hacia adelante (forward propagation)
    def forward(self,entrada):        
        self.entradas_oculta=[]
        for i in range(self.tam_oculta):
            suma=0.0
            for j in range(self.tam_entrada):
                suma+=entrada[j]*self.pesos_entrada_oculta[j][i]
            self.entradas_oculta.append(suma)

        self.salidas_oculta=[]
        for i in range(self.tam_oculta):
            self.salidas_oculta.append(sigmoide(self.entradas_oculta[i]))       
                
        
        suma = 0.0
        for j in range(self.tam_oculta):
            suma+=self.salidas_oculta[j]*self.pesos_salida_oculta[j]
        self.entradas_salida=[suma]
        
        self.salida=sigmoide(self.entradas_salida[0])
                
        return self.salida

    # retropropagacion (backpropagation) 
    def entrenar(self,entrada,etiqueta,learning_rate):

        self.forward(entrada) # Propagacion hacia adelante
        
        # Calcular el error de la capa de salida
        errores_salida=etiqueta[0]-self.salida
        deltas_salida=errores_salida*sigmoide_derivado(self.salida)
        # Actualizar los pesos de la capa de salida
        for i in range(self.tam_oculta):
            self.pesos_salida_oculta[i]+=learning_rate*deltas_salida*self.salidas_oculta[i]

        # Calcular los errores de la capa oculta (TODO SE PUEDEN JUNTAR)
        errores_oculta=[self.pesos_salida_oculta[i]*deltas_salida for i in range(self.tam_oculta)]
        deltas_oculta=[]
        for i in range(self.tam_oculta):
            deltas_oculta.append(errores_oculta[i]*sigmoide_derivado(self.salidas_oculta[i]))
        # Actualizar los pesos de la capa oculta
        for i in range(self.tam_entrada):
            for j in range(self.tam_oculta):
                self.pesos_entrada_oculta[i][j]+=learning_rate*deltas_oculta[j]*entrada[i]







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
    
    # (Num de nodos)
    tam_entrada=2         # Entrada: Altura y peso
    tam_oculta=5         # Tamaño de la capa oculta 
    tam_salida=1          # Salida: IMC
    
    # Mejor => lr=0.05 rep=1000
    learning_rate=0.1     # Aprendizaje 
    repeticiones=100      # Numero de repeticiones en el entrenamiento
    
    RedN=RedNeuronal(tam_entrada,tam_oculta,tam_salida)
    
    print("Tam.Poblacion: {} \tTam. Capa oculta: {} \tNumero de repeticiones: {}\n".format(len(datos_entrenamiento), tam_oculta,repeticiones))
    # ----------------------------------------------------------------------------------------
    # --- Entrenamiento ----------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------
    
    timeStart=MPI.Wtime()
    print("Entrenamiento:")

    for _ in range(repeticiones):
        for data in datos_entrenamiento_normalizados:
            entrada=data[:2]
            etiqueta=[data[2]]
            RedN.entrenar(entrada,etiqueta,learning_rate)
    timeEntrEnd=MPI.Wtime()
    print("Tiempo de ejecucion Entrenamiento: {}s\n".format(timeEntrEnd-timeStart))   

    # ----------------------------------------------------------------------------------------
    # --- Prediccion -------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    timePredStart=MPI.Wtime()
    print("Predicciones:")
    
    for i in range(datos_prueba_tam):
        prediccion_normalizada=RedN.forward(datos_prueba_normalizados[i])        
        prediccion=desnormalizar_dato(prediccion_normalizada,imcD_min,imcD_max)
       
        print(  f"Altura: {datos_prueba[i][0]:.2f}m. Peso: {datos_prueba[i][1]:.2f}kg. "
                f"IMC Predicho: {prediccion:.3f}. IMC Real: {datos_prueba_IMC[i]:.3f}. Fallo: {abs(prediccion-datos_prueba_IMC[i]):.3f}")

    timeEnd=MPI.Wtime()
    print("Tiempo de ejecucion Predicciones: {}s".format(timeEnd-timePredStart))
    print("\nTiempo de ejecucion Total: {}s".format(timeEnd-timeStart))


main()

