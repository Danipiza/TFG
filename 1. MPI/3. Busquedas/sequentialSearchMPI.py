from mpi4py import MPI
import sys
import os

"""
COSTE O(N^2)

100000 10;70.1 - 30;56.0 - 15;56.3 - 25;
            MPI (20)    MPI(50)     NORMAL
10000       0.51                    4.5
100000      55          55.9        440.4
1000000     

"""





def main():  
    MASTER = 0              # int.
    INF=sys.maxsize         
    END_OF_PROCESSING=-2    

    timeStart=0.0           # double.
    timeEnd=0.0             
    
    
    # Arrays 
    a=[]                    # int[]. Entrada    
    enc=False                              

    # Variables usadas en el proceso MPI        
    pos=-1                  # int. Variables que se envian y reciben entre los procesos
    val=0                   
    

		    

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
        a,n=leeArchivo("100",None) 
        val = int(input("Introduce valor a buscar: "))
        
        
    val=comm.bcast(val, root=MASTER)    

    # Comienza el timer una vez inicializado todo
    timeStart=MPI.Wtime()
    
    if myrank==MASTER:
        # Init      
        tamEnviar=n//numWorkers
        workesExtra=n%numWorkers
        izq=0
        der=tamEnviar

        if tamEnviar>=1:
            der+=1
            for i in range(1, workesExtra+1):                                  
                comm.send(a[izq:der], dest=i) 
                comm.send(izq,dest=i)
                #print("Master envia a W",i,a[izq:der])  
                izq+=tamEnviar+1
                der+=tamEnviar+1
            der-=1
            for i in range(workesExtra+1, numWorkers+1):  
                comm.send(a[izq:der], dest=i)   
                comm.send(izq,dest=i)
                izq+=tamEnviar
                der+=tamEnviar
        else :
            aux=numWorkers-workesExtra
            for i in range(1, numWorkers-aux+1):                      
                comm.send(a[(i-1):(i)], dest=i)   
                comm.send((i-1),dest=i)							
            for i in range(numWorkers-aux+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                  
            numWorkers-=aux
      
                            
            
                    

        # Procesa los datos
        while numWorkers>0:	
            rec = comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)
            status.Get_source()           

            if rec!=-1: enc=True
            

            # Envia el siguiente valor a procesar    
            comm.send(END_OF_PROCESSING, dest=status.source) 
            numWorkers-=1  
            
        timeEnd = MPI.Wtime()
        
        

        print("Tiempo de ejecucion:", timeEnd-timeStart)
        

        if enc==True: print("Valor,",val,"Encontrado")
        else: print("Valor", val, "No esta en el array")
        #print(b)
    		
    else: # workers
        while(True):
            # Recibe el valor del array a procesar   
            a=comm.recv(source=0) 
            if a==-2: break           
            pos=comm.recv(source=0)
            n=len(a)
            i=0
           

            while i<n:
                if a[i]==val: break
                i+=1
                
            if i==n: comm.send(-1, dest=0)
            else: comm.send(pos+i, dest=0)
            
          
    # End MPI environment
    #MPI.Finalize()

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


    if carpeta==None: carpeta="No_Ordenado"
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
    a: int[]    El array a comprobar
    n: int      Tamaño del array
    return.     True or False
    """
    for i in range(1,n):    
        if (a[i]!=a[i-1]+1):return False
    
    return True


main()
