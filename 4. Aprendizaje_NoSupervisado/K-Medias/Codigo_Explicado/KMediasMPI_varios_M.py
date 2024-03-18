from mpi4py import MPI
import random
import os
import math

# COMPILAR
# mpiexec -np 5 python KMediasMPI.py

# PARALELIZAR
    # 1. Dividir toda la poblacion y repartir entre los workers.
    # 2. Repartir partes de la poblacion para que vayan procesando y enviando.      

# Despues de implementar la 1ra idea, me he dado cuenta que es mas optimo
    # dividir la poblacion entre los workers. Ya que esta poblacion no cambia,
    # solo cambia la asignacion y los centros de los clustersm

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

    if myrank==MASTER:                 
        a,n=leeArchivo("100000")      
        poblacion=[[x] for x in a] 
        #n=12
        #poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0], [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]         
        
        n=len(poblacion)        # Tamaño
        d=len(poblacion[0])     # Numero de dimensiones
        k=10                     # Numero de cluster

    # Envia el numero de clusters a los workers
    k=comm.bcast(k, root=MASTER)
    # Envia el numero de dimensiones a los workers
    d=comm.bcast(d, root=MASTER)
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
    else :        
        poblacion=comm.recv(source=0)        
        if poblacion==-2: 
            print("WORKER {}: finaliza".format(myrank))
            exit(0)
        n=len(poblacion)
     

    timeStart = MPI.Wtime()
    
    for times in range(5):
        # Inicializa centros
        if myrank==MASTER:  
            dic={}
            centroides=[]
            for i in range(k):
                while True:
                    rand = random.randint(0, n-1)
                    if rand not in dic:
                        centroides.append(poblacion[rand])                
                        dic[rand] = 1
                        break
        
        # Envia los centroides iniciales 
        centroides=comm.bcast(centroides, root=MASTER)               
        
        
        if myrank==MASTER:
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
                        
            #print(asignacion)
        else : # WORKER                       
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
                        
                        if dist>tmp:
                            dist=tmp
                            cluster=j
                    asignacion.append(cluster)

                # ACTUALIZAN CENTROS
                indsCluster=[0 for _ in range(k)]
                centroidesNuevos=[[0 for _ in range(d)] for _ in range(k)]
                for i in range(n):
                    for j in range(d):
                        centroidesNuevos[asignacion[i]][j]+=poblacion[i][j]
                    indsCluster[asignacion[i]]+=1
                comm.send(centroidesNuevos, dest=0)
                comm.send(indsCluster, dest=0)
                
                # Reciben los nuevos centroides            
                centroides=comm.recv(source=0)
                if centroides==END_OF_PROCESSING:
                    comm.send(asignacion, dest=0)
                    #exit(0)
                    break
    
    timeEnd = MPI.Wtime()
    if myrank==MASTER:
        for i in range(1, numWorkers+1):
            comm.send(END_OF_PROCESSING, dest=i)  
        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
    
    

    
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
    
    tfg_directorio=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))
    
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



main()

