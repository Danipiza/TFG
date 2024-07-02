import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import random
import os
import math

"""
El algoritmo de clustering, KMedias, tiene como objetivo dividir unos datos 
en un numero determindo de clusters (con su respectivo centroide).
"""


# TIEMPO: (datos=100000.txt, k=3)
# Manhattan:
# (ejecuta_uno) Tiempo de ejecucion: 2.326730199973099
# (ejecuta_varios, 5) Tiempo de ejecucion: 10.411191000021063

# Euclidea:
# (ejecuta_uno) Tiempo de ejecucion: 2.9821161999716423
# (ejecuta_varios, 5) Tiempo de ejecucion: 13.842410599987488


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

    def ejecutaM(self):
        # Inicializa centros de forma aleatoria
        # diccionario para almacenar los individuos ya seleccionados y no repetir centroides
        dic={} 
        """centroides=[]   # centroides iniciales
        for i in range(self.k):
            while True:
                rand=random.randint(0, self.n-1)
                if rand not in dic:
                    centroides.append(self.poblacion[rand])                
                    dic[rand]=1
                    break"""
        cent=[[-0.12293300848913269, 8.197940858866115], [9.947053218490957, -0.6975674085386796], [9.591533658594035, -7.407552627543687], [3.7079497249547195, -8.792991586408998], [0.4522664959026699, 6.0981500948027865], [-4.868512907161257, -0.16920748146691977], [-8.199029435615495, 5.179308090342815], [9.922457533335596, -0.497719340882842], [0.5151398954729185, -4.2703198155086275], [3.702589770726254, -3.3200049788824977], [0.5912719290614117, 4.955550264440161], [6.04775453370749, 0.9769190296446162], [8.464188413408685, -3.7927519994207826], [-7.844739643806415, 2.7871471490160804], [0.4227486922140038, -0.052929778805147265], [5.280102567353076, 8.882908143762695], [-0.819485831742746, 5.588877476672495], [-3.000409968481179, -4.522314880691127], [2.748080733683093, 4.108514983968931], [6.518364569672681, -9.246791075220395]]
        centroides=[]
        for i in range(self.k):
            centroides.append(cent[i])
        # TODO
        #centroides=[[2, 0], [5, 0], [12, 0]]
        #centroides=[[-6.844407445048651, 1.9947857141278398], [5.866124093070791, -3.010404365517683], [1.050669959806287, -4.833642770794762]]
        asignacion=[-1 for i in range(self.n)]
        vueltas=0
        while True: # Hasta que los centroides no cambien
            vueltas+=1
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

            print(centroidesNuevos)

            # 3. Compara los centroides para ver si finaliza la ejecucion
            if(self.compara_centros(centroides,centroidesNuevos)): break
            centroides=centroidesNuevos # No finaliza y se actualizan los centroides

        print(vueltas)
        return asignacion,centroides
    
    # Misma ejecucion pero con euclidea
    def ejecutaE(self):
        # Inicializa centros
        dic={}
        """centroides=[]   # centroides iniciales
        for i in range(self.k):
            while True:
                rand=random.randint(0, self.n-1)
                if rand not in dic:
                    centroides.append(self.poblacion[rand])                
                    dic[rand]=1
                    break"""
        cent=[[-0.12293300848913269, 8.197940858866115], [9.947053218490957, -0.6975674085386796], [9.591533658594035, -7.407552627543687], [3.7079497249547195, -8.792991586408998], [0.4522664959026699, 6.0981500948027865], [-4.868512907161257, -0.16920748146691977], [-8.199029435615495, 5.179308090342815], [9.922457533335596, -0.497719340882842], [0.5151398954729185, -4.2703198155086275], [3.702589770726254, -3.3200049788824977], [0.5912719290614117, 4.955550264440161], [6.04775453370749, 0.9769190296446162], [8.464188413408685, -3.7927519994207826], [-7.844739643806415, 2.7871471490160804], [0.4227486922140038, -0.052929778805147265], [5.280102567353076, 8.882908143762695], [-0.819485831742746, 5.588877476672495], [-3.000409968481179, -4.522314880691127], [2.748080733683093, 4.108514983968931], [6.518364569672681, -9.246791075220395]]
        centroides=[]
        for i in range(self.k):
            centroides.append(cent[i])
        # TODO
        #centroides=[[2, 0], [5, 0], [12, 0]]
        #centroides=[[-6.844407445048651, 1.9947857141278398], [5.866124093070791, -3.010404365517683], [1.050669959806287, -4.833642770794762]]
        asignacion=[-1 for i in range(self.n)]
        vueltas=0
        while True:
            vueltas+=1
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

        print(vueltas)
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

def distancia(a,b):
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
    eval=evaluacion(poblacion, asignacion,centroides,False)    

    print("Mejor Valor:",eval)
    print("Tiempo de ejecucion:",(timeEnd-timeStart))

    plot2D(poblacion,asignacion,k)

    return asignacion

def ejecuta_varios(poblacion, k, tipo, times):
    timeStart=MPI.Wtime()
    ret=float("inf")
    mejor=None
    centroidesMejor=None
    if tipo==0: 
        for _ in range(times):
            kM=KMeans(k, poblacion, False)
            asignacion,centroides=kM.ejecutaM()
            tmp=evaluacion(poblacion, asignacion,centroides,True)
            if tmp<ret:
                ret=tmp
                mejor=asignacion
                centroidesMejor=centroides
    else: 
        for _ in range(times):
            kM=KMeans(k, poblacion, False)
            asignacion,centroides=kM.ejecutaE()
            tmp=evaluacion(poblacion, asignacion,centroides,True)
            if tmp<ret:
                ret=tmp
                mejor=asignacion
                centroidesMejor=centroides
    
    
    timeEnd=MPI.Wtime()
    
    
    #print(asignacion)
    print("Mejor Valor:",ret)
    print("Tiempo de ejecucion:",(timeEnd-timeStart))

    plot2D(poblacion,mejor,k)
    return(mejor)
   

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

    DBs=[davies_bouldin(poblacion, i, mejores[i-1], centroidesMejores[i-1]) for i in range(2,k+1)]    
    dbMejor=calcula_DB_mejor(DBs)
    
    GUI(maxCluster, dbMejor+1, fits,DBs,poblacion,mejores[dbMejor+1]) 
   
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

    DBs=[davies_bouldin(poblacion, i, mejores[i-1], centroidesMejores[i-1]) for i in range(2,k+1)]    
    dbMejor=calcula_DB_mejor(DBs)
    
    GUI(maxCluster, dbMejor+1, fits,DBs,poblacion,mejores[dbMejor+1])


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
    #poblacion=[[1,0], [2,0], [4,0], [5,0], [11,0], [12,0]]#, [14,0], [15,0], [19,0], [20,0], [20.5,0], [21,0]]    
    # 6000      1 generacion de puntos aleatorios
    # 6000_2    2 generaciones de puntos aleatorios
    # 6000_3    6 generaciones de puntos aleatorios
    # 100000_2D    6 generaciones de puntos aleatorios
    #poblacion=lee("100_2D")
    poblacion=lee("100000_2D")
    poblacion=poblacion[0:180]    
    # Numero de clusters ejecutados [1-k]
    k=10
    
    # Variables: poblacion, numero de clusters, manh o eucl
    asignacion=ejecuta_uno(poblacion, k, 1)

    # Variables: poblacion, numero de clusters, manh o eucl, numero de repeticiones del algoritmo
    #asignacion=ejecuta_varios(poblacion, k, 0, 10)


    #ejecuta_busquedaM(poblacion, k, 20)
    #ejecuta_busquedaE(poblacion, k, 8)

main()
