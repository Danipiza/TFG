from mpi4py import MPI
import os
import math

# mpiexec -np 5 python iniM.py

def lee(archivo):

    dir=os.getcwd()
    n=len(dir)

    while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","Cluster", archivo+".txt")

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
"""
def dist(a,b): 
    ret=0.0
    for i in range(len(a)):
        ret+=abs(a[i]-b[i])
    return ret 

#poblacion=lee("10000_2D")


#n = len(poblacion)
n=2000
print(n)

M=[]
t1S=MPI.Wtime()
#a=[(0) for _ in range(n)]
#for _ in range(n):
#    M.append(a)
M=[[0 for _ in range(n)] for _ in range(n)]
t1E=MPI.Wtime()
print("Tiempo Genera: {}".format((t1E-t1S)))"""


"""t2S=MPI.Wtime()
c2=1
# Borra Fila
M.pop(c2)
# Borra Columna
for row in M:
    del row[c2]

t2E=MPI.Wtime()

print("Tiempo Borra col y fila: {}".format((t2E-t2S)))"""



def distancia(a,b):
    ret=0.0
    for i in range(len(a)):
        ret+=(a[i]-b[i])**2        
    
    return math.sqrt(ret)

poblacion=lee("10000_2D")
n=len(poblacion)
d=len(poblacion[0])

print("Ejecutando Init Matriz{}x{} (con calculo de distancias)".format(n,n))
t3S=MPI.Wtime()


data=[]
for i in range(n):
    tmp=[0 for _ in range(i+1)]      
    for j in range(i+1, n):
        aux=0.0
        for a in range(d):
            aux+=(poblacion[i][a]-poblacion[j][a])**2     
        tmp.append(math.sqrt(aux))
    data.append(tmp)

t3E=MPI.Wtime()

print("Tiempo de Ejecucion: {}".format((t3E-t3S)))