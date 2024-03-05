from mpi4py import MPI
import sys
import os

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

def leeArchivo():
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    tfg_directorio=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))    
    nombre_fichero=input("Introduce un nombre del fichero: ")    
    path=os.path.join(tfg_directorio, ".Otros","ficheros","Ordenados", nombre_fichero+"Desc.txt")
    
       
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
        print("El archivo '{}' no existe.".format(nombre_fichero+".txt"))
    
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
    a,n=leeArchivo()
    print("Array Generado.")
    timeStart=MPI.Wtime()
    quick_sort(a,0,len(a)-1)
    timeEnd=MPI.Wtime()
    print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
    if arrayOrdenado(a,n): print("Array Ordenado")
    else : print("Array NO ordenado")

main()