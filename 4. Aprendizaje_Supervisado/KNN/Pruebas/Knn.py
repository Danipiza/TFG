import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI
import random
import os
import math

import queue

# Tiempo de ejecucion total: 9.944005100056529 10000_2D, 1000_2D, k=3

class MaxPriorityQueue(queue.PriorityQueue):
    def __init__(self):
        super().__init__()

    def push(self, item, priority):
        super().put((-priority, item))

    def top_distancia(self):
        priority, _ = self.queue[0]  
        return -priority
    
    def top_etiqueta(self):
        _, item = self.queue[0]  
        return item
    
    def pop(self):
        _, item = super().get()
        return item
    
    def size(self):
        return self.qsize()

    


def lee(archivo):

    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".Otros","ficheros","2.Cluster", archivo+".txt")

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

def leeAsig(archivo):
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
    
    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)
        
    if archivo==None: nombre_fichero=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir,".Otros","ficheros","2.Cluster","Asig", archivo+".txt")
  
        
    array = [] 
    try:        
        with open(path, 'r') as archivo: # modo lectura
            for linea in archivo: # Solo hay una linea                
                numeros_en_linea = linea.split() # Divide por espacios                               
                for numero in numeros_en_linea:
                    array.append(int(numero))
    
    except FileNotFoundError:
        print("El archivo '{}' no existe.".format(nombre_fichero+".txt"))
    
    return array





"""
k>cluster, para que no haya posibles empates
"""
def knn_clasificador_unoE(poblacion, asignacion, clusters, individuo, k):
    n=len(poblacion)
    d=len(poblacion[0])
    pq = MaxPriorityQueue()

    

    #print("Asignacion=",asignacion)
    
    # Calcula todas las distancias y coge las k mas cercanas
    for i in range(n):
        distancia=0
        for j in range(d):
            distancia+=(poblacion[i][j]-individuo[j])**2    
        distancia=math.sqrt(distancia)
        
        
        #print("TopD={}, TopE={}".format(pq.top_distancia(),pq.top_etiqueta()))
        # Si la cola de prioridad no es k, añadir la distancia
        if pq.size()<k: pq.push(asignacion[i],distancia)
        # Si distancia actual es menor a la mayor menor, 
        # se elimina la mayor e introduce la actual        
        elif pq.top_distancia()>distancia:            
            pq.pop()
            pq.push(asignacion[i],distancia)

    # Cuenta el numero de vecinos mas cercanos para cada cluster
    etiquetas=[0 for i in range(clusters)]    
    for i in range(k):
        etiquetas[pq.pop()]+=1
    
    # Coge el que mas tenga
    ret=0
    cantidad=etiquetas[0]
    for i in range(1,clusters):
        if cantidad<etiquetas[i]:
            cantidad=etiquetas[i]
            ret=i
               
	
    return ret

def ejecuta_actualizarE(poblacion, asignacion, n, poblacionProbar, m, clusters, k):    
 


    d=len(poblacion[0])

    asignacionProbar=[]    
    for x in range(m):                          
        pq = MaxPriorityQueue()        

        
        # Calcula todas las distancias y coge las k mas cercanas
        for i in range(n):
            distancia=0
            for j in range(d):
                distancia+=(poblacion[i][j]-poblacionProbar[x][j])**2    
            distancia=math.sqrt(distancia)            
            
            # Si la cola de prioridad no es k, añadir la distancia
            if pq.size()<k: pq.push(asignacion[i],distancia)
            # Si distancia actual es menor a la mayor menor, 
            # se elimina la mayor e introduce la actual        
            elif pq.top_distancia()>distancia:            
                pq.pop()
                pq.push(asignacion[i],distancia)

        # Cuenta el numero de vecinos mas cercanos para cada cluster
        etiquetas=[0 for i in range(clusters)]    
        for i in range(k):
            etiquetas[pq.pop()]+=1
        
        # Coge el que mas tenga
        ret=0
        cantidad=etiquetas[0]
        for i in range(1,clusters):
            if cantidad<etiquetas[i]:
                cantidad=etiquetas[i]
                ret=i                
        
        asignacionProbar.append(ret)
        poblacion.append(poblacionProbar[x])
        asignacion.append(ret)
        n+=1
   
# Ejecuta sin almacenar 
def ejecuta_sin_actualizarE(poblacionIni, asignacionIni, n, poblacionProbar, m, clusters, k):    
    
        
    asignacionProbar=[]
    for i in range(m):           
        asignacionProbar.append(knn_clasificador_unoE(poblacionIni, asignacionIni, clusters, poblacionProbar[i],k))


"""
k>cluster, para que no haya posibles empates
"""
def knn_clasificador_unoM(poblacion, asignacion, clusters, individuo, k):
    n=len(poblacion)
    d=len(poblacion[0])
    pq = MaxPriorityQueue()

    

    #print("Asignacion=",asignacion)
    
    # Calcula todas las distancias y coge las k mas cercanas
    for i in range(n):
        distancia=0
        for j in range(d):
            distancia+=abs(poblacion[i][j]-individuo[j])
        
        
        #print("TopD={}, TopE={}".format(pq.top_distancia(),pq.top_etiqueta()))
        # Si la cola de prioridad no es k, añadir la distancia
        if pq.size()<k: pq.push(asignacion[i],distancia)
        # Si distancia actual es menor a la mayor menor, 
        # se elimina la mayor e introduce la actual        
        elif pq.top_distancia()>distancia:            
            pq.pop()
            pq.push(asignacion[i],distancia)

    # Cuenta el numero de vecinos mas cercanos para cada cluster
    etiquetas=[0 for i in range(clusters)]    
    for i in range(k):
        etiquetas[pq.pop()]+=1
    
    # Coge el que mas tenga
    ret=0
    cantidad=etiquetas[0]
    for i in range(1,clusters):
        if cantidad<etiquetas[i]:
            cantidad=etiquetas[i]
            ret=i
               
	
    return ret

def ejecuta_actualizarM(poblacion, asignacion, n, poblacionProbar, m, clusters, k):    


    d=len(poblacion[0])

    asignacionProbar=[]    
    for x in range(m):                          
        pq = MaxPriorityQueue()        

        
        # Calcula todas las distancias y coge las k mas cercanas
        for i in range(n):
            distancia=0
            for j in range(d):
                distancia+=abs(poblacion[i][j]-poblacionProbar[x][j])      
            
            # Si la cola de prioridad no es k, añadir la distancia
            if pq.size()<k: pq.push(asignacion[i],distancia)
            # Si distancia actual es menor a la mayor menor, 
            # se elimina la mayor e introduce la actual        
            elif pq.top_distancia()>distancia:            
                pq.pop()
                pq.push(asignacion[i],distancia)

        # Cuenta el numero de vecinos mas cercanos para cada cluster
        etiquetas=[0 for i in range(clusters)]    
        for i in range(k):
            etiquetas[pq.pop()]+=1
        
        # Coge el que mas tenga
        ret=0
        cantidad=etiquetas[0]
        for i in range(1,clusters):
            if cantidad<etiquetas[i]:
                cantidad=etiquetas[i]
                ret=i                
        
        asignacionProbar.append(ret)
        poblacion.append(poblacionProbar[x])
        asignacion.append(ret)
        n+=1

# Ejecuta sin almacenar 
def ejecuta_sin_actualizarM(poblacionIni, asignacionIni, n, poblacionProbar, m, clusters, k):    
    totalTimeStart = MPI.Wtime()
        
    asignacionProbar=[]
    for i in range(m):           
        asignacionProbar.append(knn_clasificador_unoM(poblacionIni, asignacionIni, clusters, poblacionProbar[i],k))
    
    totalTimeEnd = MPI.Wtime()
      
    



def main():
    # 100_1_2D 7
    poblacionIni=lee("1000_1_2D")
    asignacionIni=leeAsig("1000_1_2D") 
    n=len(poblacionIni)    
    
    poblacionProbar=lee("100000_2D")
    m=len(poblacionProbar)

    clusters=4
    k=10
    
    procesar=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750, 9000, 9250, 9500, 9750, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]
    procesar_k=[2,4,6,8,10,15,20,30,50,100]    

    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_Act=os.path.join(directorio_script, 'Actualiza')
    ruta_NoAct=os.path.join(directorio_script, 'No_Actualiza')
    ruta_Tam=os.path.join(directorio_script, 'Tam_Datos.txt')
    
    for x in procesar:
        ini=[]
        iniAsig=[]
        for y in poblacionIni:
            ini.append(y)
        for y in asignacionIni:
            iniAsig.append(y)

        for k in procesar_k:
            # ---------------------------------------------------------------------------
            # --- MANHATTAN -------------------------------------------------------------
            # ---------------------------------------------------------------------------
            totalTimeStart = MPI.Wtime()
            ejecuta_sin_actualizarM(ini, iniAsig, n, 
                                poblacionProbar[0:x+1], x, clusters, k)
            totalTimeEnd = MPI.Wtime()
            if k!=100: print("(k={}) Manhattan_NoAct:\t\t{}".format(k,totalTimeEnd-totalTimeStart))
            else: print("(k={}) Manhattan_NoAct:\t{}".format(k,totalTimeEnd-totalTimeStart))
            
            ruta=os.path.join(ruta_NoAct,'KNN_NoAct_k{}_M.txt'.format(k))  
            with open(ruta, 'a') as archivo:                              
                archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')

            # ---------------------------------------------------------------------------
            # --- EUCLIDEA --------------------------------------------------------------
            # ---------------------------------------------------------------------------
            totalTimeStart = MPI.Wtime()
            ejecuta_sin_actualizarE(ini, iniAsig, n, 
                                poblacionProbar[0:x+1], x, clusters, k)
            totalTimeEnd = MPI.Wtime()
            print("(k={}) Euclidea_NoAct:\t\t{}".format(k,totalTimeEnd-totalTimeStart))
            
            
            ruta=os.path.join(ruta_NoAct,'KNN_NoAct_k{}_E.txt'.format(k))  
            with open(ruta, 'a') as archivo:                               
                archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')
        

        for k in procesar_k:
            # ---------------------------------------------------------------------------
            # --- MANHATTAN -------------------------------------------------------------
            # ---------------------------------------------------------------------------
            totalTimeStart = MPI.Wtime()
            ejecuta_actualizarM(ini, iniAsig, n, 
                                poblacionProbar[0:x+1], x, clusters, k)
            totalTimeEnd = MPI.Wtime()
            print("(k={}) Manhattan_Act:\t\t{}".format(k,totalTimeEnd-totalTimeStart))
            

            ruta=os.path.join(ruta_Act,'KNN_Act_k{}_M.txt'.format(k))  
            with open(ruta, 'a') as archivo:                      
                archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')

            # ---------------------------------------------------------------------------
            # --- EUCLIDEA --------------------------------------------------------------
            # ---------------------------------------------------------------------------
            totalTimeStart = MPI.Wtime()
            ejecuta_actualizarE(ini, iniAsig, n, 
                                poblacionProbar[0:x+1], x, clusters, k)
            totalTimeEnd = MPI.Wtime()
            print("(k={}) Euclidea_Act:\t\t{}".format(k,totalTimeEnd-totalTimeStart))
           

            ruta=os.path.join(ruta_Act,'KNN_Act_k{}_E.txt'.format(k))  
            with open(ruta, 'a') as archivo:                              
                archivo.write(str(totalTimeEnd-totalTimeStart) + ', ')

        print()
        
        with open(ruta_Tam, 'a') as archivo:                               
                archivo.write(str(x) + ', ')


main()