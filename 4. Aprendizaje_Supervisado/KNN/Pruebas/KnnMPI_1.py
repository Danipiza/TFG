import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import os
import math

import queue

# mpiexec -np 5 python KnnMPI_1.py
"""
SE DIVIDEN LA POBLACION INICIAL PARA QUE CADA WORKER COMPARE LOS K VECINOS MAS CERCANOS DE SU POBLACION
SE LO MANDE AL MASTER Y ESTE CALCULE LA ASIGNACION


ERROR, 
COMO SE DIVIDE LA POBLACION INICIAL, NO SE PUEDE PONER K=100 VECINOS CON MAS DE 10 WORKERS PORQUE, ASI CADA WORKER
TIENE MENOS POBLACION INICIAL QUE LOS 100 VECINOS MAS CERCANOS Y DA FALLO DE COLA DE PRIORIDAD
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
        ruta_Tam=os.path.join(directorio_script, 'Tam_Datos1V2MPI{}.txt'.format(numWorkers))

        d=len(poblacionIni[0])
    
    

    clusters=4
    procesar=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]
    #procesar_k=[2,4,6,8,10,15,20,30,50]#,100]  
    procesar_k=[10]  
    #if numWorkers<=10: procesar_k.append(100)


    poblacionIni=comm.bcast(poblacionIni, root=MASTER)
    asignacionIni=comm.bcast(asignacionIni, root=MASTER)
    #m=comm.bcast(m, root=MASTER)
    d=comm.bcast(d, root=MASTER)    
    # Poblacion 
    poblacionProbar=comm.bcast(poblacionProbar, root=MASTER)

    for x in procesar:
        ini=[]
        iniAsig=[]
        for y in poblacionIni:
            ini.append(y)
        for y in asignacionIni:
            iniAsig.append(y)

        
        for k in procesar_k:
            """# ---------------------------------------------------------------------------
            # --- MANHATTAN -------------------------------------------------------------
            # ---------------------------------------------------------------------------
            totalTimeStart = MPI.Wtime()
            
            ejecuta_NoAct_M(comm,myrank, numWorkers, 
                     n, x, d, clusters, ini, iniAsig, poblacionProbar[0:x], k)
            totalTimeEnd = MPI.Wtime()

            
            if myrank==MASTER:  
                
                ruta=os.path.join(ruta_NoAct,'KNN_1MPI{}_NoAct_k{}_M.txt'.format(numWorkers,k)) 
                with open(ruta, 'a') as archivo:                               
                    archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')


            # ---------------------------------------------------------------------------
            # --- EUCLIDEA --------------------------------------------------------------
            # ---------------------------------------------------------------------------

            totalTimeStart = MPI.Wtime()
            
            ejecuta_NoAct_E(comm,myrank, numWorkers, 
                     n, x, d, clusters, ini, iniAsig, poblacionProbar[0:x], k)
            totalTimeEnd = MPI.Wtime()

            
            if myrank==MASTER:            
                
                ruta=os.path.join(ruta_NoAct,'KNN_1MPI{}_NoAct_k{}_E.txt'.format(numWorkers,k)) 
                with open(ruta, 'a') as archivo:                              
                    archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')"""


            # --- ACTUALIZA -------------------------------------------------------------

            # ---------------------------------------------------------------------------
            # --- MANHATTAN -------------------------------------------------------------
            # ---------------------------------------------------------------------------
            totalTimeStart = MPI.Wtime()
            
            ejecuta_Act_M(comm,myrank, numWorkers, 
                     n, x, d, clusters, ini, iniAsig, poblacionProbar[0:x], k)
            totalTimeEnd = MPI.Wtime()

            
            if myrank==MASTER:    
                
                ruta=os.path.join(ruta_Act,'KNN_1V2MPI{}_Act_k{}_M.txt'.format(numWorkers,k))  
                with open(ruta, 'a') as archivo:                                
                    archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')


            # ---------------------------------------------------------------------------
            # --- EUCLIDEA --------------------------------------------------------------
            # ---------------------------------------------------------------------------

            totalTimeStart = MPI.Wtime()
            
            ejecuta_Act_E(comm,myrank, numWorkers, 
                     n, x, d, clusters, ini, iniAsig, poblacionProbar[0:x], k)
            totalTimeEnd = MPI.Wtime()

            
            if myrank==MASTER:          
                
                ruta=os.path.join(ruta_Act,'KNN_1V2MPI{}_Act_k{}_E.txt'.format(numWorkers,k))  
                with open(ruta, 'a') as archivo:                              
                    archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')

        if myrank==MASTER:
            with open(ruta_Tam, 'a') as archivo:                               
                archivo.write(str(x) + ', ')

def ejecuta_Act_E(comm, myrank, numWorkers, 
             n, m, d, clusters, poblacionIni, asignacionIni, poblacionProbar, k):  

    MASTER=0
    END_OF_PROCESSING=-2
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

        for i in range(1,numWorkers+1):
            comm.send(None,dest=i)
        
        individuo=1
        while cont<m:
            
            pq=MaxPriorityQueue()

            for i in range(1,numWorkers+1):
                dist=comm.recv(source=i)
                etiqs=comm.recv(source=i)
                for j in range(k):
                    if pq.size()<k: pq.push(etiqs[j],dist[j])     
                    elif pq.top_distancia()>dist[j]:      
                        pq.pop()
                        pq.push(etiqs[j],dist[j])

            # Cuenta el numero de vecinos mas cercanos para cada cluster
            etiquetas=[0 for i in range(clusters)]    
            for i in range(k):
                tmp=pq.pop()                
                etiquetas[tmp]+=1
            # Coge el que mas tenga
            ret=0
            cantidad=etiquetas[0]
            for i in range(1,clusters):
                if cantidad<etiquetas[i]:
                    cantidad=etiquetas[i]
                    ret=i  
                            
            asignacionProbar.append(ret)

            for i in range(1,numWorkers+1):
                if i==individuo: comm.send(ret,dest=i)            
                else: comm.send(None,dest=i)

                        
            
            individuo+=1
            if individuo>numWorkers: individuo=1            
                    
            
            cont+=1

        """for i in range(1,numWorkers+1):
            comm.send(1000000000,dest=i)"""

            

    else : # WORKER        
        poblacionIni=comm.recv(source=MASTER)
        asignacionIni=comm.recv(source=MASTER)
        

        #print(poblacionIni)
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
            
            a=comm.recv(source=MASTER)
            if a!=None:
                poblacionIni.append(poblacionProbar[x-1])
                asignacionIni.append(a)
                n+=1

                distancia=0
                for j in range(d):
                    distancia+=(poblacionIni[-1][j]-poblacionProbar[x][j])**2    
                distancia=math.sqrt(distancia)            
                
                # Si la cola de prioridad no es k, añadir la distancia
                if pq.size()<k: pq.push(asignacionIni[-1],distancia)
                # Si distancia actual es menor a la mayor menor, 
                # se elimina la mayor e introduce la actual        
                elif pq.top_distancia()>distancia:            
                    pq.pop()
                    pq.push(asignacionIni[-1],distancia)
            
            dists=[]
            etiq=[]
            for _ in range(k):
                dists.append(pq.top_distancia())
                etiq.append(pq.top_etiqueta())
                pq.pop()

            """print("(WORKER {}) dists={}, etiqs={}".format(myrank, dists, etiq))"""
            comm.send(dists,dest=MASTER)
            comm.send(etiq,dest=MASTER)

        comm.recv(source=MASTER)
    
        
        
def ejecuta_Act_M(comm, myrank, numWorkers, 
             n, m, d, clusters, poblacionIni, asignacionIni, poblacionProbar, k):  

    MASTER=0
    END_OF_PROCESSING=-2
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

        for i in range(1,numWorkers+1):
            comm.send(None,dest=i)
        
        individuo=1
        while cont<m:
            
            pq=MaxPriorityQueue()

            for i in range(1,numWorkers+1):
                dist=comm.recv(source=i)
                etiqs=comm.recv(source=i)
                for j in range(k):
                    if pq.size()<k: pq.push(etiqs[j],dist[j])     
                    elif pq.top_distancia()>dist[j]:      
                        pq.pop()
                        pq.push(etiqs[j],dist[j])

            # Cuenta el numero de vecinos mas cercanos para cada cluster
            etiquetas=[0 for i in range(clusters)]    
            for i in range(k):
                tmp=pq.pop()                
                etiquetas[tmp]+=1
            # Coge el que mas tenga
            ret=0
            cantidad=etiquetas[0]
            for i in range(1,clusters):
                if cantidad<etiquetas[i]:
                    cantidad=etiquetas[i]
                    ret=i  
                            
            asignacionProbar.append(ret)

            for i in range(1,numWorkers+1):
                if i==individuo: comm.send(ret,dest=i)            
                else: comm.send(None,dest=i)

                        
            
            individuo+=1
            if individuo>numWorkers: individuo=1            
                    
            
            cont+=1

        """for i in range(1,numWorkers+1):
            comm.send(1000000000,dest=i)"""

            

    else : # WORKER        
        poblacionIni=comm.recv(source=MASTER)
        asignacionIni=comm.recv(source=MASTER)
        

        #print(poblacionIni)
        n=len(poblacionIni)
        
        for x in range(m):  
            pq = MaxPriorityQueue()   

            

            

            
            
            # Calcula todas las distancias y coge las k mas cercanas
            for i in range(n):
                distancia=0
                for j in range(d):
                    distancia+=abs(poblacionIni[i][j]-poblacionProbar[x][j]) 
                distancia=distancia
                
                # Si la cola de prioridad no es k, añadir la distancia
                if pq.size()<k: pq.push(asignacionIni[i],distancia)
                # Si distancia actual es menor a la mayor menor, 
                # se elimina la mayor e introduce la actual        
                elif pq.top_distancia()>distancia:            
                    pq.pop()
                    pq.push(asignacionIni[i],distancia)
            
            a=comm.recv(source=MASTER)
            if a!=None:
                poblacionIni.append(poblacionProbar[x-1])
                asignacionIni.append(a)
                n+=1

                distancia=0
                for j in range(d):
                    distancia+=abs(poblacionIni[-1][j]-poblacionProbar[x][j])  
                distancia=distancia           
                
                # Si la cola de prioridad no es k, añadir la distancia
                if pq.size()<k: pq.push(asignacionIni[-1],distancia)
                # Si distancia actual es menor a la mayor menor, 
                # se elimina la mayor e introduce la actual        
                elif pq.top_distancia()>distancia:            
                    pq.pop()
                    pq.push(asignacionIni[-1],distancia)
            
            dists=[]
            etiq=[]
            for _ in range(k):
                dists.append(pq.top_distancia())
                etiq.append(pq.top_etiqueta())
                pq.pop()

            """print("(WORKER {}) dists={}, etiqs={}".format(myrank, dists, etiq))"""
            comm.send(dists,dest=MASTER)
            comm.send(etiq,dest=MASTER)

        comm.recv(source=MASTER)
    
        
def ejecuta_NoAct_E(comm, myrank, numWorkers, 
             n, m, d, clusters, poblacionIni, asignacionIni, poblacionProbar, k):
    MASTER=0
    END_OF_PROCESSING=-2

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

            comm.send(dists,dest=MASTER)
            comm.send(etiq,dest=MASTER)

          
def ejecuta_NoAct_M(comm, myrank, numWorkers, 
             n, m, d, clusters, poblacionIni, asignacionIni, poblacionProbar, k):
    MASTER=0
    END_OF_PROCESSING=-2

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
                    distancia+=abs(poblacionIni[i][j]-poblacionProbar[x][j])
                          
                
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

            comm.send(dists,dest=MASTER)
            comm.send(etiq,dest=MASTER)
        
        




main()