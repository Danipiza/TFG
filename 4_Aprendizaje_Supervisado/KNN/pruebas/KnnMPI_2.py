import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import os
import math

import queue

# mpiexec -np 5 python KnnMPI_2.py
"""
Se divide la poblacion a probar entre los workers. Al finalizar una iteracion, los
    workers envian al master el individuo y su asignacion.

"""

ruta_Act = os.path.dirname(os.path.abspath(__file__))


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
    path=os.path.join(dir,".Otros","ficheros","2.Cluster", archivo+".txt")

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
    path=os.path.join(dir,".Otros","ficheros","2.Cluster","Asig", archivo+".txt")
    
        
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
        m=len(poblacionProbar)

        
        
          

        directorio_script = os.path.dirname(os.path.abspath(__file__))
        ruta_Act=os.path.join(directorio_script, 'Actualiza')
        ruta_NoAct=os.path.join(directorio_script, 'No_Actualiza')
        ruta_Tam=os.path.join(directorio_script, 'Tam_Datos2MPI{}.txt'.format(numWorkers))

        d=len(poblacionIni[0])
    
    

    clusters=4
    procesar=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000]
    val=10250
    for i in range(1,361):
        procesar.append(val)
        val+=250
    k=15


    poblacionIni=comm.bcast(poblacionIni, root=MASTER)
    asignacionIni=comm.bcast(asignacionIni, root=MASTER)
    n=comm.bcast(n, root=MASTER)
    m=comm.bcast(m, root=MASTER)
    d=comm.bcast(d, root=MASTER)    
    # Poblacion 
    
    

    ini=[]
    iniAsig=[]
    for y in poblacionIni:
        ini.append(y)
    for y in asignacionIni:
        iniAsig.append(y)

        
    """# ---------------------------------------------------------------------------
    # --- MANHATTAN -------------------------------------------------------------
    # ---------------------------------------------------------------------------
    totalTimeStart = MPI.Wtime()
    
    ejecuta_NoAct_M(comm,myrank, numWorkers, 
                n, x, d, clusters, ini, iniAsig, poblacionProbar[0:x], k)
    totalTimeEnd = MPI.Wtime()

    
    if myrank==MASTER: 
        #print("(k={}) Manhattan_NoAct:\t\t{}".format(k,totalTimeEnd-totalTimeStart))   
        
        ruta=os.path.join(ruta_NoAct,'KNN_2MPI{}_NoAct_k{}_M.txt'.format(numWorkers,k)) 
        with open(ruta, 'a') as archivo:
            # Escribir un número flotante en el archivo                                
            archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')


    # ---------------------------------------------------------------------------
    # --- EUCLIDEA --------------------------------------------------------------
    # ---------------------------------------------------------------------------

    totalTimeStart = MPI.Wtime()
    
    ejecuta_NoAct_E(comm,myrank, numWorkers, 
                n, x, d, clusters, ini, iniAsig, poblacionProbar[0:x], k)
    totalTimeEnd = MPI.Wtime()

    
    if myrank==MASTER: 
        #print("(k={}) Euclidea_NoAct:\t\t{}".format(k,totalTimeEnd-totalTimeStart))           
        
        ruta=os.path.join(ruta_NoAct,'KNN_2MPI{}_NoAct_k{}_E.txt'.format(numWorkers,k)) 
        with open(ruta, 'a') as archivo:
            # Escribir un número flotante en el archivo                                
            archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')


    # --- ACTUALIZA -------------------------------------------------------------

    # ---------------------------------------------------------------------------
    # --- MANHATTAN -------------------------------------------------------------
    # ---------------------------------------------------------------------------
    totalTimeStart = MPI.Wtime()
    
    
    ejecuta_Act_M(comm,myrank, numWorkers, 
                n, x, d, clusters, ini, iniAsig, poblacionProbar[0:x], k)
    totalTimeEnd = MPI.Wtime()

    
    if myrank==MASTER: 
        #print("(k={}) Manhattan_Act:\t\t{}".format(k,totalTimeEnd-totalTimeStart))   
        
        ruta=os.path.join(ruta_Act,'KNN_2MPI{}_Act_k{}_M.txt'.format(numWorkers,k))  
        with open(ruta, 'a') as archivo:
            # Escribir un número flotante en el archivo                                
            archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')"""


    # ---------------------------------------------------------------------------
    # --- EUCLIDEA --------------------------------------------------------------
    # ---------------------------------------------------------------------------
    
    
    
    ejecuta_Act_E(comm,myrank, numWorkers, 
                n, m, d, clusters, ini, iniAsig, poblacionProbar, k,procesar)

   


def ejecuta_Act_E(comm, myrank, numWorkers, 
             n, m, d, clusters, poblacionIni, asignacionIni, poblacionProbar, k,procesar):  

    MASTER=0
    END_OF_PROCESSING=-2
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
        totalTimeStart = MPI.Wtime()        
        
        cont=0
        cont2=0
        while numWorkers>0:            
            auxInds=[]
            auxAsigs=[]
            for i in range(1,numWorkers+1):                
                ind=comm.recv(source=i)
                asig=comm.recv(source=i)
                asignacionProbar[indices[i-1]]=asig                
                indices[i-1]+=1

                auxInds.append(ind)
                auxAsigs.append(asig)
            
            # Continuan?
            tmp=0
            for i in range(1,numWorkers+1):
                data=comm.recv(source=i)
                if data==False:
                    tmp+=1
                else: 
                    comm.send(auxInds,dest=i)
                    comm.send(auxAsigs,dest=i)
            
            if cont2<len(procesar) and cont>=procesar[cont2]:
                totalTimeEnd = MPI.Wtime()

                cont2+=1

                print("(k={}) Euclidea_NoAct:\t\t{}".format(k,totalTimeEnd-totalTimeStart))           
        
                ruta=os.path.join(ruta_Act,'KNN_2MPI{}_Act_k{}_E.txt'.format(numWorkers,k))  
                with open(ruta, 'a') as archivo:
                    # Escribir un número flotante en el archivo                                
                    archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')
                    
            
            cont+=numWorkers
            numWorkers-=tmp   
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
            
            comm.send(poblacionProbar[x],dest=MASTER)
            comm.send(ret,dest=MASTER)

            if x!=m-1:
                comm.send(True,dest=MASTER)
                indsTmp=comm.recv(source=MASTER)
                asigsTmp=comm.recv(source=MASTER)
                for ind in indsTmp:
                    poblacionIni.append(ind)
                for asig in asigsTmp:
                    asignacionIni.append(asig)
            else: comm.send(False,dest=MASTER)           
            
            poblacionIni.append(poblacionProbar[x])
            asignacionIni.append(ret)
            n+=1+numWorkers
    
        
      
        
        
def ejecuta_Act_M(comm, myrank, numWorkers, 
             n, m, d, clusters, poblacionIni, asignacionIni, poblacionProbar, k):  

    MASTER=0
    END_OF_PROCESSING=-2
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
            auxInds=[]
            auxAsigs=[]
            for i in range(1,numWorkers+1):                
                ind=comm.recv(source=i)
                asig=comm.recv(source=i)
                asignacionProbar[indices[i-1]]=asig                
                indices[i-1]+=1

                auxInds.append(ind)
                auxAsigs.append(asig)
            
            # Continuan?
            tmp=0
            for i in range(1,numWorkers+1):
                data=comm.recv(source=i)
                if data==False:
                    tmp+=1
                else: 
                    comm.send(auxInds,dest=i)
                    comm.send(auxAsigs,dest=i)
            
            numWorkers-=tmp   
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
                    distancia+=abs(poblacionIni[i][j]-poblacionProbar[x][j])  
                
                
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
            
            comm.send(poblacionProbar[x],dest=MASTER)
            comm.send(ret,dest=MASTER)

            if x!=m-1:
                comm.send(True,dest=MASTER)
                indsTmp=comm.recv(source=MASTER)
                asigsTmp=comm.recv(source=MASTER)
                for ind in indsTmp:
                    poblacionIni.append(ind)
                for asig in asigsTmp:
                    asignacionIni.append(asig)
            else: comm.send(False,dest=MASTER)           
            
            poblacionIni.append(poblacionProbar[x])
            asignacionIni.append(ret)
            n+=1+numWorkers
    
       
        
def ejecuta_NoAct_E(comm, myrank, numWorkers, 
             n, m, d, clusters, poblacionIni, asignacionIni, poblacionProbar, k):
    MASTER=0
    END_OF_PROCESSING=-2

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
        
       
          
def ejecuta_NoAct_M(comm, myrank, numWorkers, 
             n, m, d, clusters, poblacionIni, asignacionIni, poblacionProbar, k):
    MASTER=0
    END_OF_PROCESSING=-2

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
                    distancia+=abs(poblacionIni[i][j]-poblacionProbar[x][j])   
                  
                
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
       
        




main()