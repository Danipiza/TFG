import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import random
import os
import math

import queue

# EJECUTA
# py KNN.py

"""
Algoritmo de clustering KNN  (K-Nearest Neighbors).

Distancia entre individuso:
    - Manhattan
    - Euclidea
  
Una vez terminado el algoritmo, la interfaz muestra la asignacion de la poblacion inivical a la izquierda, y 
a la derecha la asignacion final de los individuos a categorizar.
"""



# Tiempo de ejecucion total: 9.944005100056529 10000_2D, 1000_2D, k=3

class MaxPriorityQueue(queue.PriorityQueue):
    def __init__(self):
        super().__init__()

    def push(self, item, priority):
        super().put((-priority, item))

    def top_distancia(self):
        priority, _ = self.queue[0]  
        return -priority
    
    def top_etiqueta(self):
        _, item = self.queue[0]  
        return item
    
    def pop(self):
        _, item = super().get()
        return item
    
    def size(self):
        return self.qsize()

    



"""
SE PUEDE HACER CON workers
1. CADA worker PROCESA UNA INSTANCIA
2. CADA worker PROCESA MUCHAS INSTANCIAS PASADAS POR UN ARRAY

USAR BARRERAS PARA QUE CADA worker VAYAN AL MISMO TIEMPO
Y ASI REDUCIR LOS POSIBLES FALLOS DE CLASIFICACION

TODO K-MEDIAS...

TODO Algoritmos de clustering jerárquico aglomerativo

DISTANCIAS ENTRE INDIVIDUOS
    Manhattan
    Euclidea 
    Chebychev

CAMBIAR DISTANCIAS ENTRE CLUSTERS
    Centroide
    Enlace simple (single linkage) 
    Enlace completo (complete linkage):

ELECCION DE NUMERO DE CLUSTERS

REGIONES VORONOI

INDICES QUE MIDEN LO "COMPACTO" DE LA SOLUCION
    Dunn
    Davies-Bouldin 
    Coeficiente de silueta:

DIAGRAMAS DE CODO

VALIDACION CRUZADA

DENDOGRAMAS
"""

def lee(archivo):

    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".otros","ficheros","2_Cluster", archivo+".txt")

    with open(path, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')      
    for i in range(0, len(datos), 2):
        x = float(datos[i])
        y = float(datos[i + 1])

        array.append([x, y])

    #print("\n",array)        
    
    return array

def leeAsig(archivo):
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)
        
    if archivo==None: nombre_fichero=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".otros","ficheros","2_Cluster","Asig", archivo+".txt")
    
        
    array = [] 
    try:        
        with open(path, 'r') as archivo: # modo lectura
            for linea in archivo: # Solo hay una linea                
                numeros_en_linea = linea.split() # Divide por espacios                               
                for numero in numeros_en_linea:
                    array.append(int(numero))
    
    except FileNotFoundError:
        print("El archivo '{}' no existe.".format(nombre_fichero+".txt"))
    
    return array

def GUI(clusters, poblacionIni,asignacionIni,n, poblacionFin,asignacionFin,m):    
    # Definir los datos grafico 2
    colors = ['blue', 'red', 'green', 'pink', 'yellow', 'magenta', 'brown', 'darkgreen', 'gray', 'fuchsia',
            'violet', 'salmon', 'darkturquoise', 'forestgreen', 'firebrick', 'darkblue', 'lavender', 'palegoldenrod',
            'navy']
    
    # Crear figura y ejes
    fig, axs = plt.subplots(1,2, figsize=(12, 6))    
    
    x1=[[] for _ in range(clusters)]
    y1=[[] for _ in range(clusters)]
    
    for i in range(n):        
        x1[asignacionIni[i]].append(poblacionIni[i][0])
        y1[asignacionIni[i]].append(poblacionIni[i][1])          

    # Graficar
    for i in range(clusters):
        axs[0].scatter(x1[i], y1[i], color=colors[i])
    
    for i in range(m):
        axs[0].scatter(poblacionFin[i][0], poblacionFin[i][1], color="black")
    
    
    axs[0].set_xlabel('X')
    axs[0].set_ylabel('Y')
    axs[0].set_title('Poblacion Ini')


    for i in range(m):
        x1[asignacionFin[i]].append(poblacionFin[i][0])
        y1[asignacionFin[i]].append(poblacionFin[i][1]) 
    

    
    # Graficar 
    for i in range(clusters):
        axs[1].scatter(x1[i], y1[i], color=colors[i])    
    
    axs[1].set_xlabel('X')
    axs[1].set_ylabel('Y')
    axs[1].set_title('Poblacion Fin')
    


    # Mostrar la figura con ambos gráficos
    plt.tight_layout()
    plt.show()



"""
k>cluster, para que no haya posibles empates
"""
def knn_clasificador_unoE(poblacion, asignacion, clusters, individuo, k):
    
    n=len(poblacion)
    d=len(poblacion[0])
    pq = MaxPriorityQueue()

    

    #print("Asignacion=",asignacion)
    
    # Calcula todas las distancias y coge las k mas cercanas
    for i in range(n):
        distancia=0
        for j in range(d):
            distancia+=(poblacion[i][j]-individuo[j])**2    
        distancia=math.sqrt(distancia)
        
        
        #print("TopD={}, TopE={}".format(pq.top_distancia(),pq.top_etiqueta()))
        # Si la cola de prioridad no es k, añadir la distancia
        if pq.size()<k: pq.push(asignacion[i],distancia)
        # Si distancia actual es menor a la mayor menor, 
        # se elimina la mayor e introduce la actual        
        elif pq.top_distancia()>distancia:            
            pq.pop()
            pq.push(asignacion[i],distancia)

    # Cuenta el numero de vecinos mas cercanos para cada cluster
    etiquetas=[0 for i in range(clusters)]    
    for i in range(k):
        etiquetas[pq.pop()]+=1
    
    # Coge el que mas tenga
    ret=0
    cantidad=etiquetas[0]
    for i in range(1,clusters):
        if cantidad<etiquetas[i]:
            cantidad=etiquetas[i]
            ret=i
               
	
    return ret

def ejecuta_actualizarE(poblacion, asignacion, n, poblacionProbar, m, clusters, k):    
    print("Si Actualiza")
    totalTimeStart = MPI.Wtime()

    poblacionIni=[x for x in poblacion]
    asignacionIni=[x for x in asignacion]

    d=len(poblacion[0])

    asignacionProbar=[]    
    for x in range(m):                          
        pq = MaxPriorityQueue()        

        
        # Calcula todas las distancias y coge las k mas cercanas
        for i in range(n):
            distancia=0
            for j in range(d):
                distancia+=(poblacion[i][j]-poblacionProbar[x][j])**2    
            distancia=math.sqrt(distancia)            
            
            # Si la cola de prioridad no es k, añadir la distancia
            if pq.size()<k: pq.push(asignacion[i],distancia)
            # Si distancia actual es menor a la mayor menor, 
            # se elimina la mayor e introduce la actual        
            elif pq.top_distancia()>distancia:            
                pq.pop()
                pq.push(asignacion[i],distancia)

        # Cuenta el numero de vecinos mas cercanos para cada cluster
        etiquetas=[0 for i in range(clusters)]    
        for i in range(k):
            etiquetas[pq.pop()]+=1
        
        # Coge el que mas tenga
        ret=0
        cantidad=etiquetas[0]
        for i in range(1,clusters):
            if cantidad<etiquetas[i]:
                cantidad=etiquetas[i]
                ret=i                
        
        asignacionProbar.append(ret)
        poblacion.append(poblacionProbar[x])
        asignacion.append(ret)
        n+=1
    
    totalTimeEnd = MPI.Wtime()
    print("Tiempo de ejecucion total: {}".format(totalTimeEnd-totalTimeStart))
    
    print("len(poblacion)={}, len(asignacion)={}".format(len(poblacionIni),len(asignacionIni)))
    
    GUI(clusters,poblacionIni,asignacionIni,n-m, poblacionProbar,asignacionProbar,m)


# Ejecuta sin almacenar 
def ejecuta_sin_actualizarE(poblacionIni, asignacionIni, n, poblacionProbar, m, clusters, k):    
    print("No Actualiza")
    totalTimeStart = MPI.Wtime()
        
    asignacionProbar=[]
    for i in range(m):           
        asignacionProbar.append(knn_clasificador_unoE(poblacionIni, asignacionIni, clusters, poblacionProbar[i],k))
    
    totalTimeEnd = MPI.Wtime()
    print("Tiempo de ejecucion total: {}".format(totalTimeEnd-totalTimeStart))
    
    
    
    GUI(clusters,poblacionIni,asignacionIni,n, poblacionProbar,asignacionProbar,m)

"""
k>cluster, para que no haya posibles empates
"""
def knn_clasificador_unoM(poblacion, asignacion, clusters, individuo, k):
    n=len(poblacion)
    d=len(poblacion[0])
    pq = MaxPriorityQueue()

    

    #print("Asignacion=",asignacion)
    
    # Calcula todas las distancias y coge las k mas cercanas
    for i in range(n):
        distancia=0
        for j in range(d):
            distancia+=abs(poblacion[i][j]-individuo[j])
        
        
        #print("TopD={}, TopE={}".format(pq.top_distancia(),pq.top_etiqueta()))
        # Si la cola de prioridad no es k, añadir la distancia
        if pq.size()<k: pq.push(asignacion[i],distancia)
        # Si distancia actual es menor a la mayor menor, 
        # se elimina la mayor e introduce la actual        
        elif pq.top_distancia()>distancia:            
            pq.pop()
            pq.push(asignacion[i],distancia)

    # Cuenta el numero de vecinos mas cercanos para cada cluster
    etiquetas=[0 for i in range(clusters)]    
    for i in range(k):
        etiquetas[pq.pop()]+=1
    
    # Coge el que mas tenga
    ret=0
    cantidad=etiquetas[0]
    for i in range(1,clusters):
        if cantidad<etiquetas[i]:
            cantidad=etiquetas[i]
            ret=i
               
	
    return ret

def ejecuta_actualizarM(poblacion, asignacion, n, poblacionProbar, m, clusters, k):    
    print("Si Actualiza")
    totalTimeStart = MPI.Wtime()

    poblacionIni=[x for x in poblacion]
    asignacionIni=[x for x in asignacion]

    d=len(poblacion[0])

    asignacionProbar=[]    
    for x in range(m):                          
        pq = MaxPriorityQueue()        

        
        # Calcula todas las distancias y coge las k mas cercanas
        for i in range(n):
            distancia=0
            for j in range(d):
                distancia+=abs(poblacion[i][j]-poblacionProbar[x][j])      
            
            # Si la cola de prioridad no es k, añadir la distancia
            if pq.size()<k: pq.push(asignacion[i],distancia)
            # Si distancia actual es menor a la mayor menor, 
            # se elimina la mayor e introduce la actual        
            elif pq.top_distancia()>distancia:            
                pq.pop()
                pq.push(asignacion[i],distancia)

        # Cuenta el numero de vecinos mas cercanos para cada cluster
        etiquetas=[0 for i in range(clusters)]    
        for i in range(k):
            etiquetas[pq.pop()]+=1
        
        # Coge el que mas tenga
        ret=0
        cantidad=etiquetas[0]
        for i in range(1,clusters):
            if cantidad<etiquetas[i]:
                cantidad=etiquetas[i]
                ret=i                
        
        asignacionProbar.append(ret)
        poblacion.append(poblacionProbar[x])
        asignacion.append(ret)
        n+=1
    
    totalTimeEnd = MPI.Wtime()
    print("Tiempo de ejecucion total: {}".format(totalTimeEnd-totalTimeStart))
    
    print("len(poblacion)={}, len(asignacion)={}".format(len(poblacionIni),len(asignacionIni)))
    
    GUI(clusters,poblacionIni,asignacionIni,n-m, poblacionProbar,asignacionProbar,m)


# Ejecuta sin almacenar 
def ejecuta_sin_actualizarM(poblacionIni, asignacionIni, n, poblacionProbar, m, clusters, k):    
    print("No Actualiza")
    totalTimeStart = MPI.Wtime()
        
    asignacionProbar=[]
    for i in range(m):           
        asignacionProbar.append(knn_clasificador_unoM(poblacionIni, asignacionIni, clusters, poblacionProbar[i],k))
    
    totalTimeEnd = MPI.Wtime()
    print("Tiempo de ejecucion total: {}".format(totalTimeEnd-totalTimeStart))
    
    
    
    GUI(clusters,poblacionIni,asignacionIni,n, poblacionProbar,asignacionProbar,m)


def main():
    # 100_1_2D 7
    poblacionIni=lee("1000_1_2D")
    asignacionIni=leeAsig("1000_1_2D") 
    n=len(poblacionIni)    
    
    poblacionProbar=lee("100000_2D")
    poblacionProbar=poblacionProbar[0:1000]
    m=len(poblacionProbar)
    
    clusters=4
    k=10
    distancia=1
    distancia_opt=["Manhattan", "Euclidea"]
    actualiza=1
    
    print("Poblacion Ini: {}\tPoblacion Probar: {}\tk= {}\tDistancia {}".format(n, m, k,
            distancia_opt[distancia]), end="\t")

    if distancia==0:
        if actualiza==0:
            ejecuta_sin_actualizarM(poblacionIni, asignacionIni, n, poblacionProbar, m, clusters, k)
        else:
            ejecuta_actualizarM(poblacionIni, asignacionIni, n, poblacionProbar, m, clusters, k)
    else:   
        if actualiza==0:
            ejecuta_sin_actualizarE(poblacionIni, asignacionIni, n, poblacionProbar, m, clusters, k)
        else:
            ejecuta_actualizarE(poblacionIni, asignacionIni, n, poblacionProbar, m, clusters, k)
    



main()