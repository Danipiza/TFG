from mpi4py import MPI
import numpy as np
import os
import sys


# EJECUTAR
# mpiexec -np 5 python MulMatrizMPI2.py

"""
NO TERMINADO PORQUE NO ES OPTIMO


TODO MASTER ENVIA TODAS LA FILAS
"""

# Generar matriz aleatoria
def generate_matrix(valor_maximo, tam):
    return np.random.randint(0, valor_maximo, size=(tam, tam))

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
    path=os.path.join(dir, ".Otros","ficheros","1.Matrices", archivo+".txt")
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
    END_OF_PROCESSING = 0  # End of processing

    NROWS = 10  # Number of rows to each worker
    
    filas=0
    columnas=0 
    tam = 100  # Matrix size
    valor_maximo = 10  # Maximum number value for generating each matrix


    comm = MPI.COMM_WORLD
    myrank = comm.Get_rank()
    numProc = comm.Get_size()
    numWorkers=numProc-1


    if (NROWS * (numWorkers)) > tam:
        if myrank == MASTER:
            print(f"Wrong configuration for NROWS ({NROWS}). SIZE ({tam}) < numWorkers({numProc-1})*NROWS({NROWS})")
            print("At least, each worker must receive {} rows to be processed".format(NROWS))
        MPI.Finalize()
        exit(-1)

    matrizA=[[]]
    matrizB=[[]]
    if myrank == MASTER:

        # Generate matrix A			
        #print("Generating matrix A (%dx%d)\n", tam, tam);        
        #matrixA=generate_matrix(valor_maximo, tam)
        print("Leyendo matriz A ({}x{})".format(filas,columnas))
        matrizA,filas,columnas=leeArchivo("M10X10")
        if PRINT:
            print("Matrix A:\n")
            print(matrizA)
            print("\n\n")
        

        # Generate matrix B
        #print("Generating matrix B (%dx%d)\n", tam, tam);   
        #matrizB = generate_matrix(valor_maximo, tam)
        print("Leyendo matriz B ({}x{})".format(filas,columnas)) 
        matrizB,_,_=leeArchivo("M10X10")
        if PRINT:
            print("Matrix B:")
            print(matrizB)
            print("\n\n")

    # Broadcast matrix B
    matrizB = comm.bcast(matrizB, root=MASTER)

    if myrank == MASTER:
        matrixC = np.zeros((tam, tam), dtype=int)

        sent_rows = 0
        current_row = 0
        processed_rows = 0

        while processed_rows < tam:
            for i in range(1, numProc):
                sent_rows = min(NROWS, tam - current_row)

                comm.send(sent_rows, dest=i, tag=1)
                comm.send(current_row, dest=i, tag=2)
                comm.send(matrizB, dest=i, tag=3)

                current_row += sent_rows

            for i in range(1, numProc):
                sent_rows = min(NROWS, tam - processed_rows)

                received_data = comm.recv(source=i, tag=4)
                received_rows, received_matrix = received_data

                matrixC[processed_rows : processed_rows + received_rows, :] = received_matrix

                processed_rows += received_rows

        if PRINT:
            print("Matrix C:")
            print(matrixC)
            print("\n\n")

    else:
        while True:
            sent_rows = comm.recv(source=MASTER, tag=1)

            if sent_rows == END_OF_PROCESSING:
                break

            current_row = comm.recv(source=MASTER, tag=2)
            matrizB = comm.recv(source=MASTER, tag=3)

            matrizA = np.zeros((sent_rows, tam), dtype=int)
            matrixC = np.zeros((sent_rows, tam), dtype=int)

            comm.Recv(matrizA, source=MASTER, tag=5)

            for i in range(sent_rows):
                for j in range(tam):
                    matrixC[i, j] = np.dot(matrizA[i, :], matrizB[:, j])

            comm.send((sent_rows, matrixC), dest=MASTER, tag=4)

    MPI.Finalize()

main()