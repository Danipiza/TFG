import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI

import random
import os
import math

import copy


def guarda_datos(archivo,datos,tamDatos):    
    """print(tamArray)
    for x in datos:
        print(x,"\n")"""
    

    with open(archivo[0], 'w') as file:
        for i, val in enumerate(datos[0]):
            file.write("{}, ".format(val))
        file.write("\n")
    with open(archivo[1], 'w') as file:
        for i, val in enumerate(datos[1]):
            file.write("{}, ".format(val))
        file.write("\n")
    with open(archivo[2], 'w') as file:
        for i, val in enumerate(tamDatos):
            file.write("{}, ".format(val))
        file.write("\n")


def lee(archivo):

    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","2.Cluster", archivo+".txt")

    with open(path, 'r') as file:
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

class Distancia1():
    def distancia(self,a,b): 
        ret=0.0
        for i in range(len(a)):
            ret+=abs(a[i]-b[i])
        return ret    
class Distancia2():
    def distancia(self,a,b): 
        ret=0.0
        for i in range(len(a)):
            ret+=(a[i]-b[i])**2        
        
        return math.sqrt(ret)

class Jerarquico_Aglom:
    def __init__(self, vals, C, tipo, dist):
        self.poblacion=vals         # float[i][dimension].  Poblacion a analizar
        self.d=len(vals[0])         # int.                  Dimensiones de los individuos
        self.n=len(vals)            # int.                  Tamaño de la poblacion        
        self.C=C                    # int.                  Numero de clusters
        self.tipo=tipo              # int.                  Distancia entre clusters
        #                                                   0: Centroide, 1: Simple, 2: Completa
        self.distancia=None         # Distancia.            Funcion para calcular la distancia enter individuos
        #                                                   Manhattan:0 Euclidea=1

        if dist==0: self.distancia=Distancia1()
        else: self.distancia=Distancia2()

        
    
    def ejecuta(self,a,clusts):
        procesar=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]
        
        datos=[[]for _ in range(2)]
        tamDatos=[]
        
        # SIMPLE
        if self.tipo==0: 
            for x in procesar:
                self.distancia=Distancia1()
                timeStart=MPI.Wtime()
                
                self.poblacion=[]
                for ind in a[0:x+1]:
                    self.poblacion.append(ind)
                self.n=len(self.poblacion) 

                self.ejecuta_centroide(clusts)
                timeEnd=MPI.Wtime()
                print("Tiempo de ejecucion D. Manhattan: {} \t{}".format((timeEnd-timeStart),x))
                datos[0].append(timeEnd-timeStart)

                # ---
                self.distancia=Distancia2()
                timeStart=MPI.Wtime()

                self.poblacion=[]
                for ind in a[0:x+1]:
                    self.poblacion.append(ind)
                self.n=len(self.poblacion) 

                self.ejecuta_centroide(clusts)
                timeEnd=MPI.Wtime()
                print("Tiempo de ejecucion D. Euclidea: {} \t{}".format((timeEnd-timeStart),x))
                datos[1].append(timeEnd-timeStart)

                tamDatos.append(x)
                guarda_datos(["Aglomerative_C_M.txt","Aglomerative_C_E.txt","TamDatos.txt"],datos,tamDatos)


        elif self.tipo==1: 
            for x in procesar:
                self.distancia=Distancia1()
                timeStart=MPI.Wtime()
                
                self.poblacion=[]
                for ind in a[0:x+1]:
                    self.poblacion.append(ind)
                self.n=len(self.poblacion) 

                self.ejecuta_simple(clusts)
                timeEnd=MPI.Wtime()
                print("Tiempo de ejecucion D. Manhattan (SIMPLE):",(timeEnd-timeStart))
                datos[0].append(timeEnd-timeStart)

                # ---
                self.distancia=Distancia2()
                timeStart=MPI.Wtime()

                self.poblacion=[]
                for ind in a[0:x+1]:
                    self.poblacion.append(ind)
                self.n=len(self.poblacion) 

                self.ejecuta_simple(clusts)
                timeEnd=MPI.Wtime()
                print("Tiempo de ejecucion D. Euclidea (SIMPLE):",(timeEnd-timeStart))
                datos[1].append(timeEnd-timeStart)

                tamDatos.append(x)
                guarda_datos(["Aglomerative_Sim_M.txt","Aglomerative_Sim_E.txt","TamDatos.txt"],datos,tamDatos)
            
        else: 
            for x in procesar:
                self.distancia=Distancia1()
                timeStart=MPI.Wtime()
                
                self.poblacion=[]
                for ind in a[0:x+1]:
                    self.poblacion.append(ind)
                self.n=len(self.poblacion) 

                self.ejecuta_completo(clusts)
                timeEnd=MPI.Wtime()
                print("Tiempo de ejecucion D. Manhattan (COMPLETO):",(timeEnd-timeStart))
                datos[0].append(timeEnd-timeStart)

                # ---
                self.distancia=Distancia2()
                timeStart=MPI.Wtime()

                self.poblacion=[]
                for ind in a[0:x+1]:
                    self.poblacion.append(ind)
                self.n=len(self.poblacion) 

                self.ejecuta_completo(clusts)
                timeEnd=MPI.Wtime()
                print("Tiempo de ejecucion D. Euclidea (COMPLETO):",(timeEnd-timeStart))
                datos[1].append(timeEnd-timeStart)

                tamDatos.append(x)
                guarda_datos(["Aglomerative_Com_M.txt","Aglomerative_Com_E.txt","TamDatos.txt"],datos,tamDatos)
            
    
    def ejecuta_centroide(self, clusts):

        # FASE1: Inicializa Matriz de distancias
        M=[([0 for _ in range(self.n)]) for _ in range(self.n-1)]        
        for i in range(self.n-1):                       
            for j in range(i+1,self.n):
                M[i][j]=self.distancia.distancia(self.poblacion[i],self.poblacion[j])
            
        # Array de clusters
        clusters=[[i] for i in range(self.n)]        
        # Array con los centros de cada cluster
        clustersCentros=[x for x in self.poblacion]        
        
        asig=[[] for _ in range(clusts)]
        centr=[[] for _ in range(clusts)]
        
        
        
        # FASE2:         
        # Repite hasta que solo haya "self.C" clusters
        for k in range(self.C,self.n):  

            # Elegir los 2 cluster mas cercanos            
            c1,c2=None,None
            distMin=float("inf")            
            for i in range(len(M)):
                for j in range(i+1,len(M[0])):
                    if distMin>=M[i][j]: 
                        distMin=M[i][j]
                        c1=i
                        c2=j            
            
            # Junta los cluster mas cercanos
            for x in clusters[c2]:
                clusters[c1].append(x)                
            clusters.pop(c2) 
           
            # Actualiza centro            
            tmp=[0.0 for _ in range(self.d)]
            for x in clusters[c1]:
                for y in range(self.d):
                    tmp[y]+=self.poblacion[x][y]
            for x in range(self.d):
                tmp[x]/=len(clusters[c1])
            clustersCentros[c1]=tmp
            clustersCentros.pop(c2)
           
            
            # Borra fila, si se elimina el ultimo cluster no hay que eliminar la fila.
                # Porque la matriz esta implementada solo el triangulo superior 
            if c2!=len(M): M.pop(c2)
            # Borra Columna
            for row in M:
                del row[c2]
            
            # Actualiza col
            i=0
            while i!=c1:
                M[i][c1]=self.distancia.distancia(clustersCentros[c1],clustersCentros[i])                
                i+=1

            # Actualiza fil
            for i in range(c1+1,len(M[c1])):
                M[c1][i]=self.distancia.distancia(clustersCentros[c1],clustersCentros[i])

            
            
            # PARA LA GUI y comprobar el mejor numero de clusters
            if self.n-k-1<clusts: 
                asig[self.n-k-1]=copy.deepcopy(clusters)
                centr[self.n-k-1]=copy.deepcopy(clustersCentros)

            
        return asig, centr

    def ejecuta_simple(self, clusts):

        # FASE1: Inicializa Matriz de distancias
        M=[([0 for _ in range(self.n)]) for _ in range(self.n-1)]        
        for i in range(self.n-1):                       
            for j in range(i+1,self.n):
                M[i][j]=self.distancia.distancia(self.poblacion[i],self.poblacion[j])
            
        # Array de clusters
        clusters=[[i] for i in range(self.n)]        
        # Array con los centros de cada cluster
        clustersCentros=[[x] for x in self.poblacion]
        
        asig=[[] for _ in range(clusts)]
        centr=[[] for _ in range(clusts)]
        # FASE2:         
        # Repite hasta que solo haya "self.C" clusters
        for k in range(self.C,self.n): 
            # Elegir los 2 cluster mas cercanos            
            c1,c2=None,None
            distMin=float("inf")            
            for i in range(len(M)):
                for j in range(i+1,len(M[0])):
                    if distMin>M[i][j]: 
                        distMin=M[i][j]
                        c1=i
                        c2=j            
            
            # Junta los cluster mas cercanos
            for x in clusters[c2]:
                clusters[c1].append(x)                
            clusters.pop(c2) 
           
            # Actualiza centro    
            for x in clustersCentros[c2]:
                clustersCentros[c1].append(x)                
            clustersCentros.pop(c2) 
            
            
            # Borra fila, si se elimina el ultimo cluster no hay que eliminar la fila.
                # Porque la matriz esta implementada solo el triangulo superior 
            if c2!=len(M): M.pop(c2)
            # Borra Columna
            for row in M:
                del row[c2]
            

            c1N=len(clustersCentros[c1])
            # Actualiza col
            i=0
            while i!=c1:
                nDist=float("inf")
                distTMP=float("inf")
                c2N=len(clustersCentros[i])
                for a in range(c1N):            # Recorre los individuos de "c1"
                    for b in range(c2N):    # Recorre los individuos de "i2 (individuo a cambiar de la fila)
                        distTMP=self.distancia.distancia(clustersCentros[c1][a],clustersCentros[i][b])
                        if distTMP<nDist: nDist=distTMP # Coge la menor distancia entre el individuo "c1" e "i"

                M[i][c1]=nDist
                #M[i][c1]=self.distancia.distancia(clustersCentros[c1],clustersCentros[i])                
                i+=1

            # Actualiza fil TODO PARALELIZAR                       
            for i in range(c1+1,len(M[c1])):
                nDist=float("inf")
                distTMP=float("inf")
                c2N=len(clustersCentros[i])
                for a in range(c1N):            # Recorre los individuos de "c1"
                    for b in range(c2N):    # Recorre los individuos de "i2 (individuo a cambiar de la fila)
                        distTMP=self.distancia.distancia(clustersCentros[c1][a],clustersCentros[i][b])
                        if distTMP<nDist: nDist=distTMP # Coge la menor distancia entre el individuo "c1" e "i"

                M[c1][i]=nDist

            # PARA LA GUI y comprobar el mejor numero de clusters
            if self.n-k-1<clusts: 
                asig[self.n-k-1]=copy.deepcopy(clusters)
                centr[self.n-k-1]=copy.deepcopy(clustersCentros)
        return asig, centr
    
    def ejecuta_completo(self, clusts):

        # FASE1: Inicializa Matriz de distancias        
        M=[[0 for _ in range(self.n)] for _ in range(self.n-1)]        
        
        for i in range(self.n-1):                       
            for j in range(i+1,self.n):
                M[i][j]=self.distancia.distancia(self.poblacion[i],self.poblacion[j])
           
        # Array de clusters
        clusters=[[i] for i in range(self.n)]        
        # Array con los centros de cada cluster
        clustersCentros=[[x] for x in self.poblacion]
        
        asig=[[] for _ in range(clusts)]
        centr=[[] for _ in range(clusts)]
        # FASE2:         
        # Repite hasta que solo haya "self.C" clusters
        for k in range(self.C,self.n):  
            # Elegir los 2 cluster mas cercanos            
            c1,c2=None,None
            distMin=float("inf")            
            for i in range(len(M)):
                for j in range(i+1,len(M[0])):
                    if distMin>M[i][j]: 
                        distMin=M[i][j]
                        c1=i
                        c2=j            
            
            # Junta los cluster mas cercanos
            for x in clusters[c2]:
                clusters[c1].append(x)                
            clusters.pop(c2) 
           
            # Actualiza centro    
            for x in clustersCentros[c2]:
                clustersCentros[c1].append(x)                
            clustersCentros.pop(c2)              
            
            # Borra fila, si se elimina el ultimo cluster no hay que eliminar la fila.
                # Porque la matriz esta implementada solo el triangulo superior 
            if c2!=len(M): M.pop(c2)
            # Borra Columna
            for row in M:
                del row[c2]
            

            c1N=len(clustersCentros[c1])
            # Actualiza col
            i=0
            while i!=c1:
                nDist=-float("inf")
                distTMP=-float("inf")
                c2N=len(clustersCentros[i])
                for a in range(c1N):            # Recorre los individuos de "c1"
                    for b in range(c2N):    # Recorre los individuos de "i2 (individuo a cambiar de la fila)
                        distTMP=self.distancia.distancia(clustersCentros[c1][a],clustersCentros[i][b])
                        if distTMP>nDist: nDist=distTMP # Coge la menor distancia entre el individuo "c1" e "i"

                M[i][c1]=nDist
                #M[i][c1]=self.distancia.distancia(clustersCentros[c1],clustersCentros[i])                
                i+=1

            # Actualiza fil TODO PARALELIZAR                       
            for i in range(c1+1,len(M[c1])):
                nDist=-float("inf")
                distTMP=-float("inf")
                c2N=len(clustersCentros[i])
                for a in range(c1N):            # Recorre los individuos de "c1"
                    for b in range(c2N):    # Recorre los individuos de "i2 (individuo a cambiar de la fila)
                        distTMP=self.distancia.distancia(clustersCentros[c1][a],clustersCentros[i][b])
                        if distTMP>nDist: nDist=distTMP # Coge la menor distancia entre el individuo "c1" e "i"

                M[c1][i]=nDist

                        
            # PARA LA GUI y comprobar el mejor numero de clusters
            if self.n-k-1<clusts: 
                asig[self.n-k-1]=copy.deepcopy(clusters)
                centr[self.n-k-1]=copy.deepcopy(clustersCentros)
        return asig, centr



"""La funcion de evaluacion calcula la suma al cuadrado de distancias (euclidianas) 
de cada individuo al centroide de su cluster"""
def evaluacion(poblacion, asignacion,centroides):
    n=len(poblacion)
    d=len(poblacion[0])
    
    tmp=0.0
    ret=0.0 # distancia Euclidea    
    for i in range(n):
        tmp=0.0
        for a in range(d): # Recorre sus dimensiones                
            tmp+=(poblacion[i][a]-centroides[asignacion[i]][a])**2            
        ret+=(tmp**2)
            
    return ret

def distancia(a,b):
    ret=0.0
    for i in range(len(a)):
        ret+=(a[i]-b[i])**2        
    
    return math.sqrt(ret)


def ejecuta_diferentes_poblaciones(poblacion,k):

    # vals, Num Clusters, tipo=centroide, simple, completo, dist=Manhattan o Euclidea, print
    suma=100
    cont=10

    dic={}
    dic[0]="Centroide"
    dic[1]="Simple   "
    dic[2]="Completa "
    print("Array desordenado con valores de 0-10000")

    while(cont<10000):
        print("\nArray[0:{}]".format(cont))
        for i in range(3):
            timeStart=MPI.Wtime()
            JA=Jerarquico_Aglom(poblacion[0:cont],k,i,0)
            prueba=JA.ejecuta()
            timeEnd=MPI.Wtime()
            print("{}. Tiempo de ejecucion: {}".format(dic[i],(timeEnd-timeStart)))
        cont+=suma
        if cont == 1000:
            suma=250
        elif cont == 2500:
            suma=500    

def ejecuta_centroide(poblacion, distancia, clusts):
    n=len(poblacion)
    k=1
    timeStart=MPI.Wtime()
    JA=Jerarquico_Aglom(poblacion,k,0,distancia)
    asignaciones, centroides=JA.ejecuta(clusts)    
    
    """for x in asignaciones:
        print("Len=",len(x),x)"""
    
    asignacionesFin=[[-1 for _ in range(n)] for _ in range(clusts)]
    for numClust in range(clusts):
        for i in range(numClust+1):
            for j in asignaciones[numClust][i]:
                asignacionesFin[numClust][j]=i
        #print(asignacionesFin[i])
        
    

    timeEnd=MPI.Wtime()
    print("Tiempo de ejecucion: {}\n".format(timeEnd-timeStart))

   

def ejecuta_simple(poblacion, distancia, clusts):
    n=len(poblacion)
    d=len(poblacion[0])
    k=1
    timeStart=MPI.Wtime()
    JA=Jerarquico_Aglom(poblacion,k,1,distancia)
    asignaciones, centroides=JA.ejecuta(clusts) 
    
    asignacionesFin=[[-1 for _ in range(n)] for _ in range(clusts)]
    for numClust in range(clusts):
        for i in range(numClust+1):
            for j in asignaciones[numClust][i]:
                asignacionesFin[numClust][j]=i

    centroidesFin=[] 
    for numClust in range(clusts):
        tmpClust=[]
        for j in range(numClust+1):
            m=len(centroides[numClust][j])
            tmp=[0 for _ in range(d)]
            for x in centroides[numClust][j]:
                for a in range(d):
                    tmp[a]+=x[a]
            for a in range(d):
                tmp[a]/=m
            tmpClust.append(tmp)                      

        centroidesFin.append(tmpClust)

    
    timeEnd=MPI.Wtime()
    print("Tiempo de ejecucion: {}\n".format(timeEnd-timeStart))
      
    

def ejecuta_completa(poblacion, distancia, clusts):
    n=len(poblacion)
    d=len(poblacion[0])
    k=1
    timeStart=MPI.Wtime()
    JA=Jerarquico_Aglom(poblacion,k,2,distancia)
    asignaciones, centroides=JA.ejecuta(clusts) 

    timeEnd=MPI.Wtime()
    print("Tiempo de ejecucion: {}\n".format(timeEnd-timeStart))
    
    asignacionesFin=[[-1 for _ in range(n)] for _ in range(clusts)]
    for numClust in range(clusts):
        for i in range(numClust+1):
            for j in asignaciones[numClust][i]:
                asignacionesFin[numClust][j]=i

    centroidesFin=[] 
    for numClust in range(clusts):
        tmpClust=[]
        for j in range(numClust+1):
            m=len(centroides[numClust][j])
            tmp=[0 for _ in range(d)]
            for x in centroides[numClust][j]:
                for a in range(d):
                    tmp[a]+=x[a]
            for a in range(d):
                tmp[a]/=m
            tmpClust.append(tmp)                      

        centroidesFin.append(tmpClust)

    


def main():
    
    """archivo="6000_1_2D"
    C=7
    dists=["Manhattan","Euclidea"]
    distancia=1
    poblacion=lee(archivo)

    print("\nEjecutando archivo: {}, numero de clusters para la GUI: {}, distancia: {}\n".format(archivo, C, dists[distancia]))
        
    #ejecuta_diferentes_poblaciones(poblacion,1)

    #ejecuta_centroide(poblacion, distancia, C)
    ejecuta_simple(poblacion, distancia, C)
    #ejecuta_completa(poblacion, distancia, C)"""
    # Valores entre [-10,10] para ambas dimensiones
    poblacion=lee("100000_2D")
    
    C=1
    distancia=0    
    tipo=1 # 0: Centroide, 1: Simple, 2: Completa 
        
    JA=Jerarquico_Aglom(poblacion,C,tipo,distancia)
    JA.ejecuta(poblacion,1) 

    

main()


