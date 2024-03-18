from mpi4py import MPI
import random
import os
import math


# COMPILAR
# mpiexec -np 5 python MPI.py


    
    

def main():      
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    # DATOS A COMPARTIR
    poblacion=[]
    n=0
    k=0
    d=0
    asignacion=[]
    centroides=[]

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
    #if myrank==0: print("Master: tiene {} workers".format(numWorkers))



    # TODO PARALELIZAR
    # 1. Dividir toda la poblacion y repartir entre los workers
    # 2. Repartir partes de la poblacion para que vayan procesando y enviando


    # Inicializa centros
    if myrank==MASTER:                 
        a,n=leeArchivo("10000")      
        poblacion=[[x] for x in a]  
        #poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0], [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]
        n=len(poblacion)        # Tamaño
        d=len(poblacion[0])     # Numero de dimensiones
        k=3                     # Numero de cluster

        dic={}
        centroides=[]
        for i in range(k):
            while True:
                rand = random.randint(0, n-1)
                if rand not in dic:
                    centroides.append(poblacion[rand])                
                    dic[rand] = 1
                    break
        #print("Centroides:", centroides)
    
    # Envia el numero de clusters a los workers
    k=comm.bcast(k, root=MASTER)
    # Envia el numero de dimensiones a los workers
    d=comm.bcast(d, root=MASTER)
    # Envia los centroides iniciales 
    centroides=comm.bcast(centroides, root=MASTER)
    
    timeStart = MPI.Wtime()

    if myrank==MASTER:       
        
        # ENVIA LA PARTE DE LA POBLACION QUE CADA worker ----------------------- 
        #   VA A PROCESAR EN TODA LA EJECUCION ---------------------------------
        # Numero de elementos para cada worker       
        tamProc=n//numWorkers
        # Si mcd(n,numWorkers)!=numWorkers, 
        #   es porque habra algunos workers con 1 elemento mas
        modulo=n%numWorkers
        # Punteros
        izq=0
        der=tamProc+1

        # Hay al menos 1 elemento para cada worker.
        if tamProc>=1:  
            for i in range(1, modulo+1):    
                comm.send(poblacion[izq:der],dest=i)
                # update
                izq+=tamProc+1
                der+=tamProc+1
            der-=1
            # Hay algun worker con 1 elemento menos que los demas.
            for i in range(modulo+1,numWorkers+1):
                comm.send(poblacion[izq:der],dest=i)
                # update
                izq+=tamProc
                der+=tamProc    
        # No hay al menos 1 elemento para cada worker
        #   los workers que se queden sin elemento se finalizan.
        else:
            for i in range(1, modulo+1):  
                comm.send(poblacion[izq], dest=i)   
                # update
                izq+=1							
            for i in range(modulo+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                  
            # Se reduce el numero de workers
            numWorkers-=numWorkers-modulo
        
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
                   
                

        # Procesa datos, termina cuando los centros no cambian
        while True:
            centroidesNuevos=[[0 for _ in range(d)] for _ in range(k)]
            indsCluster=[0 for _ in range(k)]

            for _ in range(numWorkers):
                datos = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
                source_rank=status.Get_source() 
                # Suma los centroides
                for i in range(k):
                    for j in range(d):
                        centroidesNuevos[i][j]+=datos[i][j]
                # Suma los indices
                datos = comm.recv(source=source_rank, tag=tag,status=status)
                for i in range(k):
                    indsCluster[i]+=datos[i]                     
                        
            # Calcula los nuevos clusters            
            for i in range(k): 
                for j in range(d):              
                    centroidesNuevos[i][j]/=indsCluster[i]
            #print("\n\n, centroidesNuevos=",centroidesNuevos)
            
            # FINALIZA
            if(compara_centros(d, centroides,centroidesNuevos)): 
                for i in range(1,numWorkers+1):
                    comm.send(END_OF_PROCESSING,dest=i)
                asignacion=[]
                for i in range(1,numWorkers+1):
                    datos = comm.recv(source=i)
                    for x in datos:
                        asignacion.append(x)

                break

            # CONTINUA: Envia los nuevos centroides 
            for i in range(1,numWorkers+1):
                comm.send(centroidesNuevos,dest=i)
            centroides=centroidesNuevos
            
                
        timeEnd = MPI.Wtime()
        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
        #print(asignacion)
    
    else : # WORKER
        #print("WORKER {}, ha recibido con BCast: k={}, d={}, centroides={}".format(myrank,k,d,centroides))
        poblacion=comm.recv(source=0)
        #print("WORKER: {}, recibe {}".format(myrank,poblacion))
        if poblacion==-2: exit(0)
        n=len(poblacion)
        while True:
            # POBLACION NO CAMBIA, CUANDO TODOS LOS workers ENVIEN UN MENSAJE AL
            #   master DICIENDO QUE LOS CENTROIDES NO HAN CAMBIADO, EL master ENVIA
            #   UN MENSAJE PARA QUE LOS workers DEVUELVAN LA ASIGNACION FINAL

            # FASE DE ASIGNACION            
            asignacion=[]
            for i in range(n):
                tmp=-1
                cluster=-1
                dist=float('inf')
                for j in range(k):                    
                    tmp=0.0      
                    for a in range(d):
                        tmp+=abs(poblacion[i][a]-centroides[j][a])     
                    tmp=math.sqrt(tmp)
                    
                    if dist>tmp:
                        dist=tmp
                        cluster=j
                asignacion.append(cluster)
            #print("WORKER {}: asignacion={}".format(myrank, asignacion))

            # ACTUALIZAN CENTROS
            indsCluster=[0 for _ in range(k)]
            centroidesNuevos=[[0 for _ in range(d)] for _ in range(k)]
            for i in range(n):
                for j in range(d):
                    centroidesNuevos[asignacion[i]][j]+=poblacion[i][j]
                indsCluster[asignacion[i]]+=1
            #print("WORKER {}: centroidesNuevos={}, indsCluster={}".format(myrank, centroidesNuevos,indsCluster))
            comm.send(centroidesNuevos, dest=0)
            comm.send(indsCluster, dest=0)
            
            # Reciben los nuevos centroides            
            centroides=comm.recv(source=0)
            #print("WORKER {}: centroides={}".format(myrank, centroides))
            if centroides==END_OF_PROCESSING:
                # TODO ENVIA
                comm.send(asignacion, dest=0)
                exit(0)

                

            
            

    
    

    
def compara_centros(d, a, b):
    n=len(a)
    for i in range(n):
        for j in range(d):
            if a[i][j]!=b[i][j]: return False
    
    return True

# Manhattan
def manhattan(self,a,b):
    ret=0.0
    for i in range(len(a)):
        ret+=abs(a[i]-b[i])
    return ret

def euclidea(self, a,b):
    ret=0.0
    for i in range(len(a)):
        ret+=(a[i]-b[i])**2        
    
    return math.sqrt(ret)


def leeArchivo(archivo):
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    tfg_directorio=os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))
    
    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(tfg_directorio, ".Otros","ficheros","No_Ordenado", archivo+".txt")
       
    tam=0    
    array = [] 
    try:        
        with open(path, 'r') as archivo: # modo lectura
            for linea in archivo: # Solo hay una linea                
                numeros_en_linea = linea.split() # Divide por espacios                               
                for numero in numeros_en_linea:
                    array.append(int(numero))
                    tam+=1
    
    except FileNotFoundError:
        print("El archivo '{}' no existe.".format(archivo+".txt"))
    
    return array, tam



#for i in range(10):
main()

"""for k in range(1,19):
   
    ret=0
    timeStart=MPI.Wtime()
    for i in range(100):
        asignacion=kM.ejecuta()
        maxC=[(-float('inf')) for _ in range(k)]
        minC=[(float('inf')) for _ in range(k)]
        for j in range(n):
            if maxC[asignacion[j]]<poblacion[j]: maxC[asignacion[j]]=poblacion[j]
            if minC[asignacion[j]]>poblacion[j]: minC[asignacion[j]]=poblacion[j]
        tmp=0
        for j in range(k):
            tmp+=maxC[j]-minC[j]
        if ret<tmp: ret=tmp

    timeEnd=MPI.Wtime()
        
    print("Tiempo de ejecucion:",(timeEnd-timeStart))
    print("Mejor Resultado:",ret)"""

