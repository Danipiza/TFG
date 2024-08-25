from mpi4py import MPI
import sys
import os
import signal
import random

import tkinter as tk

# EJECUTAR
# py RL_1.py

"""
Programa de Aprendizaje por Refuerzo (RL)

Sin preprocesar la matriz
"""


def signal_handler(sig, frame):
    print("Ctrl+C\n")    
    sys.exit(0)

def leeArchivo(archivo):
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

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".otros","ficheros","0_Laberintos", archivo+".txt")
           
    filas=0
    columnas=0 
    M=[]
    
    try:        
        with open(path, 'r') as archivo: # modo lectura
            for linea in archivo:                                
                filas+=1
                columnas=0
                array = [] 
                numeros_en_linea = linea.split() # Divide por espacios                                              
                for numero in numeros_en_linea:
                    array.append(int(numero))
                    columnas+=1
                M.append(array)
                
    
    except FileNotFoundError:
        print("El archivo '{}' no existe.".format(archivo+".txt"))
    
    return M, filas, columnas

def escribir_matriz(nombre, matriz):

    with open(nombre, 'w') as acrhivo:
        for fila in matriz:
            acrhivo.write(' '.join(map(str, fila))+'\n')

def leer_matriz(nombre):
    ret=[]

    with open(nombre, 'r') as archivo:        
        for linea in archivo:
            fila=list(map(float, linea.split()))
            ret.append(fila)

    return ret


class Q_Learning():
    
    def __init__(self, alpha,gamma,epsilon, episodios, archivo):
        # Definir el laberinto 0: vacio, 1: pared
        
        self.matriz,self.fils,self.cols=leeArchivo(archivo)
        
        self.acciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # mapa de calor 
        self.matriz_calor=[[0 for _ in range(self.cols)] for _ in range(self.fils)]        
        for i in range(self.fils):
            for j in range(self.cols):
                if self.matriz[i][j]==1: self.matriz_calor[i][j]=-1


        
        #self.fils = len(self.matriz)
        #self.cols = len(self.matriz[0])
        self.num_acciones = len(self.acciones)
        # Definir acciones (arriba, abajo, izquierda, derecha)
        

        # Definir recompensas
        self.recompensas = {
            'destino': 100,
            'pared': -10,
            'otro': -1}

        # Parametros de aprendizaje
        #self.alpha = 0.3  # Tasa de aprendizaje
        self.alpha = alpha
        #self.gamma = 0.9  # Factor de descuento
        self.gamma = gamma  
        
        #self.epsilon = 0.1  # Factor de exploración
        self.epsilon=epsilon

        #self.episodios=2500
        self.episodios=episodios

        # Inicializar la Q table
        self.Q_table = [[[0 for _ in range(self.num_acciones)] for _ in range(self.cols)] for _ in range(self.fils)]

        self.estado_final=(self.fils-2, self.cols-2)
        print(self.matriz[self.fils-2][self.cols-2])


    # Seleciona una accion basada en epsilon-greedy
    def selecciona_accion(self, estado):        
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0,self.num_acciones-1)
        else:
            #return max(range(self.num_acciones), key=lambda x: self.Q_table[estado[0]][estado[1]][x])
            tmp=0
            maximo=self.Q_table[estado[0]][estado[1]][0]
            ind=0		
            for k in range(1,self.num_acciones):
                tmp=self.Q_table[estado[0]][estado[1]][k]
                if maximo<tmp: 
                    maximo=tmp
                    ind=k
            return ind

    # Actualiza la tabla Q
    def actualiza_Q_table(self, estado, accion, recompensa, sig_estado):
        tmp=0        
        ind=0
        maximo=self.Q_table[sig_estado[0]][sig_estado[1]][0]
        for k in range(1,self.num_acciones):
            tmp=self.Q_table[sig_estado[0]][sig_estado[1]][k]
            if maximo<tmp: 
                maximo=tmp
                ind=k
        
        self.Q_table[estado[0]][estado[1]][accion]=(1-self.alpha)*self.Q_table[estado[0]][estado[1]][accion] + \
                                                    self.alpha*(recompensa + self.gamma*self.Q_table[sig_estado[0]][sig_estado[1]][ind] )
        #self.Q_table[estado[0]][estado[1]][accion] += self.alpha*(recompensa + self.gamma * self.Q_table[sig_estado[0]][sig_estado[1]][ind] - \
		#											self.Q_table[estado[0]][estado[1]][accion])

    # Dentro del tablero, y no es pared
    def accion_valida(self, estado, accion):
        sig_estado = (estado[0] + accion[0], estado[1] + accion[1])
        return 0 <= sig_estado[0] < self.fils and 0 <= sig_estado[1] < self.cols 


    def entrenamiento(self, episodios):
        i=0
        Estados=[(0,0) for _ in range(10)]
        Acciones=[0 for _ in range(10)]
        try:
            for ep in range(episodios):
                estado = (1, 1)
                #estado = (self.fils-1, 1)
                #estado = (1, self.cols-1)
                #estado = (self.fils//2, self.cols//2)
                
                while estado != self.estado_final: 
                    # mapa de calor 
                    self.matriz_calor[estado[0]][estado[1]]+=1
                    
                    accion = self.selecciona_accion(estado)
                    Estados[i]=estado
                    Acciones[i]=accion
                    i=(i+1)%10

                    if self.accion_valida(estado, self.acciones[accion]):
                        sig_estado = (estado[0] + self.acciones[accion][0], estado[1] + self.acciones[accion][1])
                        if self.matriz[sig_estado[0]][sig_estado[1]] == 1: 
                            recompensa = self.recompensas['pared']
                        elif sig_estado == self.estado_final: 
                            recompensa = self.recompensas['destino']
                        else: recompensa = self.recompensas['otro']
                        self.actualiza_Q_table(estado, accion, recompensa, sig_estado)
                        if self.matriz[sig_estado[0]][sig_estado[1]]!=1: estado = sig_estado
                print("Ha terminado el episodio:",ep)
        except KeyboardInterrupt:
            print(Estados)            
            print(Acciones)  
            print(self.Q_table[Estados[0][0]][Estados[0][1]])
            sys.exit(0)

    def ejecuta(self):
        timeStart=MPI.Wtime()
        self.entrenamiento(self.episodios)        
        timeEndEnt=MPI.Wtime()
        print("Ha terminado el entrenamiento en: {} \n".format(timeEndEnt-timeStart))

        """
        # Evaluación del Agente
        i=0
        Estados=[(0,0) for _ in range(10)]
        Acciones=[0 for _ in range(10)]
        try:
            estado = (1, 1) # Numero aleatorio
            accion = self.selecciona_accion(estado)
            
            while estado != self.estado_final:
                Estados[i]=estado
                Acciones[i]=accion
                i=(i+1)%10
                
                tmp=0
                maximo=self.Q_table[estado[0]][estado[1]][0]
                accion=0		
                for k in range(1,self.num_acciones):
                    tmp=self.Q_table[estado[0]][estado[1]][k]
                    if maximo<tmp: 
                        maximo=tmp
                        accion=k
                #accion = self.selecciona_accion(estado)                
                #accion = max(range(self.num_acciones), key=lambda x: self.Q_table[estado[0]][estado[1]][x])
                
                #and self.matriz[estado[0]+self.acciones[accion][0]][estado[1]+self.acciones[accion][1]] != 1
                if self.accion_valida(estado, self.acciones[accion]): 
                    estado = (estado[0] + self.acciones[accion][0], estado[1] + self.acciones[accion][1])
                    #print(f"Siguiente accion: {self.acciones[accion]}, Siguiente estado: {estado}")
                
            timeEnd=MPI.Wtime()
            print("Ejecucion final:", (timeEnd-timeEndEnt))
        except KeyboardInterrupt:
            print(Estados)            
            print(Acciones)  
            print(self.Q_table[Estados[0][0]][Estados[0][1]])
            sys.exit(0)
        """
    def guarda_mapa_calor(self):
        try:        
            with open("mapa_calor_10reps.txt", 'w') as archivo: # modo escritura
                for fila in self.matriz_calor:
                    for x in fila:
                        archivo.write("{} ".format(x))
                    archivo.write("\n")
                
        except FileNotFoundError:
            print("El archivo 'mapa_calor.txt' no existe.")           

def media_matrices(fichero1, fichero2, fichero3, fichero4, fichero_salida):
    
    M1=leer_matriz(fichero1)
    M2=leer_matriz(fichero2)
    M3=leer_matriz(fichero3)
    M4=leer_matriz(fichero4)

    filas=len(M1)
    columnas=len(M1[0])

    ret=[[0.0 for _ in range(columnas)] for _ in range(filas)]

    for i in range(filas):
        for j in range(columnas):
            ret[i][j]=(M1[i][j]+M2[i][j]+M3[i][j]+M4[i][j])/4.0

    escribir_matriz(fichero_salida, ret)

def compara_matrices(fichero1, fichero2, fichero_salida):
    
    M1=leer_matriz(fichero1)
    M2=leer_matriz(fichero2)
    
    filas=len(M1)
    columnas=len(M1[0])

    ret = [[-1 for _ in range(columnas)] for _ in range(filas)]

    for i in range(filas):
        for j in range(columnas):            
            if M1[i][j]>M2[i][j]: ret[i][j]=0
            elif M1[i][j]<M2[i][j]: ret[i][j]=1

    escribir_matriz(fichero_salida, ret)

def mostrar_mapa(fichero):
    
    M=leer_matriz(fichero)

    root=tk.Tk()
    root.title("Visualizacion del mapa")

    filas=len(M)
    columnas=len(M[0])

    canvas=tk.Canvas(root, width=columnas*5, height=filas*5)
    canvas.pack()

    # 5x5 pixeles
    cell_size=5 

    # Dibujar en canvas
    for i in range(filas):
        for j in range(columnas):
            tmp=M[i][j]

            # color
            if tmp==-1:  color="black"
            elif tmp==0: color="red"
            elif tmp==2: color="yellow"
            else:        color="green"

            # posicion
            x1=j*cell_size
            y1=i*cell_size
            x2=x1+cell_size
            y2=y1+cell_size

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    # bucle principal de la GUI
    root.mainloop()

def main():
    # 30 y 50
    alpha=0.3
    gamma=0.9
    epsilon=0.1
    episodios=100
    # 100
    """
    # FUNCIONA A VECES
    alpha=0.3
    gamma=0.9
    epsilon=0.8
    episodios=1000"""
    """alpha=0.3
    gamma=0.9
    epsilon=0.8
    episodios=1000"""

    alpha=0.5
    gamma=0.9
    epsilon=0.8
    episodios=10
    

    """QL=Q_Learning(alpha,gamma,epsilon,episodios, "100")
    QL.ejecuta()"""
    
    #QL.guarda_mapa_calor()

    #media_matrices("paralelo1.txt","paralelo2.txt","paralelo3.txt","paralelo4.txt","paralelo.txt")
    #compara_matrices("secuencial.txt","paralelo.txt","matriz_comparacion.txt")
    mostrar_mapa("matriz_comparacion.txt")



main()