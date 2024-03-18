from mpi4py import MPI
import sys
import os

# N:100000 ordenados de manera descendente
# BubbleSort:           517.9079863999978s
# InsertionSort:        339.88781240000026s
# SelectionSort:        141.95964079999976s    
# SequentialSort:       429.5713084000017s
# MPI SequentialSort:   50.1617846100001s 

def bubble_sort(a):
    n = len(a)
    for i in range(n-1):
        for j in range(n-1-i):
            if a[j] > a[j+1]:   
                tmp = a[j]
                a[j] = a[j+1]
                a[j+1] = tmp

def insertion_sort(a):
    n = len(a)
    for i in range(1, n):
        if a[i-1] > a[i]:                
            pos=i
            tmp = a[pos]
            while pos > 0 and tmp < a[pos-1]:
                a[pos] = a[pos-1]
                pos -= 1
            a[pos] = tmp

def selection_sort(a):
    n = len(a)
    minE = 0
    pos = 0
    for i in range(n-1):
        minE = a[i]
        pos = i
        for j in range(i+1, n):
            if minE > a[j]:
                minE = a[j]
                pos = j            
        tmp = a[i]
        a[i] = a[pos]
        a[pos] = tmp

# Recorre el array N veces (1 por cada elemento) recorriendo el array de izquierda a derecha, 
#   comparando el valor actual con todo el array, para que cuando termine, colocarlo en que posición del array ordenado.
def sequential_sort(a):
    INF=sys.maxsize   
    n=len(a)
    b=[(INF) for i in range(n)]        
    for i in range(n):
        cont=0
        val=a[i]
        # Compara el elemento actual con todos para saber en que posicion ponerlo
        for i in range(n):  
            if a[i]<val: cont+=1
        # Termina una ejecucion y lo pone en su sitio. 
        # Si esta ocupado es porque hay un valor duplicado, por lo que busca el siguiente
        while b[cont]!=INF: cont+=1
        b[cont]=val
    return b




def leeArchivo(archivo):
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    tfg_directorio=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))))
    if archivo==None: archivo=input("Introduce un nombre del fichero: ")  
    path=os.path.join(tfg_directorio, ".Otros","ficheros","Ordenado", archivo+"Desc.txt")
    
       
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
        print("El archivo '{}' no existe.".format(archivo+"Desc.txt"))
    
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

def main():
    #a,n=leeArchivo(archivo=None)
    archivo="1000"

    #for i in range
    
    a,n=leeArchivo(archivo)
    print("Array Generado.")
    
    timeStart=MPI.Wtime()
    bubble_sort(a) # ,0,len(a)-1
    timeEnd=MPI.Wtime()
    print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
    if arrayOrdenado(a,n): print("Array Ordenado")
    else : print("Array NO ordenado")





main()