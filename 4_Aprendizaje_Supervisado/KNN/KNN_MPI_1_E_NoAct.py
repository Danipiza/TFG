import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import os
import math

import queue

# EJECUTAR 
# mpiexec -np 5 python KNN_MPI_1_E_NoAct.py

"""
Algoritmo de clustering KNN (K-Nearest Neighbors). Con la primera mejora MPI.

NO actualiza valores

Se divide la poblacion inicial entre los workers, por lo que cada worker compara
    el que se esta prediciendo con n/numWorkers. Al finalizar una iteracion, los
    workers envian al master sus k vecinos mas cercanos y este se encarga de predecir.
    
Distancia entre individuso: Euclidea
  
Una vez terminado el algoritmo, la interfaz muestra la asignacion de la poblacion inivical a la izquierda, y 
a la derecha la asignacion final de los individuos a categorizar.
"""

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




def main():
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    # DATOS A COMPARTIR
    poblacionIni=[]
    asignacionIni=[]
    n=0
    poblacionProbar=[]
    m=0
    
    d=0
    k=0
    clusters=0


   

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    # Init
    if myrank==MASTER:                 
        poblacionIni=lee("1000_1_2D")
        asignacionIni=leeAsig("1000_1_2D") 
        n=len(poblacionIni)    

        poblacionProbar=lee("100000_2D")
        poblacionProbar=poblacionProbar[0:1000]
        m=len(poblacionProbar)

        clusters=7
        k=10

        d=len(poblacionIni[0])
        
    timeStart = MPI.Wtime()


    m=comm.bcast(m, root=MASTER)
    # Numero de vecinos
    k=comm.bcast(k, root=MASTER)
    # Numero de dimensiones de los individuos
    d=comm.bcast(d, root=MASTER)
    # Numero de clusters
    clusters=comm.bcast(clusters, root=MASTER)
    # Poblacion inicial
    poblacionProbar=comm.bcast(poblacionProbar, root=MASTER)
    
    
    
    
    if myrank==MASTER:       
        tamProc=n//numWorkers
        modulo=n%numWorkers
        izq=0
        der=tamProc+1

        # Hay al menos 1 elemento para cada worker.
        if tamProc>=1:  
            for i in range(1, modulo+1):    
                comm.send(poblacionIni[izq:der],dest=i)
                comm.send(asignacionIni[izq:der],dest=i)
                # update
                izq+=tamProc+1
                der+=tamProc+1
            der-=1
            # Hay algun worker con 1 elemento menos que los demas.
            for i in range(modulo+1,numWorkers+1):
                comm.send(poblacionIni[izq:der],dest=i)
                comm.send(asignacionIni[izq:der],dest=i)
                # update
                izq+=tamProc
                der+=tamProc    
        # No hay al menos 1 elemento para cada worker
        #   los workers que se queden sin elemento se finalizan.
        else:
            for i in range(1, modulo+1):  
                comm.send(poblacionIni[izq],dest=i)
                comm.send(asignacionIni[izq],dest=i)
                # update
                izq+=1							
            for i in range(modulo+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                  
            # Se reduce el numero de workers
            numWorkers-=numWorkers-modulo
        
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        
        				

        asignacionProbar=[]     
                
        cont=0
        
        while cont<m:           
                
            
            pq=MaxPriorityQueue()
            # TODO MEJORAR CON ANYSOURCE
            for i in range(1,numWorkers+1):
                dist=comm.recv(source=i)
                etiqs=comm.recv(source=i)
                for j in range(k):
                    if pq.size()<k: pq.push(etiqs[j],dist[j])     
                    elif pq.top_distancia()>dist[j]: 
                        """print("Master cambia por ", dist[j])    """       
                        pq.pop()
                        pq.push(etiqs[j],dist[j])

            # Cuenta el numero de vecinos mas cercanos para cada cluster
            etiquetas=[0 for i in range(clusters)]    
            for i in range(k):
                tmp=pq.pop()                
                etiquetas[tmp]+=1
            """print("MASTER, etiquetas=",etiquetas)"""
            # Coge el que mas tenga
            ret=0
            cantidad=etiquetas[0]
            for i in range(1,clusters):
                if cantidad<etiquetas[i]:
                    cantidad=etiquetas[i]
                    ret=i  
                            
            asignacionProbar.append(ret)
            
                    
            
            cont+=1
        
        timeEnd = MPI.Wtime()
        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))

        GUI(clusters,poblacionIni,asignacionIni,n, poblacionProbar,asignacionProbar,m)
    else : # WORKER        
        poblacionIni=comm.recv(source=MASTER)
        asignacionIni=comm.recv(source=MASTER)
        n=len(poblacionIni)
        
        for x in range(m):  
            pq = MaxPriorityQueue()       
            
            # Calcula todas las distancias y coge las k mas cercanas
            for i in range(n):
                distancia=0
                for j in range(d):
                    distancia+=(poblacionIni[i][j]-poblacionProbar[x][j])**2    
                distancia=math.sqrt(distancia)            
                
                # Si la cola de prioridad no es k, añadir la distancia
                if pq.size()<k: pq.push(asignacionIni[i],distancia)
                # Si distancia actual es menor a la mayor menor, 
                # se elimina la mayor e introduce la actual        
                elif pq.top_distancia()>distancia:            
                    pq.pop()
                    pq.push(asignacionIni[i],distancia)
            
            dists=[]
            etiq=[]
            for _ in range(k):
                dists.append(pq.top_distancia())
                etiq.append(pq.top_etiqueta())
                pq.pop()

            """print("(WORKER {}) dists={}, etiqs={}".format(myrank, dists, etiq))"""
            comm.send(dists,dest=MASTER)
            comm.send(etiq,dest=MASTER)

            
        exit(0)
        
        
        




main()