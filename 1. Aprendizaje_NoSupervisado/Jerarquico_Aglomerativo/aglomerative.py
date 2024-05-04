import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import random
import os
import math

# Para realizar copias sin punteros
import copy



# Mejor

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

        
    
    def ejecuta(self,clusts):
        if self.tipo==0: return self.ejecuta_centroide(clusts)
        elif self.tipo==1: return self.ejecuta_simple(clusts)
        else: return self.ejecuta_completo(clusts)
    
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


def GUI(k, mejor, fits, coefs, poblacion,asignacion):    
    # Create figure and axes
    #fig, axs = plt.subplots(2, 2, figsize=(18, 12), gridspec_kw={'width_ratios': [1, 2]})
    
    # Define data for the first plot
    x1 = [i for i in range(1, k + 1)]  
    # Define data for the second plot
    x2 = [i for i in range(2, k + 1)] 
    # Define data for the third plot
    colors = ['blue', 'red', 'green', 'black', 'pink', 'yellow', 'magenta', 'brown', 'darkgreen', 'gray', 'fuchsia',
            'violet', 'salmon', 'darkturquoise', 'forestgreen', 'firebrick', 'darkblue', 'lavender', 'palegoldenrod',
            'navy']
    n = len(poblacion)
    x3 = [[] for _ in range(k)]
    y3 = [[] for _ in range(k)]
    for i in range(n):
        x3[asignacion[i]].append(poblacion[i][0])
        y3[asignacion[i]].append(poblacion[i][1])


    # Crear la figura y GridSpec
    fig = plt.figure(figsize=(10, 6))
    gs = GridSpec(2, 2, figure=fig)

    # Grafico 1 (arriba a la izquierda)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x1, fits, color='b', linestyle='-')
    ax1.scatter(mejor+1, fits[mejor], color='red')  # Punto rojo 
    ax1.set_xlabel('Clusters')
    ax1.set_ylabel('Fitness')
    ax1.set_title('Diagrama de codo')
    ax1.grid(True)

    # Grafico 2 (abajo a la izquierda)
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(x2, coefs, color='b', linestyle='-') 
    ax2.scatter(mejor+1, coefs[mejor-1], color='red')  # Punto rojo 
    ax2.set_xlabel('Clusters')
    ax2.set_ylabel('Coficiente')
    ax2.set_title('Davies Bouldin')
    ax2.grid(True)
    ax2.set_xlim(1, k)  # Expandir el eje x

    # Grafico 3 (a la derecha, ocupando las 2 filas)
    ax3 = fig.add_subplot(gs[:, 1])
    # Plot the third diagram in the first row, second column
    for i in range(k):
        ax3.scatter(x3[i], y3[i], color=colors[i])
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_title('Poblacion')
    
    
    plt.tight_layout() # Ajustar la disposición de los subplots    
    plt.show() # Mostrar los gráficos

def calcula_DB_mejor(DBs):
    n=len(DBs)
    val=DBs[0]
    ret=0

    for i in range(1,n):
        if val>DBs[i]: 
            val=DBs[i]
            ret=i

    return ret          

def davies_bouldin(poblacion, k, asignacion, centroides):
    ret=0.0
    n=len(poblacion)
    
    tmp=0.0
    distanciaProm=[0.0 for _ in range(k)]    
    indsCluster=[0 for _ in range(k)] # Numero de inviduos en cada cluster    
    for i in range(n):
        distanciaProm[asignacion[i]]+=distancia(centroides[asignacion[i]],poblacion[i])        
        indsCluster[asignacion[i]]+=1
    
    for i in range(k):
        distanciaProm[i]/=indsCluster[i]
    
    distanciaClust=[[0 for _ in range(k)] for _ in range(k)]
    for i in range(k-1):
        for j in range(i+1,k):
            tmp=distancia(centroides[i],centroides[j])
            distanciaClust[i][j]=tmp
            distanciaClust[j][i]=tmp
    
    tmp=0.0
    for i in range(k):
        maxVal=0.0
        for j in range(k):
            if i==j: continue
            tmp=(distanciaProm[i]+distanciaProm[j])/(distanciaClust[i][j])
            if tmp>maxVal: maxVal=tmp
        
        ret+=maxVal
    
    ret/=k
    return ret

def plot2D(poblacion,asignacion,k):
    #['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
    colors=['blue','red','green','black','pink','yellow','magenta','brown','darkgreen','gray','fuchsia','violet','salmon','darkturquoise','forestgreen','firebrick', 'darkblue','lavender','palegoldenrod','navy']
    n=len(poblacion)

    x=[[]for _ in range(k)]
    y=[[]for _ in range(k)]
    for i in range(n):
        x[asignacion[i]].append(poblacion[i][0])
        y[asignacion[i]].append(poblacion[i][1])
        
    for i in range(k):
        plt.scatter(x[i], y[i], color=colors[i])            
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2D-Plot')
    
    plt.show()

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
    print("Por centroide")
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

   
    
    fits=[evaluacion(poblacion, asignacionesFin[i],centroides[i]) for i in range(clusts)]

    DBs=[davies_bouldin(poblacion, i, asignacionesFin[i-1], centroides[i-1]) for i in range(2,clusts+1)] 
    
    dbMejor=calcula_DB_mejor(DBs)

    """print("F",DBs)"""

    GUI(clusts, dbMejor+1, fits,DBs,poblacion, asignacionesFin[dbMejor+1])

def ejecuta_simple(poblacion, distancia, clusts):
    print("Por enlace simple")
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
    
    
    print(centroidesFin[0])
    fits=[evaluacion(poblacion, asignacionesFin[i],centroidesFin[i]) for i in range(clusts)]

    DBs=[davies_bouldin(poblacion, i, asignacionesFin[i-1], centroidesFin[i-1]) for i in range(2,clusts+1)]     
    dbMejor=calcula_DB_mejor(DBs)

    GUI(clusts, dbMejor+1, fits,DBs,poblacion, asignacionesFin[dbMejor+1])

def ejecuta_completa(poblacion, distancia, clusts):
    print("Por enlace completo")
    
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

    

    
    
    fits=[evaluacion(poblacion, asignacionesFin[i],centroidesFin[i]) for i in range(clusts)]

    DBs=[davies_bouldin(poblacion, i, asignacionesFin[i-1], centroidesFin[i-1]) for i in range(2,clusts+1)]    
    dbMejor=calcula_DB_mejor(DBs)

    GUI(clusts, dbMejor+1, fits,DBs,poblacion, asignacionesFin[dbMejor+1])



def main():
    #poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0], [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]#, [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]
    # 6000      1 generacion de puntos aleatorios
    # 6000_2    2 generaciones de puntos aleatorios
    # 6000_3    6 generaciones de puntos aleatorios
    # 100000_2D    6 generaciones de puntos aleatorios
    archivo="5000_1_2D"
    C=7
    dists=["Manhattan","Euclidea"]
    distancia=1
    poblacion=lee(archivo)

    print("\nEjecutando archivo: {}, numero de clusters para la GUI: {}, distancia: {}\n".format(archivo, C, dists[distancia]))
        
    #ejecuta_diferentes_poblaciones(poblacion,1)

    #ejecuta_centroide(poblacion, distancia, C)
    ejecuta_simple(poblacion, distancia, C)
    #ejecuta_completa(poblacion, distancia, C)

    

main()


