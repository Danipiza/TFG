from mpi4py import MPI
import sys
import os
import signal
import time

# N:100000 ordenados de manera descendente
# BubbleSort:           517.9079863999978s
# InsertionSort:        339.88781240000026s
# SelectionSort:        141.95964079999976s    
# SequentialSort:       429.5713084000017s
# MPI SequentialSort:   50.1617846100001s 

# Signal handler 
def signal_handler(sig, frame):
    print("Ctrl+C, almacenando en ")
    guarda_datos(["BubbleSort.txt","InsertionSort.txt","SelectionSort.txt","SequentialSort.txt",
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
    with open(archivo[1], 'w') as file:
        for i, val in enumerate(datos[1]):
            file.write("{}, ".format(val))
        file.write("\n")
    with open(archivo[2], 'w') as file:
        for i, val in enumerate(datos[2]):
            file.write("{}, ".format(val))
        file.write("\n")
    with open(archivo[3], 'w') as file:
        for i, val in enumerate(datos[3]):
            file.write("{}, ".format(val))
        file.write("\n")
    
    with open(archivo[4], 'w') as file:
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
datos=[[] for _ in range(4)]
# Crear handler para SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

a,n=leeArchivo("100000Desc",None)
#a,n=leeArchivo("100Desc",None)
print("Array Generado.")

"""print(a)
selection_sort(a)
print(a)
if arrayOrdenado(a,len(a)):            
    print("Ordenado")
else : print("Array NO ordenado") """
#20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 
procesar=[64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]


try:
    for x in procesar:  
        tamArray.append(x)

        b=[]
        for val in a[0:x+1]:
            b.append(val)
        
        timeStart=MPI.Wtime()
        bubble_sort(b)
        timeEnd=MPI.Wtime()            
        print("1. {}: {}".format(x,(timeEnd-timeStart)),end=" ")        
        if arrayOrdenado(b,len(b)):            
            datos[0].append(timeEnd-timeStart)
        else : print("Array NO ordenado en {}".format(x))   

        # --------------------------------------------------------------
        b=[]
        for val in a[0:x+1]:
            b.append(val)

        timeStart=MPI.Wtime()
        insertion_sort(b)
        timeEnd=MPI.Wtime()            
        print("2. {}: {}".format(x,(timeEnd-timeStart)),end=" ")        
        if arrayOrdenado(b,len(b)): 
            datos[1].append(timeEnd-timeStart)
        else : print("Array NO ordenado en {}".format(x)) 

        # --------------------------------------------------------------
        b=[]
        for val in a[0:x+1]:
            b.append(val)

        timeStart=MPI.Wtime()
        selection_sort(b)
        timeEnd=MPI.Wtime()            
        print("3. {}: {}".format(x,(timeEnd-timeStart)),end=" ")        
        if arrayOrdenado(b,len(b)): 
            datos[2].append(timeEnd-timeStart)
        else : print("Array NO ordenado en {}".format(x)) 

        # --------------------------------------------------------------
        b=[]
        for val in a[0:x+1]:
            b.append(val)

        timeStart=MPI.Wtime()
        b=sequential_sort(b)
        timeEnd=MPI.Wtime()            
        print("4. {}: {}".format(x,(timeEnd-timeStart)),end=" ")        
        if arrayOrdenado(b,len(b)):             
            datos[3].append(timeEnd-timeStart)
        else : 
            print(b)
            time.sleep(2)
            print("SELECTION Array NO ordenado en {}".format(x)) 


    print("FIN DE TODOS -----------------------")
    while True:
        i=0
except KeyboardInterrupt:
    print('\nProgram interrupted, storing processed array in a file...')
    guarda_datos(["BubbleSort.txt","InsertionSort.txt","SelectionSort.txt","SequentialSort.txt",
                  "TamArray.txt"])
    sys.exit(0)



#main()