import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import os
import math

import queue

# mpiexec -np 5 python KnnMPI_2_E.py

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
    path=os.path.join(dir,".Otros","ficheros","KNN", archivo+".txt")

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
    path=os.path.join(dir,".Otros","ficheros","KNN","Asig", archivo+".txt")
    
        
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

        poblacionProbar=lee("10000_1_2D")
        m=len(poblacionProbar)

        clusters=7
        k=10

        d=len(poblacionIni[0])
        
    timeStart = MPI.Wtime()


    n=comm.bcast(n, root=MASTER)
    # Numero de vecinos
    k=comm.bcast(k, root=MASTER)
    # Numero de dimensiones de los individuos
    d=comm.bcast(d, root=MASTER)
    # Numero de clusters
    clusters=comm.bcast(clusters, root=MASTER)
    # Poblacion inicial
    poblacionIni=comm.bcast(poblacionIni, root=MASTER)
    # Asignacion inicial
    asignacionIni=comm.bcast(asignacionIni, root=MASTER)
    
    
    
    if myrank==MASTER:       
        tamProc=m//numWorkers
        modulo=m%numWorkers
        izq=0
        der=tamProc+1

        # Hay al menos 1 elemento para cada worker.
        if tamProc>=1:  
            for i in range(1, modulo+1):    
                comm.send(poblacionProbar[izq:der],dest=i)
                # update
                izq+=tamProc+1
                der+=tamProc+1
            der-=1
            # Hay algun worker con 1 elemento menos que los demas.
            for i in range(modulo+1,numWorkers+1):
                comm.send(poblacionProbar[izq:der],dest=i)
                # update
                izq+=tamProc
                der+=tamProc    
        # No hay al menos 1 elemento para cada worker
        #   los workers que se queden sin elemento se finalizan.
        else:
            for i in range(1, modulo+1):  
                comm.send(poblacionProbar[izq], dest=i)   
                # update
                izq+=1							
            for i in range(modulo+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                  
            # Se reduce el numero de workers
            numWorkers-=numWorkers-modulo
        
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        
        indices=[]
        izq=0
        if tamProc>=1:  
            for i in range(1, modulo+1):    
                indices.append(izq)                
                izq+=tamProc+1                
            for i in range(modulo+1,numWorkers+1):
                indices.append(izq)                
                izq+=tamProc  
        else:
            for i in range(1, modulo+1):  
                indices.append(izq)                
                izq+=1						

        asignacionProbar=[0 for _ in range(m)]        
                
        while numWorkers>0:            
            for i in range(1,numWorkers+1):
                data=comm.recv(source=i)
                asignacionProbar[indices[i-1]]=data
                indices[i-1]+=1
            
            # Continuan?
            tmp=0
            for i in range(1,numWorkers+1):
                data=comm.recv(source=i)
                if data==False:
                    tmp+=1            
            
            numWorkers-=tmp
        
        timeEnd = MPI.Wtime()
        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))

        GUI(clusters,poblacionIni,asignacionIni,n, poblacionProbar,asignacionProbar,m)
    else : # WORKER        
        poblacionProbar=comm.recv(source=MASTER)
        m=len(poblacionProbar)

        for x in range(m):  
            #print("(WORKER {})Iteracion: {}".format(myrank,x))
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
            
            comm.send(ret,dest=MASTER)
            comm.send(x!=m-1,dest=MASTER)           
            poblacionIni.append(poblacionProbar[x])
            asignacionIni.append(ret)
            n+=1
        exit(0)
        
        
        




main()