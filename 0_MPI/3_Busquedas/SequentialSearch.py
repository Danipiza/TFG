from mpi4py import MPI
import sys
import os

# EJECUTAR
# py SequentialSearch.py

"""
Busqueda secuencial de un elemento.

Recorre un array completo buscando el entero escrito por la terminal
"""


def main():
   
    timeStart=0.0           # double.
    timeEnd=0.0
   
    a=[]                    # int[]. Entrada
    n=0                     # int.   Tamaño de los arrays                           
    i=0        
    enc=False
    
    a,n=leeArchivo("100",None) 
    val = int(input("Introduce valor a buscar: "))
   
              

    timeStart=MPI.Wtime()

    while i<n:
        if a[i]==val: 
            enc=True
            break
        i+=1
    
    timeEnd=MPI.Wtime()

       
    print("Tiempo de ejecucion:", ((timeEnd-timeStart)))
    if enc==True: print("Valor,",val,"Encontrado")
    else: print("Valor", val, "No esta en el array")

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

 



main()