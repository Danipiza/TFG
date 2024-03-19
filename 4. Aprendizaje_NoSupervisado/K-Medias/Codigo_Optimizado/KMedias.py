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

        return asignacion,centroides
    

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

        return asignacion,centroides

        
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
def plot2D(poblacion,asignacion,k):
    #['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
    colors=['blue','red','green','black','pink','yellow','magenta','brown','darkgreen','gray','fuchsia','violet','salmon','darkturquoise','forestgreen','firebrick', 'darkblue','lavender','palegoldenrod','navy']
    n=len(poblacion)
    d=len(poblacion[0])


    x=[[]for _ in range(k)]
    y=[[]for _ in range(k)]
    """coords=[[] for _ in range(k)]"""
    for i in range(n):
        """coords[asignacion[i]].append(points[i])"""
        x[asignacion[i]].append(poblacion[i][0])
        y[asignacion[i]].append(poblacion[i][1])
    #print(coords[0])
    
    

    for i in range(k):
        plt.scatter(x[i], y[i], color=colors[i])
    
        
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2D-Plot')
    
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

"""In KMeans clustering, the goal is to partition the input data into a 
predetermined number of clusters, with each cluster represented by its 
centroid (the center point of the cluster). The algorithm aims to minimize 
the sum of squared distances between data points and their respective cluster centroids."""
def evaluacion(poblacion, asignacion,centroides):
    n=len(poblacion)
    d=len(poblacion[0])
    k=len(centroides)
    

    """for i in range(len(a)):
            ret+=(a[i]-b[i])**2 """
    tmp=0.0
    ret=0.0 # distancia Euclidea    
    for i in range(n):
        tmp=0.0
        for a in range(d): # Recorre sus dimensiones                
            tmp+=(poblacion[i][a]-centroides[asignacion[i]][a])**2            
        ret+=(tmp**2)

            
    print("Valor calculado:",ret)
    return ret


def ejecuta_uno(poblacion, k, tipo):
    timeStart=MPI.Wtime()   
    
    kM=KMeans(k, poblacion, False)
    if tipo==0: 
        asignacion,centroides=kM.ejecutaM()
    else: 
        asignacion,centroides=kM.ejecutaE()    
    timeEnd=MPI.Wtime()
    eval=evaluacion(poblacion, asignacion,centroides)
    #print(asignacion)
    print("Mejor Valor:",eval)
    print("Tiempo de ejecucion:",(timeEnd-timeStart))

    plot2D(poblacion,asignacion,k)
    return asignacion

def ejecuta_varios(poblacion, k, times,tipo):
    timeStart=MPI.Wtime()
    ret=float("inf")
    mejor=None
    if tipo==0: 
        for _ in range(times):
            kM=KMeans(k, poblacion, False)
            asignacion,centroides=kM.ejecutaM()
            tmp=evaluacion(poblacion, asignacion,centroides)
            if tmp<ret:
                ret=tmp
                mejor=asignacion
    else: 
        for _ in range(times):
            kM=KMeans(k, poblacion, False)
            asignacion,centroides=kM.ejecutaE()
            tmp=evaluacion(poblacion, asignacion,centroides)
            if tmp<ret:
                ret=tmp
                mejor=asignacion
    
    
    timeEnd=MPI.Wtime()
    
    #print(asignacion)
    print("Mejor Valor:",ret)
    print("Tiempo de ejecucion:",(timeEnd-timeStart))

    plot2D(poblacion,mejor,k)
    return(mejor)
    
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
    k=20
    
    #print(poblacion)
    #a,n=leeArchivo("100000")
    #poblacion=[[x] for x in a]
    #print(poblacion)
    #poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0], [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]

    #asignacion=ejecuta_uno(poblacion, k, 0)
    asignacion=ejecuta_varios(poblacion, k, 20, 0)
    #ejecuta_busquedaM(poblacion, 2, n)
    #ejecuta_busquedaE(poblacion, 2, n)

    



main()



""" FUNCION DE EVALUACION CON LAS DISTANCIAS MINIMAS Y MAXIMAS DE CADA CLUSTER
def evaluacion(poblacion, asignacion,k):
    n=len(poblacion)
    d=len(poblacion[0])
    
    ret=0.0    
    tmp=[[[float("inf"),-float("inf")] for _ in range(d)] for _ in range(k)]
    for i in range(n):
        for a in range(d): # Recorre sus dimensiones                
            if poblacion[i][a]<tmp[asignacion[i]][a][0]: tmp[asignacion[i]][a][0]=poblacion[i][a]     # min
            elif poblacion[i][a]>tmp[asignacion[i]][a][1]: tmp[asignacion[i]][a][1]=poblacion[i][a] # max

    
    for i in range(k):    
        for a in range(d):            
            ret+=abs(tmp[i][a][0]-tmp[i][a][1])**2
            
    print("Valor calculado:",ret)
    return ret
"""