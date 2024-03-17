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

"""class Distancias(ABC):
    @abstractmethod
    def distancia(self,a,b): 
        pass   """  
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
    def __init__(self, vals, C, tipo, dist, print):
        self.poblacion=vals         # float[i][dimension].  Poblacion a analizar
        self.d=len(vals[0])         # int.                  Dimensiones de los individuos
        self.n=len(vals)            # int.                  Tamaño de la poblacion
        self.print=print            # bool.                 Imprime el procedimiento
        self.C=C                    # int.                  Numero de clusters
        self.tipo=tipo              # int.                  Distancia entre clusters
        #                                                   0: Centroide, 1: Simple, 2: Completa
        self.distancia=None         # Distancia.            Funcion para calcular la distancia enter individuos
        #                                                   Manhattan:0 Euclidea=1

        if dist==0: self.distancia=Distancia1()
        else: self.distancia=Distancia2()

        
        

        
    
    def ejecuta(self):
        if self.tipo==0: return self.ejecuta_centroide()
        elif self.tipo==1: return self.ejecuta_simple()
        else: return self.ejecuta_completo()

    def ejecuta_centroide(self):

        # FASE1: Inicializa Matriz de distancias
        M=[([0 for _ in range(self.n)]) for _ in range(self.n-1)]        
        for i in range(self.n-1):                       
            for j in range(i+1,self.n):
                M[i][j]=self.distancia.distancia(self.poblacion[i],self.poblacion[j])
            
        # Array de clusters
        clusters=[[i] for i in range(self.n)]        
        # Array con los centros de cada cluster
        clustersCentros=[x for x in self.poblacion]
        if self.print==True: 
            print("Clusters:",clusters)
            print("Centros de los Clusters:",clustersCentros)
        
        # FASE2:         
        # Repite hasta que solo haya "self.C" clusters
        for k in range(self.C,self.n):            
            if self.print==True: 
                print("\n")
                print("Matriz:")
                for row in M:
                    print(row)

            # Elegir los 2 cluster mas cercanos            
            c1,c2=None,None
            distMin=float("inf")            
            for i in range(len(M)):
                for j in range(i+1,len(M[0])):
                    if distMin>M[i][j]: 
                        distMin=M[i][j]
                        c1=i
                        c2=j            
            if self.print==True:  print("C1:",c1, "C2:",c2)
            
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

            if self.print==True: 
                print("Actualiza")
                print("Clusters:",clusters)
                print("Centros de los Clusters:",clustersCentros)                
            
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

            
            if self.print==True: 
                print("Actualiza Matriz:")
                for row in M:
                    print(row)
                #print("Poblacion ini:",self.poblacion)
        return clusters

    def ejecuta_simple(self):

        # FASE1: Inicializa Matriz de distancias
        M=[([0 for _ in range(self.n)]) for _ in range(self.n-1)]        
        for i in range(self.n-1):                       
            for j in range(i+1,self.n):
                M[i][j]=self.distancia.distancia(self.poblacion[i],self.poblacion[j])
            
        # Array de clusters
        clusters=[[i] for i in range(self.n)]        
        # Array con los centros de cada cluster
        clustersCentros=[[x] for x in self.poblacion]
        if self.print==True: 
            print("Clusters:",clusters)
            print("Centros de los Clusters:",clustersCentros)
        
        # FASE2:         
        # Repite hasta que solo haya "self.C" clusters
        for k in range(self.C,self.n):            
            if self.print==True: 
                print("\n")
                print("Matriz:")
                for row in M:
                    print(row)

            # Elegir los 2 cluster mas cercanos            
            c1,c2=None,None
            distMin=float("inf")            
            for i in range(len(M)):
                for j in range(i+1,len(M[0])):
                    if distMin>M[i][j]: 
                        distMin=M[i][j]
                        c1=i
                        c2=j            
            if self.print==True:  print("C1:",c1, "C2:",c2)
            
            # Junta los cluster mas cercanos
            for x in clusters[c2]:
                clusters[c1].append(x)                
            clusters.pop(c2) 
           
            # Actualiza centro    
            for x in clustersCentros[c2]:
                clustersCentros[c1].append(x)                
            clustersCentros.pop(c2) 

            if self.print==True: 
                print("Actualiza")
                print("Clusters:",clusters)
                print("Centros de los Clusters:",clustersCentros)                
            
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

            
            if self.print==True: 
                print("Actualiza Matriz:")
                for row in M:
                    print(row)
                #print("Poblacion ini:",self.poblacion)
        return clusters 
    
    def ejecuta_completo(self):

        # FASE1: Inicializa Matriz de distancias
        M=[([0 for _ in range(self.n)]) for _ in range(self.n-1)]        
        for i in range(self.n-1):                       
            for j in range(i+1,self.n):
                M[i][j]=self.distancia.distancia(self.poblacion[i],self.poblacion[j])
            
        # Array de clusters
        clusters=[[i] for i in range(self.n)]        
        # Array con los centros de cada cluster
        clustersCentros=[[x] for x in self.poblacion]
        if self.print==True: 
            print("Clusters:",clusters)
            print("Centros de los Clusters:",clustersCentros)
        
        # FASE2:         
        # Repite hasta que solo haya "self.C" clusters
        for k in range(self.C,self.n):            
            if self.print==True: 
                print("\n")
                print("Matriz:")
                for row in M:
                    print(row)

            # Elegir los 2 cluster mas cercanos            
            c1,c2=None,None
            distMin=float("inf")            
            for i in range(len(M)):
                for j in range(i+1,len(M[0])):
                    if distMin>M[i][j]: 
                        distMin=M[i][j]
                        c1=i
                        c2=j            
            if self.print==True:  print("C1:",c1, "C2:",c2)
            
            # Junta los cluster mas cercanos
            for x in clusters[c2]:
                clusters[c1].append(x)                
            clusters.pop(c2) 
           
            # Actualiza centro    
            for x in clustersCentros[c2]:
                clustersCentros[c1].append(x)                
            clustersCentros.pop(c2) 

            if self.print==True: 
                print("Actualiza")
                print("Clusters:",clusters)
                print("Centros de los Clusters:",clustersCentros)                
            
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

            
            if self.print==True: 
                print("Actualiza Matriz:")
                for row in M:
                    print(row)
                #print("Poblacion ini:",self.poblacion)
        return clusters 

    
    
vals,n=leeArchivo("10000")
poblacion=[[x] for x in vals]

#poblacion=[[1], [2], [4], [5], [11], [12], [14], [15], [19], [20], [20.5], [21]]  #
# vals, Num Clusters, tipo=centroide, simple, completo, dist=Manhattan o Euclidea, print
suma=100
cont=100

dic={}
dic[0]="Centroide"
dic[1]="Simple   "
dic[2]="Completa "
print("Array desordenado con valores de 0-10000")

while(cont<10000):
    print("\nArray[0:{}]".format(cont))
    for i in range(3):
        timeStart=MPI.Wtime()
        JA=Jerarquico_Aglom(poblacion[0:cont],1,i,0,False)
        prueba=JA.ejecuta()
        timeEnd=MPI.Wtime()
        print("{}. Tiempo de ejecucion: {}".format(dic[i],(timeEnd-timeStart)))
    cont+=suma
    if cont == 1000:
        suma=250
    elif cont == 2500:
        suma=500 


"""
cont=0
for x in prueba:
    prueba[cont]= sorted(x)
    cont+=1
print(prueba)
"""


