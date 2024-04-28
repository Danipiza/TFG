from mpi4py import MPI
import sys
import os
import signal
import random

"""
MEJORAS:

RECORRER QTABLE E INICIALIZAR A UN NUMERO NEGATIVO LAS ACCIONES QUE SE PEGAN CON UN MURO

PONER VARIOS WORKERS EN SECCIONES DE LA MATRIZ Y HACER QUE SE MUEVAN

DISTRIBUIR LOS EPISODIOS ENTRE WORKERS

PONER DESDE VARIOS PUNTOS AL AGENTE

"""



def signal_handler(sig, frame):
    print("Ctrl+C\n")    
    sys.exit(0)

def leeArchivo():
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

    nombre_fichero=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","Laberintos", nombre_fichero+".txt")
           
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
        print("El archivo '{}' no existe.".format(nombre_fichero+".txt"))
    
    return M, filas, columnas

class Q_Learning():
    
    def __init__(self):
        # Definir el laberinto 0: vacio, 1: pared
        
        self.matriz,self.fils,self.cols=leeArchivo()
        
        self.acciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
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
        self.alpha = 0.3  # Tasa de aprendizaje
        self.gamma = 0.9  # Factor de descuento
        self.epsilon = 0.1  # Factor de exploración

        self.episodios=500

        # Inicializar la Q table
        self.Q_table = [[[0 for _ in range(self.num_acciones)] for _ in range(self.cols)] for _ in range(self.fils)]

        self.estado_final=(self.fils-2, self.cols-2)

    def recorreQTable(self):        
        # Comprueba muros
        for i in range(self.fils):
            for j in range(self.cols):
                if self.matriz[i][j]==1:    
                    for k in range(self.num_acciones):
                        self.Q_table[i][j][k]=-100000
                    continue
                for k in range(self.num_acciones):
                    if self.matriz[i+self.acciones[k][0]][j+self.acciones[k][1]]==1:
                        self.Q_table[i][j][k]=-1000


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
                while estado != self.estado_final:  
                    
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
        print("Ha terminado el entrenamiento")
        timeEndEnt=MPI.Wtime()
        print("Ha terminado el entrenamiento en:", (timeEndEnt-timeStart))

        # Evaluación del Agente
        i=0
        Estados=[(0,0) for _ in range(10)]
        Acciones=[0 for _ in range(10)]
        try:
            estado = (1, 1) # Numero aleatorio
            print(self.Q_table[1][1])
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


QL=Q_Learning()
timeStart=MPI.Wtime()
QL.recorreQTable()
timeEnd=MPI.Wtime()
print("Tiempo de Ejecucion",(timeEnd-timeStart))