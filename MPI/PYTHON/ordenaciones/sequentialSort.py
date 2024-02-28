from mpi4py import MPI
import sys
import math
import time

# TODO FALTA TERMINARLO

#define MASTER 0 # Master process
#define END_OF_PROCESSING 0 # End of processing

# COMPILAR
# mpirun -np 5 python <name>.py

MASTER = 0
END_OF_PROCESSING=-2
INF=sys.maxsize

# PROBAR, AL ENVIAR DATOS, 
# - ES MAS EFICIENTE ENVIAR UNA PARTE DEL ARRAY
# - PONERLO COMO VARIABLE GLOBAL
# - ENVIAR TODO EL ARRAY CON MPI_Bcast()


def main():
    # Variables MPI
  	

    timeStart=0.0           # double.
    timeEnd=0.0
    END_OF_PROCESSING=-2    # int.
    
    # Arrays 
    a=[]                    # int[]. Entrada
    b=[]                    # int[]. Salida          
    n=0                     # int.   Tamaño de los arrays                           

    # Variables usadas en el proceso MPI    
    arrayProc=0             # int. Puntero de la parte procesada del array a
    pos=-1                  # int. Variables que se envian y reciben entre los procesos
    val=0                   
    cont=0                  # int. Variable auxiliar para los workers, que cuentan los elementos mayores al recibido

		    

    # Init MPI.  rank y tag de MPI y el numero de procesos creados (el primero es el master)
    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
   
    # CONTROL DE ERRORES
    """if (<Error>){
        if (myrank == MASTER) {
            printf("Wrong configuration for NROWS (%d). SIZE (%d) < numWorkers(%d)*NROWS(%d)\n", NROWS, SIZE, numProc-1, NROWS);
            printf ("At least, each worker must receive %d rows to be processed\n", NROWS);
        }
        MPI_Finalize();
        exit(-1);			
    }"""
		
    # master lee el archivo .txt con el array de entrada
    # cuenta el tamaño del array de entrada e inicializa el array de salida
    if myrank==MASTER: 
        a,n=leeArchivo() 
        b=[(INF) for i in range(n)]

        """# Envia el tamaño de los arrays a los workers
        comm.bcast(n, root=0)        
        # Envia el array entero a los workers, lo necesitan entero
        comm.bcast(a, root=0)     
        else:
        print("Worker",myrank) 
        # Recibe el tamaño de los arrays
        n= comm.bcast(n, root=0)                        
        # Recibe el array entero
        a = comm.bcast(a, root=0)  
        print("Worker",myrank, "Lee array:",a, "de tam:",n)   
        """
    

    # Envia el tamaño de los arrays a los workers
    n=comm.bcast(n, root=MASTER)        
    # Envia el array entero a los workers, lo necesitan entero
    a=comm.bcast(a, root=MASTER)  
    
    if myrank!=0: print("Worker:",myrank,"Array:",a,"tam",n)  
    else : print("Master")

    # Comienza el timer una vez inicializado todo
    timeStart = MPI.Wtime()
    
    if myrank==MASTER:
        # Init
        arrayProc=0;        
        print("Init")
        # Distribucion inicial
        if numWorkers<=n:  
            for i in range(1, numWorkers+1):                           
                # Envia val
                comm.send(a[arrayProc], dest=i)                
                # update
                arrayProc+=1        
        else:
            aux=numWorkers%n
            for i in range(1, numWorkers-aux+1):                      
                # Envia val
                comm.send(a[arrayProc], dest=i)   
                # update
                arrayProc+=1							
            for i in range(numWorkers-aux+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                  
            
            numWorkers-=aux        

        # Hay mas elementos a procesar
        while arrayProc<n:		
            pos=-1;	
            # Recibe los resultados de algun worker
            pos = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
            source_rank = status.Get_source()
            
            val = comm.recv(source=source_rank, tag=tag,status=status)
            #print("Master recibe:",pos,"de:", source_rank)
            

            # Procesa los datos recibidos
            # Si la posicion en el array b esta ocupado, es porque es el mismo valor
            # y busca el siguiente espacio disponible           
            while b[pos]!=INF: pos+=1
            b[pos]=val

            # Envia el siguiente valor a procesar    
            comm.send(a[arrayProc], dest=status.source)   
            # Update
            arrayProc+=1

            # Fin
            if arrayProc==n: break	

            					
        

        # Ultimos valores por procesar
        while numWorkers!=0:
            pos = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
            source_rank = status.Get_source()
            
            val = comm.recv(source=source_rank, tag=tag,status=status)


            while b[pos]!=INF: pos+=1
            b[pos]=val

            comm.send(END_OF_PROCESSING, dest=status.source, tag=tag)   
            numWorkers-=1
        
        timeEnd = MPI.Wtime()

        print("Tiempo de ejecucion:", timeEnd-timeStart)

        if arrayOrdenado(b,n): print("Array ordenado")
        else: print("Array no ordenado")
    		
    else: # workers
        while(True):
            # Recibe el valor del array a procesar
            val=comm.recv(source=0)

            if val==-2: break

            cont=0
            for i in range(n):            
                if a[i]<val: cont+=1
            
            comm.send(cont, dest=0)
            comm.send(val, dest=0)
            
          
    if myrank==0: print(b)
    # End MPI environment
    #MPI.Finalize()

    return 0




def leeArchivo():
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    file_name = input("Introduce un nombre del fichero: ")
    array = []    
    tam=0    
    try:        
        with open(file_name, 'r') as archivo: # modo lectura
            # Lee las lineas del archivo
            for linea in archivo:
                # Divide por espacios
                numeros_en_linea = linea.split()                
                
                # Convertir de string a int
                for numero in numeros_en_linea:
                    array.append(int(numero))
                    tam+=1
    
    except FileNotFoundError:
        print("El archivo '{}' no existe.".format(file_name))
    
    return array, tam


    
#printArray([(i) for i in range(20)], 20)
def printArray(a, n):
    print("Array:")
    for i in range(n):
        print(a[i], end=" ")    
    print()    

#a,tam=leeArchivo()
#printArray(a, tam)

def arrayOrdenado(a, n):
    """
    a: int[]    El array a comprobar
    n: int      Tamaño del array
    return.     True or False
    """
    for i in range(1,n):    
        if (a[i]!=a[i-1]+1):return False
    
    return True


main()