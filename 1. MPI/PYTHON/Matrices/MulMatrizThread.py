#from mpi4py import MPI

import sys
import os
import time

"""
Normal:
M100X100    =    0.15625s
M1000X1000  =    196.84375s
"""

import threading
"""
medido por time

M100X100   =    0.125s
M1000X1000 =    125.84375s
"""

import multiprocessing
"""
medido por time

M100X100   =    0.046875s
M1000X1000 =    56.25875s
"""

from concurrent.futures import ThreadPoolExecutor



def print_matriz(matriz):
    i=0
    for x in matriz:
        print("Fila {}: {}".format(i, x))
        i+=1

# Funcion para cada thread
def multiply_row(id, matrizA, matrizB, matrizC, n,m, rows):    
    for row in range(rows[0],rows[1]):
        for col in range(m):
            tmp=0
            for k in range(n):
                tmp+=matrizA[row][k]*matrizB[k][col]
            matrizC[row][col] = tmp
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

    for i in range(numThreads):
        # print("MASTER",i)
        """thread = threading.Thread(target=multiply_row, args=(i, matrizA, matrizB, matrizC, n,m, asig[i]))
        threads.append(thread)
        thread.start()"""

        process = multiprocessing.Process(target=multiply_row, args=(i, matrizA, matrizB, matrizC, n,m, asig[i]))
        threads.append(process)
        process.start()

    """with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(5):
            executor.submit(multiply_row, args=(i, matrizA, matrizB, matrizC, n,m, asig[i]))"""

    # Espera a que todos terminen 
    for thread in threads:
        thread.join()


def main():       
    PRINT = False           # boolean.  Imprimir matrices

    matrizA,fA,cA=leeArchivo("M100X100")
    print("Matriz A({}x{}), generada.".format(fA,cA))
    if PRINT: print(matrizA)
    matrizB,fB,cB=leeArchivo("M100X100")
    print("Matriz B({}x{}), generada.".format(fB,cB))
    if PRINT: print(matrizB)

    if cA != fB:
        print("No se pueden multiplicar las matrices. cA ({}) != fB ({})".format(cA,fB))
    else:
        matrizC = [[0 for _ in range(cB)] for _ in range(fA)]
    
    
    
    timeStart = time.process_time()
    #timeStart = MPI.Wtime()

    create_threads(4,matrizA, matrizB, matrizC)
    
    timeEnd = time.process_time()
    #timeEnd = MPI.Wtime()

    print("Tiempo de ejecucion: {}s".format(timeEnd-timeStart))
    
    if PRINT: 
        for f in matrizC:
            print(f)
        
    

    


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
    path=os.path.join(dir, ".Otros","ficheros","Matrices", archivo+".txt")
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