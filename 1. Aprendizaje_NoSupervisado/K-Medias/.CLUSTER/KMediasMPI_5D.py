from mpi4py import MPI
import random
import os
import math

# EJECUTAR
# mpiexec -np 5 python KMediasMPI.py

def main():      
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    # DATOS A COMPARTIR
    poblacion=[]
    n=0    
    d=0
    asignacion=[]
    centroides=[]
    numsK=[]

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
  

    # Inicializa centros
    if myrank==MASTER:          
        poblacion=lee("250000_5D",5)       
                
        
        d=len(poblacion[0])    

        numsK=[50]        
        cent=poblacion[0:50]        
        
    
    numsK=comm.bcast(numsK, root=MASTER)
    # Envia el numero de dimensiones a los workers
    d=comm.bcast(d, root=MASTER)
    # Envia los centroides iniciales 
    
    ruta_pruebas = os.path.dirname(os.path.abspath(__file__))
    
    
    procesar=[20000* i for i in range(1,13)]

    for k in numsK:
        for x in procesar:

            if myrank==MASTER:
                centroides=[cent[i] for i in range(k)]
                for i in range(1,numWorkers+1):
                    comm.send(centroides,dest=i)            
            else:
                centroides=comm.recv(source=MASTER)
            
            n=x

            # ---------------------------------------------------------------------------
            # --- EUCLIDEA --------------------------------------------------------------
            # ---------------------------------------------------------------------------

            timeStart = MPI.Wtime()

            ejecutaE(comm,myrank, numWorkers,tag,status,
                     n,d,k,centroides,poblacion)                     
        
            timeEnd = MPI.Wtime()            
            
            if myrank==MASTER:
                ruta=os.path.join(ruta_pruebas,'KMedias{}E5D_MPI{}.txt'.format(k,numWorkers))    
                with open(ruta, 'a') as archivo:                               
                    archivo.write(str(timeEnd-timeStart) + ', ')

                ruta=os.path.join(ruta_pruebas,'TamDatos{}_MPI{}.txt'.format(k,numWorkers))    
                with open(ruta, 'a') as archivo:                               
                    archivo.write(str(n) + ', ')

                

            


def ejecutaE(comm, myrank, numWorkers,tag,status,
             n, d, k,centroides,poblacion):
    MASTER=0
    END_OF_PROCESSING=-2
    ruta_pruebas = os.path.dirname(os.path.abspath(__file__))

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

            for w in range(1,numWorkers+1):
                """datos = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
                source_rank=status.Get_source()""" 
                datos = comm.recv(source=w)
                
                # Suma los centroides
                for i in range(k):
                    for j in range(d):
                        centroidesNuevos[i][j]+=datos[i][j]
                # Suma los indices
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
            
        

        for i in range(1,numWorkers+1):
            comm.send(0,dest=i)

                  
    else : # WORKER
        poblacion=comm.recv(source=0)
        if poblacion==-2: exit(0)
        n=len(poblacion)
        vueltas=0
        while True:
            vueltas+=1
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
                        tmp+=(poblacion[i][a]-centroides[j][a])**2    
                    tmp=math.sqrt(tmp)
                    
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
            centroidesMaster=comm.recv(source=0)
            if centroidesMaster==END_OF_PROCESSING:                        
                comm.send(asignacion, dest=0)
                break
            centroides=centroidesMaster

        if myrank==1:
            ruta=os.path.join(ruta_pruebas,'KMedias{}E5D_MPI{}_Iteraciones.txt'.format(k,numWorkers))  
            with open(ruta, 'a') as archivo:                              
                archivo.write(str(vueltas) + ', ')        

        comm.recv(source=MASTER)
                
            

            
def compara_centros(d, a, b):
    n=len(a)
    for i in range(n):
        for j in range(d):
            if a[i][j]!=b[i][j]: return False
    
    return True



def lee(archivo, d):

    dir=os.getcwd()
       
    path=os.path.join(dir, archivo+".txt")
    
    with open(path, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')      
    for i in range(0, len(datos), d):
        ind=[]
        for j in range(d):
            ind.append(float(datos[i+j]))
        #y = float(datos[i + 1])

        array.append(ind)

    #print("\n",array)        
    
    return array
 



main()

