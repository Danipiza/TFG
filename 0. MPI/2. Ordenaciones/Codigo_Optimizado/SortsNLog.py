from mpi4py import MPI
import sys
import os
from collections import deque
import random


# N:100000 ordenados de manera descendente
# QuickSort:            RecursionError: maximum recursion depth exceeded in comparison
# MergeSort:            20.67818360000092s
# MergeSortMPI:         1.149167099996702s


def particion(a, izq, der):
    pivote = a[der]
    posPivote = der
    der -= 1
    eIzq = a[izq]
    eDer = a[der]
    tmp = 0
    while izq < der:
        while eIzq < pivote:
            izq += 1
            eIzq = a[izq]
        while eDer > pivote and izq < der:
            der -= 1
            eDer = a[der]
        if izq < der:
            # swap
            tmp = a[izq]
            a[izq] = a[der]
            a[der] = tmp
            # aumenta los punteros
            izq += 1
            eIzq = a[izq]
            der -= 1
            eDer = a[der]
            if izq == der:
                izq += 1
    # swap
    a[posPivote] = a[izq]
    a[izq] = pivote
    return izq

def quick_sort(a, izq, der):
    izqTemp=izq
    derTemp=der   

    if izq < der:
        pivote = a[derTemp]
        posPivote = derTemp
        derTemp -= 1
        eIzq = a[izqTemp]
        eDer = a[derTemp]
        tmp = 0
        while izqTemp < derTemp:
            while eIzq < pivote:
                izqTemp += 1
                eIzq = a[izqTemp]
            while eDer > pivote and izqTemp < derTemp:
                derTemp -= 1
                eDer = a[derTemp]
            if izqTemp < derTemp:
                # swap
                tmp = a[izqTemp]
                a[izqTemp] = a[derTemp]
                a[derTemp] = tmp
                # aumenta los punteros
                izqTemp += 1
                eIzq = a[izqTemp]
                derTemp -= 1
                eDer = a[derTemp]
                if izqTemp == derTemp:
                    izqTemp += 1
        # swap
        a[posPivote] = a[izqTemp]
        a[izqTemp] = pivote
        pInd= izqTemp
        
        quick_sort(a, izq, pInd - 1)
        quick_sort(a, pInd + 1, der)






# Convertir subarbol en monticulo
def heap_aux(a, n, nodo):
    mayor=nodo  # nodo raiz como el mayor
    i=2*nodo+1
    j=2*nodo+2
    
    # HijIzq existe y es mayor
    if i<n and a[i]>a[mayor]: mayor=i
    
    # HijDer existe y es mayor
    if j<n and a[j]>a[mayor]: mayor=j
    
    # Mayor!=raiz
    tmp=None
    if mayor!=nodo:
        tmp=a[nodo]
        a[nodo]=a[mayor]
        a[mayor]=tmp        
        heap_aux(a, n, mayor)  # Subarbol afectado

def heap_sort(a, n):       
    # Monticulo de maximos
    for i in range(n//2-1,-1,-1):
        heap_aux(a, n, i)
    
    
    tmp=None
    for i in range(n-1,0,-1): # Extraer elementos 
        tmp=a[0]
        a[0]=a[i]
        a[i]=tmp        
        heap_aux(a, i, 0)  


def counting_sort(a, exp):
    n=len(a)

    ret = [0 for _ in range(n)]
    count = [0 for _ in range(10)] # Array para contar la frecuencia de cada dígito
    
    # Frecuencia de cada digito
    for i in range(n):
        index=a[i]//exp
        count[index%10]+=1
    
    # Posicion actual de cada digito
    for i in range(1, 10):
        count[i]+=count[i-1]
    
    
    i=n-1
    while i>=0: # Construir el array de salida
        index=a[i]//exp
        ret[count[index%10]-1]=a[i]
        count[index%10]-=1
        i-=1
    
    # Copiar el array de salida 
    for i in range(n):
        a[i]=ret[i]

def radix_sort(a):
    maxDigs=0 # maximo numero de digitos en el array
    for x in a:
        if maxDigs<x: maxDigs=x    
    #max_num = max(arr)
    
    # Aplicar Counting Sort para cada digito. 
    exp=1
    while maxDigs//exp>0:
        counting_sort(a, exp)
        exp*=10


def merge(a, izq, m, der):
    i = izq
    j = m + 1
    k = izq
    aux = [0] * len(a)
    for i in range(izq, der+1):
        aux[i] = a[i]
    
    i = izq
    while i <= m and j <= der:
        if aux[i] <= aux[j]:
            a[k] = aux[i]
            i += 1
        else:
            a[k] = aux[j]
            j += 1
        k += 1

    while i <= m:
        a[k] = aux[i]
        k += 1
        i += 1
    while j <= der:
        a[k] = aux[j]
        k += 1
        j += 1

def merge_sort(a, izq, der):
    if izq < der:
        m = (izq + der) // 2
        merge_sort(a, izq, m)
        merge_sort(a, m+1, der)
        merge(a, izq, m, der)

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
    a: int[]        El array a comprobar
    n: int          Tamaño del array

    return => bool  True or False
    """

    for i in range(1,n):    
        if (a[i]<a[i-1]):return False
    
    return True

def main():
    #a,n=leeArchivo("100000Desc",None)
    n=1000000
    a=[i for i in range(n,-1,-1)]
    
    #a = [random.randint(1, 100) for _ in range(n)]
    print("Array Generado.")
    timeStart=MPI.Wtime()
    merge_sort(a,0,len(a)-1)
    #a=sorted(a)
    #a.sort()
    #heap_sort(a,n)
    #radix_sort(a)
    timeEnd=MPI.Wtime()
    print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
    if arrayOrdenado(a,n): print("Array Ordenado")
    else : print("Array NO ordenado")

main()