from mpi4py import MPI
import sys
import os

# EJECUTAR
# py .\BinarySearch.py


"""
Busqueda binaria de un elemento.
El array tiene que estar ordenado para poder realizar la busqueda.

Recorre el array dividiendo por la mitad hasta encontrar el elemento o que el subarray a buscar sea 1.
"""

def main():
    INF=sys.maxsize         # int. Variable infinito con el maximo valor de int

    timeStart=0.0           # double. Para medir el tiempo de ejecucion
    timeEnd=0.0
   
    a=[]                    # int[]. Array Entrada         
    n=0                     # int.   Tamaño de los arrays                           
    
    izq=0
    der=0
    m=0
    encontrado=-1

        
    a,n=leeArchivo("100",None)                # Lee el archivo devolviendo el array y su tamaño        
    if not arrayOrdenado(a,n): 
        print("Array tiene que estar ordenado")
        exit(0)
    
    der=n-1    
    val=int(input("Introduce un valor a buscar: "))
    
              

    timeStart=MPI.Wtime()           # Comienza el Algoritmo

    # Procesar
               
    while izq<=der:
        m=(izq+der)//2
        if a[m]==val:
            encontrado=m
            break
        elif a[m]>val:
            der=m-1
        else:
            izq=m+1
    
    
    timeEnd=MPI.Wtime()             # Termina la ejecucion

    # Comprueba si esta ordenado
    if encontrado != -1: print("El valor ESTA en la posicion:", encontrado, "del array")
    else: print("Array NO ESTA en el array")

    print("Tiempo de ejecucion:", ((timeEnd-timeStart)))

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
    path=os.path.join(dir, ".otros","ficheros","1_Array", carpeta, archivo+".txt")
    #print(path)
       
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
        if (a[i]<a[i-1]):return False
    
    return True


main()