from mpi4py import MPI
import sys
import os



def print_matriz(matriz):
    i=0
    for x in matriz:
        print("Fila {}: {}".format(i, x))
        i+=1



def main():       
    PRINT = False           # boolean.  Imprimir matrices

    matrizA,fA,cA=leeArchivo()
    print("Matriz A({}x{}), generada.".format(fA,cA))
    if PRINT: print(matrizA)
    matrizB,fB,cB=leeArchivo()
    print("Matriz B({}x{}), generada.".format(fB,cB))
    if PRINT: print(matrizB)

    if cA != fB:
        print("No se pueden multiplicar las matrices. cA ({}) != fB ({})".format(cA,fB))
    else:
        matrizC = [[0 for _ in range(cB)] for _ in range(fA)]
    timeStart = MPI.Wtime()
    for i in range(fA):
        for j in range(cB):
            for k in range(cA):
                matrizC[i][j]+=matrizA[i][k]*matrizB[k][j]
    
    timeEnd = MPI.Wtime()
    print("Tiempo de ejecucion: {}s".format(timeEnd-timeStart))
    
    if PRINT: print(matrizC)
        
    

    

# TODO COMPROBAR SI FUNCIONA
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
    path=os.path.join(dir, ".Otros","ficheros","Matrices", nombre_fichero+".txt")
    print(path)
       
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
        print("El archivo '{}' no existe.".format(nombre_fichero+".txt"))
    
    return M, filas, columnas
    

main()