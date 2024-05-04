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
        poblacion=lee("100000_2D")
        
         

        datosTXT=[]
        tamDatos=[]         
        
        #n=len(poblacion)        # Tamaño
        d=len(poblacion[0])     # Numero de dimensiones
        #numsK=[3,5,10,15]                     # Numero de cluster
        numsK=[10]
        cent=[[-0.12293300848913269, 8.197940858866115], [9.947053218490957, -0.6975674085386796], [9.591533658594035, -7.407552627543687], [3.7079497249547195, -8.792991586408998], [0.4522664959026699, 6.0981500948027865], [-4.868512907161257, -0.16920748146691977], [-8.199029435615495, 5.179308090342815], [9.922457533335596, -0.497719340882842], [0.5151398954729185, -4.2703198155086275], [3.702589770726254, -3.3200049788824977], [0.5912719290614117, 4.955550264440161], [6.04775453370749, 0.9769190296446162], [8.464188413408685, -3.7927519994207826], [-7.844739643806415, 2.7871471490160804], [0.4227486922140038, -0.052929778805147265], [5.280102567353076, 8.882908143762695], [-0.819485831742746, 5.588877476672495], [-3.000409968481179, -4.522314880691127], [2.748080733683093, 4.108514983968931], [6.518364569672681, -9.246791075220395]]
        
        """dic={}
        centroides=[]
        for i in range(k):
            while True:
                rand = random.randint(0, n-1)
                if rand not in dic:
                    centroides.append(poblacion[rand])                
                    dic[rand] = 1
                    break """       
    
    numsK=comm.bcast(numsK, root=MASTER)
    # Envia el numero de dimensiones a los workers
    d=comm.bcast(d, root=MASTER)
    # Envia los centroides iniciales 
    
    ruta_pruebas = os.path.dirname(os.path.abspath(__file__))
    
    
    procesar=[40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]

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
            # --- MANHATTAN -------------------------------------------------------------
            # ---------------------------------------------------------------------------
            timeStart = MPI.Wtime()

            ejecutaM(comm,myrank, numWorkers,tag,status,
                     n,d,k,centroides,poblacion)                     
        
            timeEnd = MPI.Wtime()            
            
            if myrank==MASTER:
                ruta=os.path.join(ruta_pruebas,'KMedias{}M_MPI{}.txt'.format(k,numWorkers))    
                with open(ruta, 'a') as archivo:                               
                    archivo.write(str(timeEnd-timeStart) + ', ')

            # ---------------------------------------------------------------------------
            # --- EUCLIDEA --------------------------------------------------------------
            # ---------------------------------------------------------------------------

            timeStart = MPI.Wtime()

            ejecutaE(comm,myrank, numWorkers,tag,status,
                     n,d,k,centroides,poblacion)                     
        
            timeEnd = MPI.Wtime()            
            
            if myrank==MASTER:
                ruta=os.path.join(ruta_pruebas,'KMedias{}E_MPI{}.txt'.format(k,numWorkers))    
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
            ruta=os.path.join(ruta_pruebas,'KMedias{}E_MPI{}_Iteraciones.txt'.format(k,numWorkers))  
            with open(ruta, 'a') as archivo:                              
                archivo.write(str(vueltas) + ', ')        

        comm.recv(source=MASTER)
                

def ejecutaM(comm, myrank, numWorkers,tag,status,
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
                datos = comm.recv(source=w)
                """datos = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
                source_rank=status.Get_source() """
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
            centroidesMaster=comm.recv(source=0)
            if centroidesMaster==END_OF_PROCESSING:                        
                comm.send(asignacion, dest=0)
                break
            centroides=centroidesMaster

        if myrank==1:
            ruta=os.path.join(ruta_pruebas,'KMedias{}M_MPI{}_Iteraciones.txt'.format(k,numWorkers))  
            with open(ruta, 'a') as archivo:                              
                archivo.write(str(vueltas) + ', ')        

        comm.recv(source=MASTER)


               

            
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
 



main()

