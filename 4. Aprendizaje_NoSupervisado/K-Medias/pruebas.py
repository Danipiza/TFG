import sys
import os

"""a=[1,2,3,4,5]
b=[6,7,8,9,10]

for x in b:
    a.append(x)
"""
def leeArchivo(archivo):
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    tfg_directorio=os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))
    
    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(tfg_directorio, ".Otros","ficheros","Agrupar", archivo+".txt")
       
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

vals,n=leeArchivo("1000")
poblacion=[[x] for x in vals]
print(poblacion)