from mpi4py import MPI
import sys
import os

INF=sys.maxsize


def main():
   
    timeStart=0.0           # double.
    timeEnd=0.0
   
    a=[]                    # int[]. Entrada
    n=0                     # int.   Tamaño de los arrays                           
    i=0        
    enc=False
    
    a,n=leeArchivo() 
    val = int(input("Introduce valor a buscar: "))
   
              

    timeStart=MPI.Wtime()

    while i<n:
        if a[i]==val: break
        i+=1
    
    timeEnd=MPI.Wtime()

       
    print("Tiempo de ejecucion:", ((timeEnd-timeStart)))
    if enc==True: print("Valor,",val,"Encontrado")
    else: print("Valor", val, "No esta en el array")

    return 0



# TODO COMPROBAR SI FUNCIONA
def leeArchivo():
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    nombre_fichero=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","No_Ordenado", nombre_fichero+".txt")
    
       
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


 



main()