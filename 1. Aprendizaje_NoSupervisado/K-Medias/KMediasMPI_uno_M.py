from mpi4py import MPI
import random
import os
import math

# EJECUTAR
# mpiexec -np 5 python KMediasMPI_uno_M.py

# TIEMPO: (datos=100000.txt, k=3)
# Tiempo de ejecucion: 0.3559337999904528

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


    # Inicializa centros
    if myrank==MASTER:                 
        #a,n=leeArchivo("6000")      
        #poblacion=[[x] for x in a] 
        poblacion=lee("100_2D")          
        
        n=len(poblacion)        # Tamaño
        d=len(poblacion[0])     # Numero de dimensiones
        k=10                     # Numero de cluster

        dic={}
        """centroides=[]
        for i in range(k):
            while True:
                rand = random.randint(0, n-1)
                if rand not in dic:
                    centroides.append(poblacion[rand])                
                    dic[rand] = 1
                    break  """     
        cent=[[-0.12293300848913269, 8.197940858866115], [9.947053218490957, -0.6975674085386796], [9.591533658594035, -7.407552627543687], [3.7079497249547195, -8.792991586408998], [0.4522664959026699, 6.0981500948027865], [-4.868512907161257, -0.16920748146691977], [-8.199029435615495, 5.179308090342815], [9.922457533335596, -0.497719340882842], [0.5151398954729185, -4.2703198155086275], [3.702589770726254, -3.3200049788824977], [0.5912719290614117, 4.955550264440161], [6.04775453370749, 0.9769190296446162], [8.464188413408685, -3.7927519994207826], [-7.844739643806415, 2.7871471490160804], [0.4227486922140038, -0.052929778805147265], [5.280102567353076, 8.882908143762695], [-0.819485831742746, 5.588877476672495], [-3.000409968481179, -4.522314880691127], [2.748080733683093, 4.108514983968931], [6.518364569672681, -9.246791075220395]]
        centroides=[]
        for i in range(k):
            centroides.append(cent[i]) 
    
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
                   
                
        vueltas=0
        # Procesa datos, termina cuando los centros no cambian
        while True:
            vueltas+=1
            centroidesNuevos=[[0 for _ in range(d)] for _ in range(k)]
            indsCluster=[0 for _ in range(k)]

            for w in range(1,numWorkers+1):
                """datos = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
                source_rank=status.Get_source() """
                datos = comm.recv(source=w)
                
                # Suma los centroides
                for i in range(k):
                    for j in range(d):
                        centroidesNuevos[i][j]+=datos[i][j]
                # Suma los indices
                """datos = comm.recv(source=source_rank, tag=tag,status=status)"""
                datos = comm.recv(source=w)
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
            
        print(vueltas)
        timeEnd = MPI.Wtime()
        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
        #print(asignacion)
    
    else : # WORKER
        poblacion=comm.recv(source=0)
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
                exit(0)

    
def compara_centros(d, a, b):
    n=len(a)
    for i in range(n):
        for j in range(d):
            if a[i][j]!=b[i][j]: return False
    
    return True



def lee(archivo):

    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","2.Cluster", archivo+".txt")

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

