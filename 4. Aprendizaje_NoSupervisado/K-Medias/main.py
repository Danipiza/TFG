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
    def __init__(self, k, vals, print):
        self.k = k
        self.poblacion=vals
        self.n=len(vals)
        self.print=print
        

    def ejecuta(self):
        # Inicializa centros
        dic={}
        centroides=[]
        for i in range(self.k):
            while True:
                rand = random.randint(0, self.n - 1)
                if rand not in dic:
                    centroides.append(self.poblacion[rand])                
                    dic[rand] = 1
                    break

        
        asignacion=[-1 for i in range(self.n)]
        while True:
            # Fase de asginacion
            for i in range(self.n):
                tmp=-1
                cluster=-1
                dist=float('inf')
                for j in range(self.k):
                    #print(self.poblacion[i])
                    #print(centroides[j])
                    tmp=self.distancia(self.poblacion[i], centroides[j])
                    if dist>tmp:
                        dist=tmp
                        cluster=j
                asignacion[i]=cluster

            # Actualiza el los centros
            indsCluster=[0 for _ in range(self.k)]
            centroidesNuevos=[0 for _ in range(self.k)]
            for i in range(self.n):
                centroidesNuevos[asignacion[i]]+=self.poblacion[i]
                indsCluster[asignacion[i]]+=1

            if self.print==True:
                print("Poblacion:",self.poblacion)
                print("Centroides:",centroides)
                print("indsClusters:",indsCluster)
            for i in range(self.k):               
                centroidesNuevos[i]/=indsCluster[i]
            
            if self.print==True: print("Nuevos Centroides:",centroidesNuevos)
            if(self.compara_centros(centroides,centroidesNuevos)): break
            centroides=centroidesNuevos

        return asignacion

        
    def compara_centros(self, a, b):
        n=len(a)
        for i in range(n):
            if a[i]!=b[i]: return False
        
        return True

    # Manhattan
    def distancia(self,a,b):
        return abs(a-b)# + abs(a[1]-b[1])
    

poblacion,n=leeArchivo("10000")
#print(poblacion)
#poblacion=[1, 2, 4, 5, 11, 12, 14, 15, 19, 20, 20.5, 21]




for k in range(1,19):
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

