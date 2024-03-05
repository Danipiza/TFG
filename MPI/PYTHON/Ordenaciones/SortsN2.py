from mpi4py import MPI
import sys
import os
import signal

# N:100000 ordenados de manera descendente
# BubbleSort:           517.9079863999978s
# InsertionSort:        339.88781240000026s
# SelectionSort:        141.95964079999976s    
# SequentialSort:       429.5713084000017s
# MPI SequentialSort:   50.1617846100001s 

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


# Signal handler 
def signal_handler(sig, frame):
    print("Ctrl+C, almacenando en ")
    guarda_datos("merge_sort_2.txt")
    sys.exit(0)

def guarda_datos(archivo):
    print(datos)
    print(tamArray)
    with open(archivo, 'w') as file:
        for i, val in enumerate(datos):
            file.write("{}, ".format(val))
        file.write("\n")
        for i, val in enumerate(tamArray):
            file.write("{}, ".format(val))
        file.write("\n")

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

def sequential_sort(a):
    INF=sys.maxsize   
    n=len(a)
    b=[(INF) for i in range(n)]        
    for i in range(n):
        cont=0
        val=a[i]
        for i in range(n):  
            if a[i]<val: cont+=1        
        while b[cont]!=INF: cont+=1
        b[cont]=val
    return b




def leeArchivo(archivo):
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    tfg_directorio=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))    
    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(tfg_directorio, ".Otros","ficheros","Ordenados", archivo+"Desc.txt")
    
       
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

#def main():

tamArray=[]
datos=[]
# Crear handler para SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

a,n=leeArchivo("100000")
print("Array Generado.")

#procesar=[1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]
#procesar=[95000, 96000, 97000, 98000, 99000, 100000] # Selection
procesar=[68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]
try:
    for x in procesar:
        
        b=a[0:x+1]
        print("Valor inicial {}".format(b[0]),end=" ")
        timeStart=MPI.Wtime()
        merge_sort(b,0,len(b)-1)
        timeEnd=MPI.Wtime()
        print("Tiempo de ejecucion para x={}: {}".format(x,(timeEnd-timeStart)))
        if arrayOrdenado(b,len(b)): 
            tamArray.append(x)
            datos.append(timeEnd-timeStart)
        else : print("Array NO ordenado en {}".format(x))   
    print("FIN DE TODOS -----------------------")
    while True:
        i=0
except KeyboardInterrupt:
    print('\nProgram interrupted, storing processed array in a file...')
    guarda_datos("merge_sort_2.txt")
    sys.exit(0)



#main()