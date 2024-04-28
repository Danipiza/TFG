from mpi4py import MPI
import sys
import os

# COMPILAR
# py .\binarySort.py
def guarda_datos(archivo,datos,tamDatos):    
    
    

    with open(archivo[0], 'w') as file:
        for i, val in enumerate(datos):
            file.write("{}, ".format(val))
        file.write("\n")
    with open(archivo[1], 'w') as file:
        for i, val in enumerate(tamDatos):
            file.write("{}, ".format(val))
        file.write("\n")


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

        
    a,n=leeArchivo("100000",None)                # Lee el archivo devolviendo el array y su tamaño        
    if not arrayOrdenado(a,n): 
        print("Array tiene que estar ordenado")
        exit(0)
    
    der=n-1    
    
              
    datos=[]
    tamDatos=[]
    procesar=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]
    for x in procesar:
        encontrado=-1
        val=a[x-1]
        izq=0
        der=x-1
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
        if encontrado==-1: print(x," ->  Valor", val, "No esta en el array")
        else:
            print("Tiempo de ejecucion:", ((timeEnd-timeStart)))
            datos.append((timeEnd-timeStart))
            tamDatos.append(x)
            guarda_datos(["BinarySearch.txt","TamDatos.txt"],datos,tamDatos)

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


main()