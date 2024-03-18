import matplotlib.pyplot as plt
from mpi4py import MPI
import random


def genera_puntos(num, x_min, x_max, y_min, y_max):
    puntos = []
    for _ in range(num):
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        puntos.append([x, y])
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
    num = 1000
    
    p1 = genera_puntos(num, -1400, -400, -600, -100)
    p2 = genera_puntos(num, -500, 500, -600, -100)
    p3 = genera_puntos(num, 400, 1400, -600, -100)
    p4 = genera_puntos(num, -1400, -400, 100, 600)
    p5 = genera_puntos(num, -500, 500, 100, 600)
    p6 = genera_puntos(num, 400, 1400, 100, 600)
    puntos=[p1,p2,p3,p4,p5,p6]   
    archivo = '6000_3.txt'
    
    escribe(puntos, archivo)
    array=lee(archivo,True)

    array=lee(archivo,False)
    plot2D_genereados(puntos)




