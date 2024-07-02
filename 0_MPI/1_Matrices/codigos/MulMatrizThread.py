from mpi4py import MPI

import sys
import os
import time

# EJECUTAR
# py MulMatrixThread.py

# Los hilos estan muy mal optimizados en python, por eso solo me centro en MPI

"""
Normal:
M100X100    =    0.078700400001253s
M1000X1000  =    88.15625s
"""


"""
MPI:
4 WORKERS (MASTER NO HACE MAS QUE DIRIGIR)
M100X100    =   0.0141010994149s    speed-up=5.582
M1000X1000  =   16.120811400373s    speed-up=5.46
"""


import threading
""" TARDA MUCHO MAS
4 HILOS:
M100X100   =    0.05932909683034s   speed-up=1.32
M1000X1000 =    65.99578289999045s  speed-up=1.335
"""

import multiprocessing 
# TODO 
# NO TIENEN MEMORIA COMPARTIDA por defecto
# This is because each process in multiprocessing has its own memory space, 
# so changes made by one process aren't reflected in the memory of other processes.

"""
4 HILOS:
M100X100   =    0.015625s           speed-up=5.04
M1000X1000 =    18.770753199991304s speed-up=4.69

"""

import concurrent.futures
"""
OTRA POSIBLE LIBRERIA
"""



# Funcion para cada thread
def multiply_row(id, matrizA, matrizB, matrizC, n,m, rows):    

    for row in range(rows[0],rows[1]):
        for col in range(m):
            tmp=0
            for k in range(n):
                tmp+=matrizA[row][k]*matrizB[k][col]
            matrizC[row][col] = tmp

    
    #print(matrizC[0][0])

    print("Termina",id)



def create_threads(numThreads, matrizA, matrizB, matrizC):
    threads = []

    asig=[]

    n=len(matrizA)
    m=len(matrizB)
    tam=n//numThreads
    mod=n%numThreads
    izq=0
    for i in range(mod):
        asig.append([izq,izq+tam+1])
        izq+=tam+1

    for i in range(mod,numThreads):
        asig.append([izq,izq+tam])
        izq+=tam

    

    #barrier = multiprocessing.Barrier(numThreads)
    

    for i in range(numThreads):
        # print("MASTER",i)
        """thread = threading.Thread(target=multiply_row, args=(i, barrier, matrizA, matrizB, matrizC, n,m, asig[i]))
        threads.append(thread)
        thread.start()"""

        process = multiprocessing.Process(target=multiply_row, args=(i, matrizA, matrizB, matrizC, n,m, asig[i]))
        threads.append(process)
        process.start()

    # Espera a que todos terminen 
    for thread in threads:
        thread.join()
    


def main():       
    PRINT = False           # boolean.  Imprimir matrices

    matrizA,fA,cA=leeArchivo("M10X10")
    print("Matriz A({}x{}), generada.".format(fA,cA))
    if PRINT: print(matrizA)
    matrizB,fB,cB=leeArchivo("M10X10")
    print("Matriz B({}x{}), generada.".format(fB,cB))
    if PRINT: print(matrizB)

    if cA != fB:
        print("No se pueden multiplicar las matrices. cA ({}) != fB ({})".format(cA,fB))
    else:
        matrizC=[]
        for _ in range(fA):
            matrizC.append(multiprocessing.Array('f', [0.0 for _ in range(cB)]))
        
        #matrizC = [[0.0 for _ in range(cB)] for _ in range(fA)]

    
    
    
    timeStart = time.perf_counter()
    #timeStart = MPI.Wtime()

    create_threads(4,matrizA, matrizB, matrizC)
    
    timeEnd = time.perf_counter()
    #timeEnd = MPI.Wtime()

    print("Tiempo de ejecucion: {}s".format(timeEnd-timeStart))
    
    if PRINT: 
        for f in matrizC:
            for val in f:
                print(val, end=" ")
            print()

            
        



def multiply_row2(id, row, matrix):
    #print(id)
    result_row = []
    for col in range(len(matrix[0])):
        result = 0
        for i in range(len(row)):
            result += row[i] * matrix[i][col]
        result_row.append(result)
    return result_row

def multiplicar_matrices(numThreads, matrix1, matrix2):
    
    id=0
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
        futures = []
        for row in matrix1:
            futures.append(executor.submit(multiply_row2, id, row, matrix2))
        
        for future in concurrent.futures.as_completed(futures):
            result.append(future.result())
        id+=1
    
    return result

def main2():
    print("Usando concurrent.futures import ThreadPoolExecutor\n")
    PRINT = False           # boolean.  Imprimir matrices

    matrizA,fA,cA=leeArchivo("M10X10")
    print("Matriz A({}x{}), generada.".format(fA,cA))
    if PRINT: print(matrizA)
    matrizB,fB,cB=leeArchivo("M10X10")
    print("Matriz B({}x{}), generada.".format(fB,cB))
    if PRINT: print(matrizB)

    if cA != fB:
        print("No se pueden multiplicar las matrices. cA ({}) != fB ({})".format(cA,fB))
    else:
        matrizC = [[0.0 for _ in range(cB)] for _ in range(fA)]


    result = multiplicar_matrices(4, matrizA, matrizB)
    for row in result:
        print(row)



    


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
    
if __name__ == "__main__":
    main()
    #main2()