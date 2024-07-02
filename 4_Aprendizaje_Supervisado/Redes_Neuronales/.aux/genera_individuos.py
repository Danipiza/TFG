import matplotlib.pyplot as plt
from mpi4py import MPI
import random

def genera_inds1():
    puntos=[]
    altura=150
    while altura<200:
        peso=altura-115
        for _ in range(8):
            puntos.append([altura/100,peso,round((peso/(altura/100)**2),2)])
            peso+=5
        altura+=5
    return puntos

def genera_inds2():
    puntos=[]
    altura=150
    while altura<200:
        peso=(18*(altura/100)**2)//1
        IMC=round((peso/(altura/100)**2),2)
        while IMC<31:            
            puntos.append([altura/100,peso,IMC])
            peso+=1
            IMC=round((peso/(altura/100)**2),2)
        altura+=1
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
        


if __name__ == "__main__":
       
    p1=genera_inds2()
    #print(len(p1))
    archivo = 'datos2042.txt'
    
    escribe([p1], archivo)




