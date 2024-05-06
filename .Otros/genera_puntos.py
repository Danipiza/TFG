import matplotlib.pyplot as plt
from mpi4py import MPI
import random


def genera_puntos(num, mins, maxs):
    puntos=[]
    d=len(maxs)
    for _ in range(num):
        ind=[]
        for a in range(d):
            ind.append(random.uniform(mins[a],maxs[a]))
        
        puntos.append(ind)
    return puntos

def escribe(array, archivo):
    n=len(array)
    m=len(array[0])
    
    with open(archivo, 'w') as file:         
        file.write(str(array[0][0]))
        for j in range(1,m):          
            file.write(", "+str(array[0][j]))

        for i in range(1,n):            
            for j in range(m):          
                file.write(", "+str(array[i][j]))

def plot2D_genereados(points):
    colors=["blue","red","green","black","pink","yellow"]
    i=0
    for p in points:
        x = [point[0] for point in p]
        y = [point[1] for point in p]
        plt.scatter(x, y, color=colors[i])
        i+=1
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2D-Plot Aleatoria')
    
    plt.show()

def plot2D(points,num, clusters):
    colors=["blue","red","green","black","pink","yellow"]
    n=num//clusters
    izq=0
    der=n    
    for i in range(clusters):
        x=[]
        y=[]
        for j in range(izq, der):
            x.append(points[j][0])
            y.append(points[j][1])  
        plt.scatter(x, y, color=colors[i])
        izq+=n
        der+=n
    
    #plt.scatter(points[0:2][0], points[0:2][1], color=colors[0])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2D-Plot Leida')
    
    plt.show()



def lee(archivo, plot):
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
        
    if plot==True:
        plot2D(array,6000,6)
    return array




if __name__ == "__main__":
    array=lee("100000_2D.txt",False)
    escribe(array[0:50000], "50000_2D.txt")
    a=lee("50000_2D.txt",False)
    print(len(a))
    
    
    exit(1)
    num = 250000
    
    """p1 = genera_puntos(num, -12.5, -7.5, -10, -2.5)
    p2 = genera_puntos(num, -2.5, 2.5, -10, -2.5)
    p3 = genera_puntos(num, 7.5, 12.5, -10, -2.5)
    p4 = genera_puntos(num, -12.5, -7.5, 2.5, 10)
    p5 = genera_puntos(num, -2.5, 2.5, 2.5, 10)
    p6 = genera_puntos(num, 7.5, 12.5, 2.5, 10)
    puntos=[p1,p2,p3,p4,p5,p6]"""
    d=2
    mins=[-10 for _ in range(d)]
    maxs=[10 for _ in range(d)]
    p1=genera_puntos(num, mins,maxs)
    puntos=[p1]
    archivo = '250000_{}D.txt'.format(d)
    
    dic={} 
    centroides=[]   # centroides iniciales
    for i in range(50):
        while True:
            rand=random.randint(0, num-1)
            if rand not in dic:
                centroides.append(p1[rand])                
                dic[rand]=1
                break

    print(centroides)

    escribe(puntos, archivo)
    #array=lee(archivo,True)

    #array=lee(archivo,False)
    #plot2D_genereados(puntos)




