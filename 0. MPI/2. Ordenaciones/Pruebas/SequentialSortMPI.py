from mpi4py import MPI
import sys
import os

# COMPILAR
# mpiexec -np 5 python SequentialSortMPI.py

# Este programa tiene (np-1) workers, cada worker recibe un elemento
#   que envia el master para realizar el recorrido en el array


datos=[]
tamArray=[]


# Signal handler 
def signal_handler(sig, frame):
    print("Ctrl+C, almacenando en ")
    guarda_datos(["SequentialSortMPI",
                  "TamArray.txt"])
    sys.exit(0)

def guarda_datos(archivo):    
    """print(tamArray)
    for x in datos:
        print(x,"\n")"""
    

    with open(archivo[0], 'w') as file:
        for i, val in enumerate(datos):
            file.write("{}, ".format(val))
        file.write("\n")
    with open(archivo[1], 'w') as file:
        for i, val in enumerate(tamArray):
            file.write("{}, ".format(val))
        file.write("\n")
    
   

def main():  	
    MASTER = 0              # int.
    END_OF_PROCESSING=-2
    INF=sys.maxsize

    timeStart=0.0           # double. Para medir el tiempo de ejecucion
    timeEnd=0.0
    
    
    # Arrays 
    a=[]                    # int[]. Array Entrada
    b=[]                    #        Salida Salida          
    c=[]
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
    numWs=numWorkers
   
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
        a,n=leeArchivo("100000Desc",None) 
        
    
    procesar=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]

    """try:"""    
    for x in procesar: 
        # Comienza el timer una vez inicializado todo
        timeStart = MPI.Wtime()

        if myrank==MASTER:
            c=[]
            for val in a[0:x]:
                c.append(val)
            for i in range(1,numWorkers+1):
                comm.send(c,dest=i)
            n=len(c)
            b=[(INF) for _ in range(n)]
        else:
            a=comm.recv(source=MASTER)
            n=len(a)
                    
        

        

        if myrank==MASTER:
            arrayProc=0;        
            
            if numWorkers<=n:  
                for i in range(1, numWorkers+1):   
                    comm.send(c[arrayProc], dest=i)      
                    arrayProc+=1        
            else:
                aux=numWorkers%n
                for i in range(1, numWorkers-aux+1):  
                    comm.send(c[arrayProc], dest=i) 
                    arrayProc+=1							
                for i in range(numWorkers-aux+1, numWorkers+1):
                    comm.send(END_OF_PROCESSING, dest=i)                  
                
                numWorkers-=aux        

            while arrayProc<n:		
                pos=-1;	
                pos = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
                source_rank = status.Get_source()
                
                val = comm.recv(source=source_rank, tag=tag,status=status)
                
                while b[pos]!=INF: pos+=1
                b[pos]=val
    
                comm.send(a[arrayProc], dest=status.source)   
                arrayProc+=1

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
            for i in range(1,numWs+1):
                comm.send(0,dest=i)
            numWorkers=numWs

            if arrayOrdenado(b,n): print("Array ordenado")
            else: 
                print("Array no ordenado")
                print(b)

            datos.append((timeEnd-timeStart))
            tamArray.append(n)
                
        else: # workers
            while(True):
                val=comm.recv(source=0)

                if val==-2: break

                cont=0
                for i in range(n):            
                    if a[i]<val: cont+=1
                
                comm.send(cont, dest=0)
                comm.send(val, dest=0)
            comm.recv(source=MASTER)

        if myrank==MASTER:
            guarda_datos(["SequentialSort_MPI{}.txt".format(numWorkers),"TamArray.txt"])       
    """except KeyboardInterrupt:
        print('\nProgram interrupted, storing processed array in a file...')
        guarda_datos(["SequentialSortMPI",
                  "TamArray.txt"])
        sys.exit(0)"""
    return 0





def leeArchivo(archivo, carpeta):
    """
    archivo: string     Archivo a leer
    carpeta: string     Carpeta en el que se encuentra (Ordenado, No_Ordenado)

    return =>
    array: int[].       Array con los enteros leidos
    tam: int.           Tamaño del array leido
    """
    
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)


    if carpeta==None: carpeta="Ordenado"
    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","1.Array", carpeta, archivo+".txt")
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
        print("El archivo '{}' no existe.".format(archivo+".txt"))
    
    return array, tam

   


def arrayOrdenado(a, n):
    """
    a: int[]        El array a comprobar
    n: int          Tamaño del array

    return => bool  True or False
    """

    for i in range(1,n):    
        if (a[i]<a[i-1]):return False
    
    return True


main()