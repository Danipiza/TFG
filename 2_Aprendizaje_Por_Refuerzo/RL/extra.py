import os
import random
from collections import deque

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
    path=os.path.join(dir, ".Otros","ficheros","0.Laberintos", archivo+".txt")
           
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


def cuenta_acciones(matriz,fils,cols):
    
    mX=[-1,0,0,1]
    mY=[0,-1,1,0]

    sumaAcciones=0
    sumaEstados=0
    for i in range(fils):
        for j in range(cols):
            if matriz[i][j]==0:
                sumaEstados*=1
                for k in range(4):
                    if matriz[i+mX[k]][j+mY[k]]==0: sumaAcciones+=1


    print("\nNumero de estados sin mejorar: {}".format(fils*cols*4))
    print("Numero de estados mejorando: {}*2={} (2 tablas Acciones y Q-Table)\n".format(
        sumaAcciones, sumaAcciones*2))

def bfs(matriz, start, end):
    fils=len(matriz)
    cols=len(matriz[0])
    visitado = [[0 for _ in range(cols)] for _ in range(fils)]

    queue = deque([(start, 0)])  
    mX=[-1,0,0,1]
    mY=[0,-1,1,0] 

    while queue:
        (i, j), d=queue.popleft()

        if (i, j)==end: return d

        for k in range(4):            
            x=i+mX[k]
            y=j+mY[k]

            if 0<=x<fils and 0<=y<cols and matriz[x][y]==0 and visitado[x][y]==0:
                visitado[x][y]=1

                queue.append(((x, y), d+1))

    return -1  # No hay camino


def main():
    archivo="50"
    matriz,fils,cols=leeArchivo(archivo)
    
    s=(1,1)
    t=(fils-2, cols-2)

    #cuenta_acciones(matriz,fils,cols)
    
    print("Num. de movimientos minimo para M{}X{}: {}\n".format(fils,cols,
                                                        bfs(matriz,s,t)))



main()