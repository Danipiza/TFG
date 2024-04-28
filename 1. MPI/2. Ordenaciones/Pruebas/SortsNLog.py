from mpi4py import MPI
import sys
import os
import signal
import time



# Signal handler 
def signal_handler(sig, frame):
    print("Ctrl+C, almacenando en ")
    guarda_datos(["MergeSort.txt",#"QuickSort.txt",
                  "TamArray.txt"])
    sys.exit(0)

def guarda_datos(archivo):    
    print(tamArray)
    for x in datos:
        print(x,"\n")
    

    with open(archivo[0], 'w') as file:
        for i, val in enumerate(datos[0]):
            file.write("{}, ".format(val))
        file.write("\n")
    """with open(archivo[1], 'w') as file:
        for i, val in enumerate(datos[1]):
            file.write("{}, ".format(val))
        file.write("\n")"""
    
    
    with open(archivo[1], 'w') as file:
        for i, val in enumerate(tamArray):
            file.write("{}, ".format(val))
        file.write("\n")
 

def quick_sort(a, izq, der):
    izqTemp=izq
    derTemp=der   
    # PARTICION
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
    #
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
    a: int[]    El array a comprobar
    n: int      Tamaño del array
    return.     True or False
    """
    for i in range(1,n):    
        if (a[i]<a[i-1]):return False
    
    return True

#def main():

tamArray=[]
datos=[[] for _ in range(1)]
# Crear handler para SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

a,n=leeArchivo("100000Desc",None)
#a,n=leeArchivo("100Desc",None)
print("Array Generado.")
"""b=a[0:21]
quick_sort(b,0,len(b)-1)
if arrayOrdenado(b,len(b)):
    print("ordenado")
else:
    print("no ordenado",b)"""

"""print(a)
selection_sort(a)
print(a)
if arrayOrdenado(a,len(a)):            
    print("Ordenado")
else : print("Array NO ordenado") """
#
procesar=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]

fin=True
try:
    for x in procesar:  
        tamArray.append(x)

        b=[]
        for val in a[0:x+1]:
            b.append(val)
        
        timeStart=MPI.Wtime()
        merge_sort(b,0,len(b)-1)
        timeEnd=MPI.Wtime()            
        print("1. {}: {}".format(x,(timeEnd-timeStart)),end=" ")        
        if arrayOrdenado(b,len(b)):            
            datos[0].append(timeEnd-timeStart)
        else : print("Array NO ordenado en {}".format(x))   

        # --------------------------------------------------------------
        """if fin:
            b=[]
            for val in a[0:x+1]:
                b.append(val)

            timeStart=MPI.Wtime()
            try:
                quick_sort(b,0,len(b)-1)
                timeEnd=MPI.Wtime()            
                print("2. {}: {}".format(x,(timeEnd-timeStart)),end=" ")        
                if arrayOrdenado(b,len(b)): 
                    datos[1].append(timeEnd-timeStart)
                else : print("Array NO ordenado en {}".format(x)) 
            except Exception:
                print("SELECTION NO PUEDE CON TAM=",x)
                fin=False"""
            

        


    print("FIN DE TODOS -----------------------")
    while True:
        i=0
except KeyboardInterrupt:
    print('\nProgram interrupted, storing processed array in a file...')
    guarda_datos(["MergeSort.txt",#"QuickSort.txt",
                  "TamArray.txt"])
    sys.exit(0)



#main()