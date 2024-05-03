import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import random
import os
import math

"""
El algoritmo de clustering, KMeans, tiene como objetivo dividir unos datos 
en un numero determindo de clusters (con su respectivo centroide).
"""

# TIEMPO: (datos=100000.txt, k=3)
# Manhattan:
# (ejecuta_uno) Tiempo de ejecucion: 2.326730199973099
# (ejecuta_varios, 5) Tiempo de ejecucion: 10.411191000021063

# Euclidea:
# (ejecuta_uno) Tiempo de ejecucion: 2.9821161999716423
# (ejecuta_varios, 5) Tiempo de ejecucion: 13.842410599987488

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


"""La funcion de evaluacion calcula la suma al cuadrado de distancias (euclidianas) 
de cada individuo al centroide de su cluster"""
def evaluacion(poblacion, asignacion,centroides,imprime):
    n=len(poblacion)
    d=len(poblacion[0])
    
    tmp=0.0
    ret=0.0 # distancia Euclidea    
    for i in range(n):
        tmp=0.0
        for a in range(d): # Recorre sus dimensiones                
            tmp+=(poblacion[i][a]-centroides[asignacion[i]][a])**2            
        ret+=(tmp**2)
            
    if imprime==True: print("Valor calculado:",ret)
    return ret

class KMeans:
    def __init__(self, k, vals, print):
        self.k = k              # int.      NUMERO DE CLUSTERS
        self.poblacion=vals     # float[].  POBLACION
        self.d=len(vals[0])     # int.      NUMERO DE DIMENSIONES
        self.n=len(vals)        # int.      TAM. POBLACION
        self.print=print        # bool.     IMPRIMIR
               
    def compara_centros(self, a, b):
        n=len(a)
        for i in range(n):
            for j in range(self.d):
                if a[i][j]!=b[i][j]: return False
        
        return True

    def ejecuta(self, a, modo):
        procesar=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]
        cent=[[-0.12293300848913269, 8.197940858866115], [9.947053218490957, -0.6975674085386796], [9.591533658594035, -7.407552627543687], [3.7079497249547195, -8.792991586408998], [0.4522664959026699, 6.0981500948027865], [-4.868512907161257, -0.16920748146691977], [-8.199029435615495, 5.179308090342815], [9.922457533335596, -0.497719340882842], [0.5151398954729185, -4.2703198155086275], [3.702589770726254, -3.3200049788824977], [0.5912719290614117, 4.955550264440161], [6.04775453370749, 0.9769190296446162], [8.464188413408685, -3.7927519994207826], [-7.844739643806415, 2.7871471490160804], [0.4227486922140038, -0.052929778805147265], [5.280102567353076, 8.882908143762695], [-0.819485831742746, 5.588877476672495], [-3.000409968481179, -4.522314880691127], [2.748080733683093, 4.108514983968931], [6.518364569672681, -9.246791075220395]]
        centroides=[cent[i] for i in range(self.k)]
        
        datos=[[]for _ in range(2)]
        tamDatos=[]
        if modo==0:            
            for x in procesar:
                timeStart=MPI.Wtime()
                
                self.poblacion=[]
                for ind in a[0:x+1]:
                    self.poblacion.append(ind)
                self.n=len(self.poblacion) 

                self.ejecutaM(centroides) 

                timeEnd=MPI.Wtime()
                print("Tiempo de ejecucion D. Manhattan:",(timeEnd-timeStart))
                datos[0].append(timeEnd-timeStart)

                # ---

                timeStart=MPI.Wtime()
                
                self.poblacion=[]
                for ind in a[0:x+1]:
                    self.poblacion.append(ind)
                self.n=len(self.poblacion) 
                
                self.ejecutaE(centroides) 

                timeEnd=MPI.Wtime()
                print("Tiempo de ejecucion D. Euclidea:",(timeEnd-timeStart))
                datos[1].append(timeEnd-timeStart)
                tamDatos.append(x)
                guarda_datos(["KMedias{}M.txt".format(self.k),"KMedias{}E.txt".format(self.k),"TamDatos.txt"],datos,tamDatos)


                
                

    def ejecutaM(self, centroides):
        # Inicializa centros de forma aleatoria
        # diccionario para almacenar los individuos ya seleccionados y no repetir centroides
        if centroides==None:
            dic={} 
            centroides=[]   # centroides iniciales
            for i in range(self.k):
                while True:
                    rand=random.randint(0, self.n-1)
                    if rand not in dic:
                        centroides.append(self.poblacion[rand])                
                        dic[rand]=1
                        break
             
        
        
        asignacion=[-1 for i in range(self.n)]

        while True: # Hasta que los centroides no cambien
            
            # 1. Fase de asginacion
            for i in range(self.n):
                tmp=-1
                cluster=-1
                dist=float('inf')
                # Compara la distancia del individuo actual a cada centroide
                for j in range(self.k): 
                    tmp=self.manhattan(self.poblacion[i], centroides[j])
                    if dist>tmp:
                        dist=tmp
                        cluster=j
                asignacion[i]=cluster # Asigna su cluster (el centroide mas cercano)

            # 2. Actualiza el los centros
                
            # Numero de inviduos en cada cluster
            indsCluster=[0 for _ in range(self.k)] 
            # Nuevos centroides: calculados con la media de todos los individuos del cluster
            centroidesNuevos=[[0 for _ in range(self.d)] for _ in range(self.k)]
            for i in range(self.n):
                for j in range(self.d): # Dimensiones
                    centroidesNuevos[asignacion[i]][j]+=self.poblacion[i][j]
                indsCluster[asignacion[i]]+=1

            

            if self.print==True:
                print("Poblacion:",self.poblacion)
                print("Centroides:",centroides)
                print("indsClusters:",indsCluster)

            # Para cada cluster divide entre su numero de individuos (en cada dimension)
            for i in range(self.k): 
                for j in range(self.d):  
                    if indsCluster[i]!=0: centroidesNuevos[i][j]/=indsCluster[i]                       
            if self.print==True: print("Nuevos Centroides:",centroidesNuevos)

            

            # 3. Compara los centroides para ver si finaliza la ejecucion
            if(self.compara_centros(centroides,centroidesNuevos)): break
            centroides=centroidesNuevos # No finaliza y se actualizan los centroides

        return asignacion,centroides
    
    # Misma ejecucion pero con euclidea
    def ejecutaE(self, centroides):
        
        # Inicializa centros
        if centroides==None:
            dic={}
            centroides=[]
            for i in range(self.k):
                while True:
                    rand = random.randint(0, self.n - 1)
                    if rand not in dic:
                        centroides.append(self.poblacion[rand])                
                        dic[rand] = 1
                        break

        #print(centroides)
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




def ejecuta_uno(poblacion, k, tipo):
    timeStart=MPI.Wtime()   
    
    kM=KMeans(k, poblacion,False)
    if tipo==0: 
        asignacion,centroides=kM.ejecutaM()
    else: 
        asignacion,centroides=kM.ejecutaE()    
    timeEnd=MPI.Wtime()
    

    
    print("Tiempo de ejecucion:",(timeEnd-timeStart))

    

    return asignacion

def ejecuta_busquedaM(poblacion, maxCluster, times):    
    print("Distancia Manhattan\n")
    fits=[]
    mejores=[]
    centroidesMejores=[]

    totalTimeStart = MPI.Wtime()
    
    for k in range(1,maxCluster+1):
        timeStart=MPI.Wtime()
        ret=float("inf")
        for _ in range(times):
            kM=KMeans(k, poblacion, False)
            asignacion,centroides=kM.ejecutaM()
            tmp=evaluacion(poblacion, asignacion,centroides,False)
            if tmp<ret:
                ret=tmp
                mejor=asignacion
                centroidesMejor=centroides
        timeEnd=MPI.Wtime()
        print("Cluster (k)= {}, mejor valor= {}.\nTiempo de Ejecucion: {}".format(k,ret,(timeEnd-timeStart)))        
        fits.append(ret)
        mejores.append(mejor)
        centroidesMejores.append(centroidesMejor)

    totalTimeEnd = MPI.Wtime()
    print("Tiempo de ejecucion total: {}".format(totalTimeEnd-totalTimeStart))

   
def ejecuta_busquedaE(poblacion, maxCluster, times):
    print("Distancia Euclidea\n")
    fits=[]
    mejores=[]
    centroidesMejores=[]
    totalTimeStart = MPI.Wtime()
        
    for k in range(1,maxCluster+1):
        timeStart=MPI.Wtime()
        ret=float("inf")
        for _ in range(times):
            kM=KMeans(k, poblacion, False)
            asignacion,centroides=kM.ejecutaE()
            tmp=evaluacion(poblacion, asignacion,centroides,False)
            if tmp<ret:
                ret=tmp
                mejor=asignacion
                centroidesMejor=centroides
        timeEnd=MPI.Wtime()
        print("Cluster (k)= {}, mejor valor= {}.\nTiempo de Ejecucion: {}".format(k,ret,(timeEnd-timeStart)))        
        fits.append(ret)
        mejores.append(mejor)
        centroidesMejores.append(centroidesMejor)
    
    totalTimeEnd = MPI.Wtime()
    print("Tiempo de ejecucion total: {}".format(totalTimeEnd-totalTimeStart))



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
 
    
def main():
    
    """poblacion=lee("10_2D")
    
    # Numero de clusters ejecutados [1-k]
    k=3
    
    # Variables: poblacion, numero de clusters, manh o eucl
    asignacion=ejecuta_uno(poblacion, k, 0)
    
    #ejecuta_busquedaM(poblacion, k, 20)
    #ejecuta_busquedaE(poblacion, k, 8)"""

    # Valores entre [-10,10] para ambas dimensiones
    poblacion=lee("100000_2D")
    
    # Numero de clusters ejecutados [1-k]
    numsK=[3,5,10,15,20]
    for k in numsK:
    #k=5
        kM=KMeans(k,poblacion,False)    
        kM.ejecuta(poblacion, 0)

main()
