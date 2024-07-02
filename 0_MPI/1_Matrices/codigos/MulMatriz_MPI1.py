from mpi4py import MPI
import numpy as np
import sys
import os

# EJECUTAR
# mpiexec -np 5 python MulMatriz_MPI1.py

"""
Multiplicacion de matrices usando MPI.

El Master envia filas conforme los Workers terminan un calculo.
"""

# Generar matriz aleatoria
def genera_matriz(valor_maximo, n, m):
    return np.random.randint(0, valor_maximo, size=(n, m))

def print_matriz(matriz):
    i=0
    for x in matriz:
        print("Fila {}: {}".format(i, x))
        i+=1

def leeArchivo(archivo):
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

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".otros","ficheros","1_Matrices", archivo+".txt")
    #print(path)
       
    filas=0
    columnas=0 
    M=[]
    
    try:        
        with open(path, 'r') as archivo: # modo lectura
            for linea in archivo:                                
                filas+=1
                columnas=0
                array = [] 
                numeros_en_linea = linea.split() # Divide por espacios                                              
                for numero in numeros_en_linea:
                    array.append(int(numero))
                    columnas+=1
                M.append(array)
                
    
    except FileNotFoundError:
        print("El archivo '{}' no existe.".format(archivo+".txt"))
    
    return M, filas, columnas

def main():    
    MASTER = 0              # int.      Master 
    PRINT = False           # boolean.  Imprimir matrices
    END_OF_PROCESSING = -1  # End of processing
    

    filas,columnas=0,0
    valor_maximo = 10  # Maximum number value for generating each matrix


    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1
    

    matrizA=[[]]
    matrizB=[[]]
    if myrank == MASTER:

        # Generate matrix A			
        #print("Generando matriz A ({}x{})".format(filas,columnas))        
        #matrizA=genera_matriz(valor_maximo,filas,columnas)
        matrizA,filas,columnas=leeArchivo("M10X10")
        print("Matriz A ({}x{})".format(filas,columnas))
        
        if PRINT:
            print("Matriz A:\n")
            #print_matriz(matrizA)
            print(matrizA)
            print("\n\n")
        
        m=len(matrizA[0])

        # Generate matrix B
        #print("Generando matriz B ({}x{})".format(filas,columnas))        
        #matrizB = genera_matriz(valor_maximo,filas,columnas)
        
        matrizB,_,_=leeArchivo("M10X10")
        print("Matriz B ({}x{})".format(filas,columnas))        
        if PRINT:
            print("Matriz B:")
            #print_matriz(matrizB)
            print(matrizB)
            print("\n")
        matrizC = [[] for _ in range(filas)]
        
    matrizB=comm.bcast(matrizB, root=MASTER) 
    filas=comm.bcast(filas, root=MASTER) 
    columnas=comm.bcast(columnas, root=MASTER) 
    
    timeStart = MPI.Wtime()

    if myrank==MASTER:
        # Init
        filaAct=0
             
        if numWorkers<=filas:  
            for i in range(1, numWorkers+1):                           
                # Envia val
                comm.send(filaAct, dest=i)
                comm.send(matrizA[filaAct], dest=i)                
                # update
                filaAct+=1        
        else:
            aux=numWorkers%filas
            for i in range(1, numWorkers-aux+1):                      
                # Envia val
                comm.send(filaAct, dest=i)
                comm.send(matrizA[filaAct], dest=i)                
                # update
                filaAct+=1							
            for i in range(numWorkers-aux+1, numWorkers+1):
                comm.send(END_OF_PROCESSING, dest=i)                 
            
            
            
            numWorkers-=aux
        
        while numWorkers>0:	
            # Recibe los resultados de algun worker
            filaInd=comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)            
            source_rank=status.Get_source()
            filaC = comm.recv(source=source_rank, tag=tag,status=status)

            # Procesa los datos recibidos
            matrizC[filaInd]=filaC


            # Envia el siguiente valor a procesar 
            if filaAct<filas:
                comm.send(filaAct, dest=status.source)
                comm.send(matrizA[filaAct], dest=status.source)   
                # Update
                filaAct+=1
            else:
                comm.send(END_OF_PROCESSING, dest=status.source)   
                numWorkers-=1
        timeEnd = MPI.Wtime()
        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
        if PRINT:
            print("Matriz C ({}x{}), calculada".format(filas,columnas))        
            print(matrizC)
            print("\n")
        
    else: # Workers
        while True:
            # Recibe datos
            filaInd=comm.recv(source=0) # int.                     
            if filaInd==-1: break        
            filaA=comm.recv(source=0) # int[].                           
                    
            
            tmp=0
            filaC=[]
            
            #for k in range(m):
            for i in range(columnas):
                for j in range(filas):
                    tmp+=filaA[j]*matrizB[j][i]
                filaC.append(tmp)
                tmp=0                            

            # Envia resultados
            comm.send(filaInd, dest=0)
            comm.send(filaC, dest=0)
				
        
    
    # End MPI environment
    MPI.Finalize()

    


    

main()