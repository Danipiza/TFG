from mpi4py import MPI
import sys
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
   		
    # Master lee el archivo .txt con el array de entrada.
    # Tambien hace al aproximacion del numero de workers a la potencia.
    if myrank==MASTER: 
        a,n=leeArchivo()   
        m=potencia_lb(numWorkers)
        if m!=numWorkers: 
            print("Eliminando {} workers para que haya potencias de 2 workers.".format(numWorkers-m))
            for i in range(m+1,numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)
            numWorkers-=numWorkers-m

    # Comienza el timer, una vez inicializado todo
    timeStart = MPI.Wtime()
    
    if myrank==MASTER:        
        # Numero de elementos que cada proceso va a procesar inicialmente
        tamProc=n//numWorkers
        # Si mcd(n,numWorkers)!=numWorkers, es porque habra algunos workers con 1 elemento mas
        modulo=n%numWorkers
        # Punteros
        izq=0
        der=tamProc+1

        # Hay al menos 1 elemento para cada worker.
        if tamProc>=1:  
            for i in range(1, modulo+1):                
                comm.send(a[izq:der],dest=i)
                # update
                izq+=tamProc+1
                der+=tamProc+1
            der-=1
            # Hay algun worker con 1 elemento menos que los demas.
            for i in range(modulo+1,numWorkers+1):
                comm.send(a[izq:der],dest=i)
                # update
                izq+=tamProc
                der+=tamProc    
        # No hay al menos 1 elemento para cada worker, los workers que se queden sin elemento se finalizan.
        else:
            for i in range(1, modulo+1):   
                comm.send(a[izq], dest=i)   
                # update
                izq+=1							
            for i in range(modulo+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                  
            # Se reduce el numero de workers
            numWorkers-=numWorkers-modulo        
        # Lista con los identificadores de los workers que siguen trabajando.
        workersList=[(i) for i in range(1,numWorkers+1)]     
        # Termina cuando solo quede un worker, es decir, este totalmente ordenado   
        while numWorkers != 1:
            tmp=[]
            # Solo avanzan los workers que esten en una posicion par 
            #   en la lista de identifiacdores activos
            for i in range(0,numWorkers):
                if i%2==0: 
                    comm.send(workersList[i+1],dest=workersList[i])
                    tmp.append(workersList[i]) # Pasa a la siguiente iteracion.
                else: comm.send(workersList[i-1],dest=workersList[i])
            numWorkers//=2 # Se divide a la mitad el numero de workers
            workersList=tmp # Se actualiza la lista de workers.
        # Una vez termine el bucle, el worker con id 1, espera un mensaje del master. 
        #   en vias -1, para decir que el proceso ya ha terminado y envie el array ordenado.
        comm.send(-1,dest=1)    
        # Recibe el array ordenado. 
        a = comm.recv(source=1, tag=tag,status=status)
        # Termina el timer
        timeEnd = MPI.Wtime()

        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
        if arrayOrdenado(a,n): print("Array ordenado.")
        else: print("Array NO ordenado.")
    # Codigo de los workers    		
    else: 
        # Recibe de master la parte del array que tiene que ordenar.
        a=comm.recv(source=0) 
        # Si no recibe array entonces finaliza su ejecucion
        if a==END_OF_PROCESSING: 
            MPI.Finalize()
            exit(0)       
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
            # Recibe, del master, el identificador con el que tiene que comunicarse
            tmp=comm.recv(source=MASTER)
            # Si recibe -1 envia al master el array ordenado
            if tmp==-1:
                comm.send(a,dest=MASTER)
                break
            # Si recibe un identificador mayor al suyo recibe de este mismo su array ordenado
            elif tmp>myrank: b=comm.recv(source=tmp)                
            # Si recibe un identifiacor menor, envia a ese id su array ordenado y finaliza
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
        
            
    MPI.Finalize()



def leeArchivo():
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
        
    nombre_fichero=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","No_Ordenado", nombre_fichero+".txt")
    print(path)
       
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
        print("El archivo '{}' no existe.".format(nombre_fichero+".txt"))
    
    return array, tam

   


def arrayOrdenado(a, n):
    """
    a: int[]    El array a comprobar
    n: int      Tamaño del array
    return.     True or False
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

main()
