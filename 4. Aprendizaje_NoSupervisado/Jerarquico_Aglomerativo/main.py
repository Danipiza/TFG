from mpi4py import MPI
import random
import os
import math

def leeArchivo(archivo):
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    tfg_directorio=os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))
    
    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(tfg_directorio, ".Otros","ficheros","No_Ordenado", archivo+".txt")
       
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

class KMeans:
    def __init__(self, vals, print):
        self.poblacion=vals
        self.n=len(vals)
        self.print=print
        

    def ejecuta(self):
        # FASE1: Inicializa Matriz de distancias
        M=[]
        tmp=[]
        for i in range(self.n):
            for j in range(i+1,self.n):
                tmp.append(self.distancia(self,poblacion[i],self.poblacion[j]))
            M.append(tmp)

        # FASE2: 
        distMin=float("inf")
        c1,c2=None,None
        for k in range(self.n-1):
            # Elegir los 2 cluster mas cercanos
            for i in range(self.n):
                for j in range(1,self.n-i):
                    if distMin>M[i][j]: 
                        distMin=M[i][j]
                        c1=i
                        c2=j
                

        

        
        

        
    

    # Manhattan
    def distancia(self,a,b):
        return abs(a-b)# + abs(a[1]-b[1])
    

#poblacion,n=leeArchivo("10000")
#print(poblacion)
poblacion=[1, 2, 4, 5, 11, 12, 14, 15, 19, 20, 20.5, 21]




"""for k in range(1,19):
    kM=KMeans(k, poblacion, False)
    ret=0
    timeStart=MPI.Wtime()
    for i in range(100):
        asignacion=kM.ejecuta()
        maxC=[(-float('inf')) for _ in range(k)]
        minC=[(float('inf')) for _ in range(k)]
        for j in range(n):
            if maxC[asignacion[j]]<poblacion[j]: maxC[asignacion[j]]=poblacion[j]
            if minC[asignacion[j]]>poblacion[j]: minC[asignacion[j]]=poblacion[j]
        tmp=0
        for j in range(k):
            tmp+=maxC[j]-minC[j]
        if ret<tmp: ret=tmp

    timeEnd=MPI.Wtime()
        
    print("Tiempo de ejecucion:",(timeEnd-timeStart))
    print("Mejor Resultado:",ret)
"""