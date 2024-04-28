from mpi4py import MPI
import sys
import os

def bubble_sort1(a):
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:   
                tmp = a[j]
                a[j] = a[j + 1]
                a[j + 1] = tmp

def bubble_sort2(a):
    n=len(a)
    for i in range(n-1):
        for j in range(n-1-i):
            if a[j]>a[j+1]:   
                tmp=a[j]
                a[j]=a[j+1]
                a[j+1]=tmp



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
    archivo="10000Desc"    
    a,n=leeArchivo(archivo,None)
    print("Array Generado.")
    
    tiempo1=0
    tiempo2=0
    repeticiones=20
    for i in range(repeticiones):
        b=[]
        for val in a:
            b.append(val)
        
        timeStart=MPI.Wtime()
        bubble_sort1(b) # ,0,len(a)-1
        timeEnd=MPI.Wtime()
        
        if arrayOrdenado(b,n): 
            #print("Array Ordenado")
            tiempo1+=timeEnd-timeStart
        else : 
            print("Array NO ordenado") 
            break

        b=[]
        for val in a:
            b.append(val)


        timeStart=MPI.Wtime()
        bubble_sort2(b) # ,0,len(a)-1
        timeEnd=MPI.Wtime()
        print("Tiempo de ejecucion: {}".format(timeEnd-timeStart))
        
        if arrayOrdenado(b,n): 
            #print("Array Ordenado")
            tiempo2+=timeEnd-timeStart
        else : 
            print("Array NO ordenado") 
            break
    tiempo1/=repeticiones
    tiempo2/=repeticiones
    print("1. Tiempo medio ({}) = {}".format(repeticiones,tiempo1))
    print("2. Tiempo medio ({}) = {}".format(repeticiones,tiempo2))





main()