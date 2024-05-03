from mpi4py import MPI
import time
import sys
import os


def guarda_datos(archivo,datos,tamDatos):    
    

    with open(archivo[0], 'w') as file:
        for i, val in enumerate(datos[0]):
            file.write("{}, ".format(val))
        file.write("\n")
    with open(archivo[1], 'w') as file:
        for i, val in enumerate(tamDatos):
            file.write("{}, ".format(val))
        file.write("\n")

def print_matriz(matriz):
    i=0
    for x in matriz:
        print("Fila {}: {}".format(i, x))
        i+=1



def main():       
    PRINT = False           # boolean.  Imprimir matrices

    matrizA,fA,cA=leeArchivo("M1000X1000")
    print("Matriz A({}x{}), generada.".format(fA,cA))    
    matrizB,fB,cB=leeArchivo("M1000X1000")
    print("Matriz B({}x{}), generada.".format(fB,cB))
    

    if cA != fB:
        print("No se pueden multiplicar las matrices. cA ({}) != fB ({})".format(cA,fB))
    else:
        matrizC = [[0 for _ in range(cB)] for _ in range(fA)]
    
    # 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460,
    procesa=[480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000]

    datos=[[]]
    tamDatos=[]

    for x in procesa:
        A=[[matrizA[i][j] for j in range(x)] for i in range(x)]        
        B=[[matrizB[i][j] for j in range(x)] for i in range(x)]        
        matrizC = [[0 for _ in range(x)] for _ in range(x)]
        timeStart = MPI.Wtime()
        
        for i in range(x):
            for j in range(x):
                for k in range(x):
                    matrizC[i][j]+=A[i][k]*B[k][j]
        
        timeEnd = MPI.Wtime()
        print("Tiempo de ejecucion: {}s".format(timeEnd-timeStart))

        datos[0].append(timeEnd-timeStart)
        tamDatos.append(x)
        guarda_datos(["MulMatriz.txt","TamDatos.txt"],datos,tamDatos)
    
    
        
    

    

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
    

main()