from mpi4py import MPI
import sys
import os
import signal
import random


# EJECUTAR
# py RL_2.py

"""
PREPROCESANDO LA MATRIZ
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
    path=os.path.join(dir, ".Otros","ficheros","0.Laberintos", archivo+".txt")
           
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

class Q_Learning():
    
    def __init__(self, alpha,gamma,epsilon, episodios, 
                 Q_table, A_table,
                 matriz,fils,cols):
        # Definir el laberinto 0: vacio, 1: pared
        
        
        self.matriz=matriz
        self.fils=fils
        self.cols=cols
        
        mX=[-1,0,0,1]
        mY=[0,-1,1,0]
        #self.acciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.acciones = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        
        """self.num_acciones = len(self.acciones)"""
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
        """self.Q_table = [[[0 for _ in range(self.num_acciones)] for _ in range(self.cols)] for _ in range(self.fils)]"""
        self.Q_table=Q_table
        self.A_table=A_table

        self.estado_final=(self.fils-2, self.cols-2)


    # Seleciona una accion basada en epsilon-greedy
    def selecciona_accion(self, estado):  
        num_acciones=len(self.A_table[estado[0]][estado[1]])
        
        if random.uniform(0, 1) < self.epsilon:            
            ind=random.randint(0,num_acciones-1)
            return self.A_table[estado[0]][estado[1]][ind], ind
            #return random.randint(0,self.num_acciones-1)
        else:            
            tmp=0
            maximo=self.Q_table[estado[0]][estado[1]][0]
            ind=0		
            #for k in range(1,self.num_acciones):
            for k in range(1,num_acciones):
                tmp=self.Q_table[estado[0]][estado[1]][k]
                if maximo<tmp: 
                    maximo=tmp
                    ind=k
            #return ind
            return self.A_table[estado[0]][estado[1]][ind], ind

    # Actualiza la tabla Q
    def actualiza_Q_table(self, estado, accion, indice, recompensa, sig_estado):
        num_acciones=len(self.A_table[sig_estado[0]][sig_estado[1]])
        
        tmp=0        
        ind=0
        
        maximo=self.Q_table[sig_estado[0]][sig_estado[1]][0]
        
        #for k in range(1,self.num_acciones):
        for k in range(1,num_acciones):
            tmp=self.Q_table[sig_estado[0]][sig_estado[1]][k]
            if maximo<tmp: 
                maximo=tmp
                ind=k
        
        self.Q_table[estado[0]][estado[1]][indice]=(1-self.alpha)*self.Q_table[estado[0]][estado[1]][indice] + \
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
                while estado != self.estado_final:  
                    
                    accion, indice=self.selecciona_accion(estado)
                    Estados[i]=estado
                    Acciones[i]=accion
                    i=(i+1)%10

                    #if self.accion_valida(estado, self.acciones[accion]):
                    sig_estado = (estado[0] + self.acciones[accion][0], estado[1] + self.acciones[accion][1])
                    
                    """if self.matriz[sig_estado[0]][sig_estado[1]] == 1: 
                        recompensa = self.recompensas['pared']"""
                    if sig_estado == self.estado_final: 
                        recompensa = self.recompensas['destino']
                    else: recompensa = self.recompensas['otro']
                    
                    self.actualiza_Q_table(estado, accion, indice, recompensa, sig_estado)
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
        print("\n M{}X{}\nHa terminado el entrenamiento en: {} \n".format(self.fils, self.cols,
                                                                          timeEndEnt-timeStart))

        # Evaluación del Agente
        i=0
        Estados=[(0,0) for _ in range(10)]
        Acciones=[0 for _ in range(10)]
        try:
            estado=(1, 1) # Numero aleatorio
            accion, indice=self.selecciona_accion(estado)
            
            while estado != self.estado_final:
                Estados[i]=estado
                Acciones[i]=accion
                i=(i+1)%10
                
                tmp=0
                
                maximo=self.Q_table[estado[0]][estado[1]][0]
                accion=0		
                num_acciones=len(self.A_table[estado[0]][estado[1]])
                #for k in range(1,self.num_acciones):
                for k in range(1,num_acciones):
                    tmp=self.Q_table[estado[0]][estado[1]][k]
                    if maximo<tmp: 
                        maximo=tmp
                        accion=k
               
                #if self.accion_valida(estado, self.acciones[accion]): 
                estado = (estado[0] + self.acciones[self.A_table[estado[0]][estado[1]][accion]][0], 
                          estado[1] + self.acciones[self.A_table[estado[0]][estado[1]][accion]][1])
                
                
            timeEnd=MPI.Wtime()
            print("Ejecucion final:", (timeEnd-timeEndEnt))
        except KeyboardInterrupt:
            print(Estados)            
            print(Acciones)  
            print(self.Q_table[Estados[0][0]][Estados[0][1]])
            sys.exit(0)

def procesarMatriz(matriz,fils,cols):
    """
    COSTE CUADRATICO O(4N^2) = O(N^2)
    Para cada celda revisa las 4 acciones disponibles si no es un muro
    """
    table=[]
    acciones=[]

    # ACCIONES: 0: N    1: O    2: E    3: S
    mX=[-1,0,0,1]
    mY=[0,-1,1,0]

    for i in range(fils):
        filaQ=[]
        filaA=[]
        for j in range(cols):
            celdaQ=[]
            celdaA=[]
            if matriz[i][j]==0:                
                for k in range(4):                    
                    if matriz[i+mX[k]][j+mY[k]]==0: 
                        celdaQ.append(0)
                        celdaA.append(k)

            filaQ.append(celdaQ)
            filaA.append(celdaA)
        table.append(filaQ)
        acciones.append(filaA)
    
    return table, acciones

def main():
    # 30 y 50
    alpha=0.5
    gamma=0.9
    epsilon=0.8
    episodios=1000
    # 100
    """
    # FUNCIONA A VECES
    alpha=0.3
    gamma=0.9
    epsilon=0.8
    episodios=1000"""
    
    alpha=0.3
    gamma=0.9
    epsilon=0.8
    episodios=1000
    archivo="75"
    matriz,fils,cols=leeArchivo(archivo)

    timeStart=MPI.Wtime()
    Q_table,A_table=procesarMatriz(matriz,fils,cols)
    
    timeEndEnt=MPI.Wtime()

    QL=Q_Learning(alpha,gamma,epsilon,episodios, 
                  Q_table, A_table,
                  matriz,fils,cols)
    QL.ejecuta()
    #print(QL.Q_table)



main()