from mpi4py import MPI
import os

# COMPILAR
# mpiexec -np 5 python MergeSortMPI.py

# Este programa inicialmente tiene (np-1) workers. Pasa por un preprocesado para 
#   tener potencias de 2 workers, haciendo una aproximacion hacia abajo de la ultima
#   potencia alcanzada

# Este programa combina los algoritmos de SelectionSort y MergeSort. 
# Cada worker se encarga primero de ordenar por el metodo de SelectionSort la parte del array recibida 
#   del master. Una vez esta ordenado empieza el proceso de intercambio de mensajes entre workers. 
# El master indica a cada worker que tienen que hacer. 
#   - Si reciben un identificador mayor a su id, tienen que esperar a recibir un array de otro worker, para 
#       ordenar y almacenar ambos arrays (el suyo y el recibido). 
#   - Si reciben un identificador menor a su id, tienen que enviar su array ordenado al worker con ese identificador
#       y terminar su ejecucion.
# Con cada iteracion el master reduce el numero de workers hasta que solo quede uno, y este envie al master
#   el array entero ordenado.

def arrayOrdenado(a, n):
    """
    a: int[]        El array a comprobar
    n: int          Tamaño del array

    return => bool  True or False
    """

    for i in range(1,n):    
        if (a[i]<a[i-1]):return False
    
    return True

def potencia_lb(n) :
    pot=1
    while 1:
        if pot*2<=n:
            pot*=2
        else : return pot
 
   

def main():  	
    MASTER = 0              # int.  Valor del proceso master
    END_OF_PROCESSING=-2    # int.  Valor para que un worker termine su ejecucion
    
    timeStart=0.0           # double.   Para medir el tiempo de ejecucion
    timeEnd=0.0

    # Arrays 
    a=[]                    # int[].    Array de Entrada             
    b=[]                    # int[].    Array de Salida
    n=0                     # int.      Tamaño de los arrays       

                      		    

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
    numWs=numWorkers
   		
    totalTimeStart=MPI.Wtime()
    if myrank==MASTER:         
        n=1000000
        a=[i for i in range(n,-1,-1)]
        
        m=potencia_lb(numWorkers)
        if m!=numWorkers: 
            print("Eliminando {} workers para que haya potencias de 2 workers.".format(numWorkers-m))
            for i in range(m+1,numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)
            numWorkers-=numWorkers-m
            numWs=numWorkers
    
    procesar=[100000*i for i in range(1,11)]
    ruta_pruebas = os.path.dirname(os.path.abspath(__file__))

    for x in procesar: 
        # Comienza el timer, una vez inicializado todo
        timeStart = MPI.Wtime()
        
        if myrank==MASTER:
            b=[]
            for val in a[0:x]:
                b.append(val)
            n=len(b)
        

        if myrank==MASTER:                            
            tamProc=n//numWorkers
            modulo=n%numWorkers
            izq=0
            der=tamProc+1

            if tamProc>=1:  
                for i in range(1, modulo+1):                
                    comm.send(b[izq:der],dest=i)               
                    izq+=tamProc+1
                    der+=tamProc+1
                der-=1

                for i in range(modulo+1,numWorkers+1):
                    comm.send(b[izq:der],dest=i)
                    izq+=tamProc
                    der+=tamProc    
            else:
                for i in range(1, modulo+1):   
                    comm.send(b[izq], dest=i)   
                    izq+=1							
                for i in range(modulo+1, numWorkers+1):
                    comm.send(END_OF_PROCESSING, dest=i)   
                       
            workersList=[(i) for i in range(1,numWorkers+1)]       
            while numWorkers != 1:
                tmp=[]
                for i in range(0,numWorkers):
                    if i%2==0: 
                        comm.send(workersList[i+1],dest=workersList[i])
                        tmp.append(workersList[i]) 
                    else: comm.send(workersList[i-1],dest=workersList[i])
                numWorkers//=2 
                workersList=tmp 
            
            comm.send(-1,dest=1)    
            b=comm.recv(source=1, tag=tag,status=status)
            
            timeEnd = MPI.Wtime()

            for i in range(1,numWs+1):
                comm.send(0,dest=i)
            numWorkers=numWs

            
            
            if arrayOrdenado(b,n): print("Array ordenado.")
            else: print("Array NO ordenado.")
            
                       
            
            ruta=os.path.join(ruta_pruebas,"MergeSort_MPI{}.txt".format(numWorkers))    
            with open(ruta, 'a') as archivo:                               
                archivo.write(str(timeEnd-timeStart) + ', ')
            
        else: 
            
            a=comm.recv(source=0) 
            if a!=END_OF_PROCESSING: 
                

                # -----------------------------
                # Ordena mediante SelectionSort        
                n = len(a)
                minE = 0
                pos = 0
                for i in range(n-1):
                    minE = a[i]
                    pos = i
                    for j in range(i+1, n):
                        if minE > a[j]:
                            minE = a[j]
                            pos = j            
                    tmp = a[i]
                    a[i] = a[pos]
                    a[pos] = tmp
                # -----------------------------        
                while(True):                       
                    tmp=comm.recv(source=MASTER)
                    if tmp==-1:
                        comm.send(a,dest=MASTER)
                        break
                    elif tmp>myrank: b=comm.recv(source=tmp)                
                    else :
                        comm.send(a,dest=tmp) 
                        break
                    
                    # ----------------------------
                    # Proceso merge() de MergeSort
                    i=0
                    j=0
                    aux=[]
                    n=len(a)
                    m=len(b)
                    while i<n and j<m:
                        if a[i]<=b[j]:
                            aux.append(a[i])
                            i+=1
                        else :
                            aux.append(b[j])
                            j+=1
                    while i<n:
                        aux.append(a[i])
                        i+=1
                    while j<m:
                        aux.append(b[j])
                        j+=1    
                    a=aux
                    # ----------------------------
            else: exit(1)
            comm.recv(source=MASTER)

    
    
     
            
    



main()
