from mpi4py import MPI
import sys
import os

# COMPILAR
# py .\sequentialSort.py

# Este programa inicialmente tiene (np-1) workers. Pasa por un preprocesado para 
#   tener potencias de 2 workers, haciendo una aproximacion hacia abajo de la ultima
#   potencia alcanzada

# Este programa combina los algoritmos de SelectionSort y MergeSort. 
# Cada worker se encarga primero de ordenar por el metodo de SelectionSort la parte del array recibida 
#   del master. Una vez esta ordenado empieza el proceso de intercambio de mensajes entre workers. 
# El master indica a cada worker que tienen que hacer. 
#   - Si reciben un identificador mayor a su id, tienen que esperar a recibir un array de otro worker, para 
#       ordenar y almacenar ambos arrays (el suyo y el recibido). 
#   - Si reciben un identificador menor a su id, tienen que enviar su array ordenado al worker con ese identificador
#       y terminar su ejecucion.
# Con cada iteracion el master reduce el numero de workers hasta que solo quede uno, y este envie al master
#   el array entero ordenado.

def main():
    INF=sys.maxsize         # int. Variable infinito con el maximo valor de int

    timeStart=0.0           # double. Para medir el tiempo de ejecucion
    timeEnd=0.0
   
    a=[]                    # int[]. Array Entrada
    b=[]                    #        Array Salida          
    n=0                     # int.   Tamaño de los arrays                           
    
    a,n=leeArchivo("1000",None)                # Lee el archivo devolviendo el array y su tamaño
    # Inicializa el array de salida a valores INF para saber que espacios estan ocupados
    b=[(INF) for i in range(n)]     
              

    timeStart=MPI.Wtime()           # Comienza el Algoritmo

    # Recorre cada elemento del array
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
    
    timeEnd=MPI.Wtime()             # Termina la ejecucion

    # Comprueba si esta ordenado
    if arrayOrdenado(b,n): print("Array ordenado")
    else: print("Array NO ordenado")

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
    a: int[]        El array a comprobar
    n: int          Tamaño del array

    return => bool  True or False
    """

    for i in range(1,n):    
        if (a[i]<a[i-1]):return False
    
    return True



main()