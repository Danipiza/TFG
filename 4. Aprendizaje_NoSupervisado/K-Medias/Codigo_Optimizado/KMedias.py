import matplotlib.pyplot as plt
from mpi4py import MPI
import random
import os
import math

# TIEMPO: (datos=100000.txt, k=3)
# Manhattan:
# (ejecuta_uno) Tiempo de ejecucion: 2.326730199973099
# (ejecuta_varios, 5) Tiempo de ejecucion: 10.411191000021063

# Euclidea:
# (ejecuta_uno) Tiempo de ejecucion: 2.9821161999716423
# (ejecuta_varios, 5) Tiempo de ejecucion: 13.842410599987488

class KMeans:
    def __init__(self, k, vals, print):
        self.k = k
        self.poblacion=vals
        self.d=len(vals[0])
        self.n=len(vals)
        self.print=print
        
        

    def ejecutaM(self):
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
                    tmp=self.manhattan(self.poblacion[i], centroides[j])
                    if dist>tmp:
                        dist=tmp
                        cluster=j
                asignacion[i]=cluster

            # Actualiza el los centros
            indsCluster=[0 for _ in range(self.k)]
            centroidesNuevos=[[0 for _ in range(self.d)] for _ in range(self.k)]
            for i in range(self.n):
                for j in range(self.d):
                    centroidesNuevos[asignacion[i]][j]+=self.poblacion[i][j]
                indsCluster[asignacion[i]]+=1

            if self.print==True:
                print("Poblacion:",self.poblacion)
                print("Centroides:",centroides)
                print("indsClusters:",indsCluster)
            for i in range(self.k): 
                for j in range(self.d):              
                    centroidesNuevos[i][j]/=indsCluster[i]
            
            if self.print==True: print("Nuevos Centroides:",centroidesNuevos)
            if(self.compara_centros(centroides,centroidesNuevos)): break
            centroides=centroidesNuevos

        return asignacion
    

    def ejecutaE(self):
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
                    tmp=self.euclidea(self.poblacion[i], centroides[j])
                    if dist>tmp:
                        dist=tmp
                        cluster=j
                asignacion[i]=cluster

            # Actualiza el los centros
            indsCluster=[0 for _ in range(self.k)]
            centroidesNuevos=[[0 for _ in range(self.d)] for _ in range(self.k)]
            for i in range(self.n):
                for j in range(self.d):
                    centroidesNuevos[asignacion[i]][j]+=self.poblacion[i][j]
                indsCluster[asignacion[i]]+=1

            if self.print==True:
                print("Poblacion:",self.poblacion)
                print("Centroides:",centroides)
                print("indsClusters:",indsCluster)
            for i in range(self.k): 
                for j in range(self.d):              
                    centroidesNuevos[i][j]/=indsCluster[i]
            
            if self.print==True: print("Nuevos Centroides:",centroidesNuevos)
            if(self.compara_centros(centroides,centroidesNuevos)): break
            centroides=centroidesNuevos

        return asignacion

        
    def compara_centros(self, a, b):
        n=len(a)
        for i in range(n):
            for j in range(self.d):
                if a[i][j]!=b[i][j]: return False
        
        return True

    # Manhattan
    def manhattan(self,a,b):
        ret=0.0
        for i in range(len(a)):
            ret+=abs(a[i]-b[i])
        return ret
    
    def euclidea(self, a,b):
        ret=0.0
        for i in range(len(a)):
            ret+=(a[i]-b[i])**2        
        
        return math.sqrt(ret)


"""Naranja esta implementado para varias dimensiones"""
def plot2D(points,asignacion,k):
    colors=["blue","red","green","black","pink","yellow"]
    n=len(points)
    d=len(points[0])

    x=[[]for _ in range(k)]
    y=[[]for _ in range(k)]
    """coords=[[] for _ in range(k)]"""
    for i in range(n):
        """coords[asignacion[i]].append(points[i])"""
        x[asignacion[i]].append(points[i][0])
        y[asignacion[i]].append(points[i][1])
    #print(coords[0])
    
    ret=0.0    
    for i in range(k): # Recorre clusters
        m=len(x[i])

        tmp=[[float("inf"),-float("inf")] for _ in range(d)]
        """tmpY=[[float("inf"),-float("inf")] for _ in range(k)]"""
        
        for j in range(m): # Recorre individuos del cluster
            """for a in range(d): # Recorre sus dimensiones                
                if coords[i][j][a]<tmp[a][0]: tmp[a][0]=coords[i][j][a]     # min
                elif coords[i][j][a]>tmp[a][1]: tmp[a][1]=coords[i][j][a]   # max"""
            if x[i][j]<tmp[0][0]: tmp[0][0]=x[i][j]     # min
            elif x[i][j]>tmp[0][1]: tmp[0][1]=x[i][j]   # max
            
            if y[i][j]<tmp[1][0]: tmp[1][0]=y[i][j]     # min
            elif y[i][j]>tmp[1][1]: tmp[1][1]=y[i][j]   # max
        
        for a in range(d):            
            ret+=abs(tmp[a][0]-tmp[a][1])
            
    print("Valor:",ret)

    for i in range(k):
        plt.scatter(x[i], y[i], color=colors[i])
    
        
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2D-Plot Leida')
    
    plt.show()



def lee(archivo):
    with open(archivo, 'r') as file:
        content = file.read()

    array = []

    # Quita " " "," "[" y "]. Y divide el archivo     
    datos = content.replace('[', '').replace(']', '').split(', ')      
    for i in range(0, len(datos), 2):
        x = float(datos[i])
        y = float(datos[i + 1])

        array.append([x, y])

    #print("\n",array)        
    
    return array

def leeArchivo(archivo):
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    tfg_directorio=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))
    
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




def ejecuta_uno(poblacion, k, tipo):
    timeStart=MPI.Wtime()   
    
    kM=KMeans(k, poblacion, False)
    if tipo==0: asignacion=kM.ejecutaM()
    else: asignacion=kM.ejecutaE()    
    timeEnd=MPI.Wtime()
    
    #print(asignacion)
    print("Tiempo de ejecucion:",(timeEnd-timeStart))
    return asignacion

def ejecuta_varios(poblacion, k, times,tipo):
    timeStart=MPI.Wtime()
    if tipo==0: 
        for _ in range(times):
            kM=KMeans(k, poblacion, False)
            asignacion=kM.ejecutaM()
    else: 
        for _ in range(times):
            kM=KMeans(k, poblacion, False)
            asignacion=kM.ejecutaE()
    
    
    timeEnd=MPI.Wtime()
    
    #print(asignacion)
    print("Tiempo de ejecucion:",(timeEnd-timeStart))
    
def ejecuta_busquedaM(poblacion, maxCluster, n):
    d=len(poblacion[0])
    for k in range(1,maxCluster+1):
        kM=KMeans(k, poblacion, False)

        ret=0 #[0 for _ in range(d)]
        timeStart=MPI.Wtime()
        for i in range(100):
            asignacion=kM.ejecutaM()
            maxC=[[(-float('inf')) for _ in range(d)] for _ in range(k)]
            minC=[[(float('inf')) for _ in range(d)] for _ in range(k)]
            for j in range(n):
                for a in range(d):
                    if maxC[asignacion[j]][a]<poblacion[j][a]: maxC[asignacion[j]][a]=poblacion[j][a]
                    if minC[asignacion[j]][a]>poblacion[j][a]: minC[asignacion[j]][a]=poblacion[j][a]
            tmp=0 #[0 for _ in range(d)]
            for j in range(k):
                for a in range(d):
                    tmp+=maxC[j][a]-minC[j][a]
            if ret<tmp: ret=tmp

        timeEnd=MPI.Wtime()
            
        print("Tiempo de ejecucion:",(timeEnd-timeStart))
        print("Mejor Resultado:",ret)

def ejecuta_busquedaE(poblacion, maxCluster, n):
    d=len(poblacion[0])
    for k in range(1,maxCluster+1):
        kM=KMeans(k, poblacion, False)

        ret=0 #[0 for _ in range(d)]
        timeStart=MPI.Wtime()
        for i in range(100):
            asignacion=kM.ejecutaE()
            maxC=[[(-float('inf')) for _ in range(d)] for _ in range(k)]
            minC=[[(float('inf')) for _ in range(d)] for _ in range(k)]
            for j in range(n):
                for a in range(d):
                    if maxC[asignacion[j]][a]<poblacion[j][a]: maxC[asignacion[j]][a]=poblacion[j][a]
                    if minC[asignacion[j]][a]>poblacion[j][a]: minC[asignacion[j]][a]=poblacion[j][a]
            tmp=0 #[0 for _ in range(d)]
            for j in range(k):
                for a in range(d):
                    tmp+=maxC[j][a]-minC[j][a]
            if ret<tmp: ret=tmp

        timeEnd=MPI.Wtime()
            
        print("Tiempo de ejecucion:",(timeEnd-timeStart))
        print("Mejor Resultado:",ret)

def main():
    poblacion=lee("6000.txt")
    k=4
    #print(poblacion)
    #a,n=leeArchivo("100000")
    #poblacion=[[x] for x in a]
    #print(poblacion)
    #poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0], [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]

    asignacion=ejecuta_uno(poblacion, k, 0)
    #ejecuta_varios(poblacion, 3, 5, 1)
    #ejecuta_busquedaM(poblacion, 2, n)
    #ejecuta_busquedaE(poblacion, 2, n)

    plot2D(poblacion,asignacion,k)



main()