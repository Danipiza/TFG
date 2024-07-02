from mpi4py import MPI
import sys
import os

# COMPILAR
# mpiexec -np 5 python NormalizacionMPI.py

"""
1. Normal
2. Envia a la mitad de los min 
3. Calculo de minimos en escalera
    n=len(poblacion)
    worker n        n/2
    worker n-1      n/2**2
    worker n-2      n/2**3
    ...
    worker 1        n/2*numWorkers
"""

def normalizar_dato(val,m,M):
    return (val-m)/(M-m)


def lee(archivo, d):
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".Otros","ficheros","RedNeu", archivo+".txt")

    with open(path, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')  
        
    for i in range(0, len(datos), d):
        ind=[]
        for a in range(d):
            ind.append(float(datos[i+a]))
        
        """altura=float(datos[i])
        peso=float(datos[i+1])
        IMC=float(datos[i+2])"""

        """array.append([altura,peso,IMC])"""
        array.append(ind)

    #print("\n",array)        
    
    return array

def main1(archivo):  	
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    poblacion=[]
    n=0           		    

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
   		
    # Master lee el archivo .txt con el array de entrada.
    # Tambien hace al aproximacion del numero de workers a la potencia.
    if myrank==MASTER: 
        print("\nEjecutando la primera forma...")
        #poblacion=lee("datos80")   
        #poblacion=lee("datos2042S")  
        poblacion=lee(archivo,10)   
               
        n=len(poblacion)
        d=len(poblacion[0])
        print("Tam. Poblacion: {}\t Num. Variables: {}\n".format(n,d))

    # Comienza el timer, una vez inicializado todo
    timeStart = MPI.Wtime()
    
    if myrank==MASTER:        
        # Numero de elementos que cada proceso va a procesar inicialmente
        tamProc=n//numWorkers
        # Si mcd(n,numWorkers)!=numWorkers, es porque habra algunos workers con 1 elemento mas
        modulo=n%numWorkers
        # Punteros
        izq=0
        workers=[]

        # Hay al menos 1 elemento para cada worker.
        if tamProc>=1:  
            for i in range(1, modulo+1):                
                comm.send(poblacion[izq:izq+tamProc+1],dest=i)
                workers.append(izq)
                # update
                izq+=tamProc+1
            # Hay algun worker con 1 elemento menos que los demas.
            for i in range(modulo+1,numWorkers+1):
                comm.send(poblacion[izq:izq+tamProc],dest=i)
                workers.append(izq)
                # update
                izq+=tamProc  
        # No hay al menos 1 elemento para cada worker, los workers que se queden sin elemento se finalizan.
        else:
            for i in range(1, modulo+1):   
                comm.send(a[izq], dest=i) 
                workers.append(izq)  
                # update
                izq+=1							
            for i in range(modulo+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                  
            # Se reduce el numero de workers
            numWorkers-=numWorkers-modulo        
        
        d=len(poblacion[0])
        normalizacion=[[] for i in range(n)]
        minsV=[float("inf") for _ in range(d)]
        maxsV=[float("-inf") for _ in range(d)]

    
        for i in range(1,numWorkers+1):
            minsR=comm.recv(source=MPI.ANY_SOURCE)            
            source=status.Get_source()
            maxsR=comm.recv(source=source)
            
            for a in range(d):
                if minsV[a]>minsR[a]: minsV[a]=minsR[a]           
            
            for a in range(d):
                if maxsV[a]<maxsR[a]: maxsV[a]=maxsR[a]

        timeMinEnd = MPI.Wtime()
        print("Tiempo de calculo (MIN): {}".format(timeMinEnd-timeStart))
        for i in range(1,numWorkers+1):
            comm.send(minsV,i)
            comm.send(maxsV,i)

        

        for i in range(1,numWorkers+1):
            data=comm.recv(source=MPI.ANY_SOURCE,tag=tag,status=status)            
            source=status.Get_source()
            
            izq=workers[source-1]
            
            for x in data:
                normalizacion[izq]=x
                izq+=1
        
        timeEnd = MPI.Wtime()

        

        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
    # Codigo de los workers    		
    else: 
        # Recibe de master la parte del array que tiene que ordenar.      
        
        poblacion=comm.recv(source=0) 
        n=len(poblacion)
        #print("WORKER {}, len= {}\n".format(myrank, len(poblacion)))
        d=len(poblacion[0])
        minsV=[float("inf") for _ in range(d)]
        maxsV=[float("-inf") for _ in range(d)]

        for i in range(n):        
            for a in range(d):
                if minsV[a]>poblacion[i][a]: minsV[a]=poblacion[i][a]
                elif maxsV[a]<poblacion[i][a]: maxsV[a]=poblacion[i][a]
        
        
        for x in poblacion:
            for a in range(d):
                if minsV[a]>x[a]: minsV[a]=x[a]
                elif maxsV[a]<x[a]: maxsV[a]=x[a]

        comm.send(minsV,dest=MASTER)
        comm.send(maxsV,dest=MASTER)

        minsV=comm.recv(source=MASTER)
        maxsV=comm.recv(source=MASTER)

        ret=[]
        
        for x in poblacion:
            ind=[]
            for a in range(d): # NORMALIZAR
                ind.append((x[a]-minsV[a])/(maxsV[a]-minsV[a]))
            ret.append(ind)

        comm.send(ret,dest=MASTER)

        



        
            
    




def main2(archivo):  	
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    poblacion=[]
    n=0           		    

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
   		
    # Master lee el archivo .txt con el array de entrada.
    # Tambien hace al aproximacion del numero de workers a la potencia.
    if myrank==MASTER: 
        print("\nEjecutando la segunda forma...")
        #poblacion=lee("datos80")   
        #poblacion=lee("datos2042S")  
        poblacion=lee(archivo,10)   
               
        n=len(poblacion)
        d=len(poblacion[0])
        print("Tam. Poblacion: {}\t Num. Variables: {}\n".format(n,d))

    # Comienza el timer, una vez inicializado todo
    timeStart = MPI.Wtime()
    
    if myrank==MASTER:        
        # Numero de elementos que cada proceso va a procesar inicialmente
        tamProc=n//numWorkers
        # Si mcd(n,numWorkers)!=numWorkers, es porque habra algunos workers con 1 elemento mas
        modulo=n%numWorkers
        # Punteros
        izq=0
        workers=[]

        # Hay al menos 1 elemento para cada worker.
        if tamProc>=1:  
            for i in range(1, modulo+1):                
                comm.send(poblacion[izq:izq+tamProc+1],dest=i)
                workers.append(izq)
                # update
                izq+=tamProc+1
            # Hay algun worker con 1 elemento menos que los demas.
            for i in range(modulo+1,numWorkers+1):
                comm.send(poblacion[izq:izq+tamProc],dest=i)
                workers.append(izq)
                # update
                izq+=tamProc  
        # No hay al menos 1 elemento para cada worker, los workers que se queden sin elemento se finalizan.
        else:
            for i in range(1, modulo+1):   
                comm.send(a[izq], dest=i) 
                workers.append(izq)  
                # update
                izq+=1							
            for i in range(modulo+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                  
            # Se reduce el numero de workers
            numWorkers-=numWorkers-modulo        
        
        d=len(poblacion[0])
        normalizacion=[[] for i in range(n)]
        minsV=[float("inf") for _ in range(d)]
        maxsV=[float("-inf") for _ in range(d)]

        for _ in range(2):
            for i in range(1,numWorkers+1):
                minsR=comm.recv(source=MPI.ANY_SOURCE)            
                source=status.Get_source()
                maxsR=comm.recv(source=source)
                
                for a in range(d):
                    if minsV[a]>minsR[a]: minsV[a]=minsR[a]           
                
                for a in range(d):
                    if maxsV[a]<maxsR[a]: maxsV[a]=maxsR[a]

        timeMinEnd = MPI.Wtime()
        print("Tiempo de calculo (MIN): {}".format(timeMinEnd-timeStart))

        for i in range(1,numWorkers+1):
            comm.send(minsV,i)
            comm.send(maxsV,i)

        

        for i in range(1,numWorkers+1):
            data=comm.recv(source=MPI.ANY_SOURCE,tag=tag,status=status)            
            source=status.Get_source()
            
            izq=workers[source-1]
            
            for x in data:
                normalizacion[izq]=x
                izq+=1
        
        timeEnd = MPI.Wtime()

        #print(normalizacion[0:100])    

        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
    # Codigo de los workers    		
    else: 
        # Recibe de master la parte del array que tiene que ordenar.      
        
        poblacion=comm.recv(source=0) 
        n=len(poblacion)
        #print("WORKER {}, len= {}\n".format(myrank, len(poblacion)))
        d=len(poblacion[0])
        minsV=[float("inf") for _ in range(d)]
        maxsV=[float("-inf") for _ in range(d)]

        for i in range(n//2):        
            for a in range(d):
                if minsV[a]>poblacion[i][a]: minsV[a]=poblacion[i][a]
                elif maxsV[a]<poblacion[i][a]: maxsV[a]=poblacion[i][a]
        
        comm.send(minsV,dest=MASTER)
        comm.send(maxsV,dest=MASTER)
        
        for i in range(n//2,n):        
            for a in range(d):
                if minsV[a]>poblacion[i][a]: minsV[a]=poblacion[i][a]
                elif maxsV[a]<poblacion[i][a]: maxsV[a]=poblacion[i][a]
        """for x in poblacion:
            for a in range(d):
                if minsV[a]>x[a]: minsV[a]=x[a]
                elif maxsV[a]<x[a]: maxsV[a]=x[a]"""

        comm.send(minsV,dest=MASTER)
        comm.send(maxsV,dest=MASTER)

        minsV=comm.recv(source=MASTER)
        maxsV=comm.recv(source=MASTER)

        ret=[]
        
        for x in poblacion:
            ind=[]
            for a in range(d): # NORMALIZAR
                ind.append((x[a]-minsV[a])/(maxsV[a]-minsV[a]))
            ret.append(ind)

        comm.send(ret,dest=MASTER)

        

        
def main3(archivo):  	
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    poblacion=[]
    n=0           		    

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
   		
    # Master lee el archivo .txt con el array de entrada.
    # Tambien hace al aproximacion del numero de workers a la potencia.
    if myrank==MASTER: 
        print("\nEjecutando la tercera forma...")
        poblacion=lee(archivo,10)   
               
        n=len(poblacion)
        d=len(poblacion[0])
        print("Tam. Poblacion: {}\t Num. Variables: {}\n".format(n,d))

    # Comienza el timer, una vez inicializado todo
    timeStart = MPI.Wtime()
    
    if myrank==MASTER:        
        # Numero de elementos que cada proceso va a procesar inicialmente
        tamProc=n//numWorkers
        # Si mcd(n,numWorkers)!=numWorkers, es porque habra algunos workers con 1 elemento mas
        modulo=n%numWorkers
        # Punteros
        izq=0
        workers=[]
        nW=numWorkers
        aux=n
        mod=0
        # Hay al menos 1 elemento para cada worker.
        if tamProc>=1:  
            for i in range(numWorkers):            
                mod=aux%2
                aux//=2
                comm.send(poblacion[izq:izq+aux+mod],dest=nW)
                #workers.append(izq)
                # update
                nW-=1
                izq+=aux+mod
            
        # No hay al menos 1 elemento para cada worker, los workers que se queden sin elemento se finalizan.
        else:
            print("Solo se realiza para datos grandes")
            exit(1)       
        
        d=len(poblacion[0])
        normalizacion=[[] for i in range(n)]
        minsV=[float("inf") for _ in range(d)]
        maxsV=[float("-inf") for _ in range(d)]
        
        # Calcula la parte pequeña del master
        for i in range(izq,n):
            for a in range(d):
                if minsV[a]>poblacion[i][a]: minsV[a]=poblacion[i][a]
                elif maxsV[a]>poblacion[i][a]: maxsV[a]=poblacion[i][a]
        
        # Recibe los valores minimos de los demas
        for i in range(1,numWorkers+1):
            minsR=comm.recv(source=MPI.ANY_SOURCE)            
            source=status.Get_source()
            maxsR=comm.recv(source=source)
            
            for a in range(d):
                if minsV[a]>minsR[a]: minsV[a]=minsR[a]           
            
            for a in range(d):
                if maxsV[a]<maxsR[a]: maxsV[a]=maxsR[a]

        timeMinEnd = MPI.Wtime()
        print("Tiempo de calculo (MIN): {}".format(timeMinEnd-timeStart))

        # Envia la poblacion dividida, los minimos y maximos
        tamProc=n//(numWorkers+1)
        mod=n%(numWorkers+1)
        izq=tamProc
        for i in range(1,mod+1):                        
            comm.send(poblacion[izq:izq+tamProc+1],dest=i)
            comm.send(minsV,dest=i)
            comm.send(maxsV,dest=i)

            # update
            izq+=tamProc+1
        for i in range(mod+1,numWorkers+1):                        
            comm.send(poblacion[izq:izq+tamProc+mod],dest=i)
            comm.send(minsV,dest=i)
            comm.send(maxsV,dest=i)

            # update
            nW-=1
            izq+=aux+mod

        normalizacion=[]
        for i in range(tamProc):
            ind=[]
            for a in range(d): # NORMALIZAR
                ind.append((poblacion[i][a]-minsV[a])/(maxsV[a]-minsV[a]))
            normalizacion.append(ind)
        
        
        # Recibe los datos normalizados que faltan
        for i in range(1,numWorkers+1):
            data=comm.recv(source=i)

            for x in data:
                normalizacion.append(x)
                
    
        #print(normalizacion[0:100])       
        
        timeEnd = MPI.Wtime()

        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
    # Codigo de los workers    		
    else: 
        # Recibe de master la parte del array que tiene que ordenar.      
        
        poblacion=comm.recv(source=0) 
        #print("WORKER {}, len={}\n".format(myrank,len(poblacion)))
        n=len(poblacion)
        #print("WORKER {}, len= {}\n".format(myrank, len(poblacion)))
        d=len(poblacion[0])
        minsV=[float("inf") for _ in range(d)]
        maxsV=[float("-inf") for _ in range(d)]

        # calcula los minimos y maximos de la poblacion recibida
        for x in poblacion:
            for a in range(d):
                if minsV[a]>x[a]: minsV[a]=x[a]
                elif maxsV[a]<x[a]: maxsV[a]=x[a]

        # Los envia
        comm.send(minsV,dest=MASTER)
        comm.send(maxsV,dest=MASTER)

        # recibe los datos
        poblacion=comm.recv(source=MASTER)
        minsV=comm.recv(source=MASTER)
        maxsV=comm.recv(source=MASTER)

        ret=[]
        
        for x in poblacion:
            ind=[]
            for a in range(d): # NORMALIZAR
                ind.append((x[a]-minsV[a])/(maxsV[a]-minsV[a]))
            ret.append(ind)

        # envia los datos calculados
        comm.send(ret,dest=MASTER)


        


def lee(archivo, d):
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".Otros","ficheros","RedNeu", archivo+".txt")

    with open(path, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')  
        
    for i in range(0, len(datos), d):
        ind=[]
        for a in range(d):
            ind.append(float(datos[i+a]))
        
        """altura=float(datos[i])
        peso=float(datos[i+1])
        IMC=float(datos[i+2])"""

        """array.append([altura,peso,IMC])"""
        array.append(ind)

    #print("\n",array)        
    
    return array



archivo="10000_1_10D"
main1(archivo)
main2(archivo)
main3(archivo)