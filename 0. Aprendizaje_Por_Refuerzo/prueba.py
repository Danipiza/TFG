#from mpi4py import MPI
import sys
import os
import signal
import random
import numpy

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
        """self.matriz = ([[1, 1, 1, 1, 1, 1, 1],
                        [1, 0, 1, 0, 0, 0, 1],
                        [1, 0, 1, 0, 1, 0, 1],
                        [1, 0, 0, 0, 1, 0, 1],
                        [1, 0, 1, 1, 1, 0, 1],
                        [1, 0, 0, 0, 1, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1]])"""
        
        self.matriz,self.fils,self.cols=leeArchivo()
        
        self.acciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        self.fils = len(self.matriz)
        self.cols = len(self.matriz[0])
        self.num_acciones = len(self.acciones)
        # Definir acciones (arriba, abajo, izquierda, derecha)
        

        # Definir recompensas
        self.recompensas = {
            'destino': 100,
            'pared': -10,
            'otro': -1}

        # Parametros de aprendizaje
        self.alpha = 0.1  # Tasa de aprendizaje
        self.gamma = 0.9  # Factor de descuento
        self.epsilon = 0.1  # Factor de exploración

        # Inicializar la Q table
        self.Q_table = [[[0 for _ in range(self.num_acciones)] for _ in range(self.cols)] for _ in range(self.fils)]

        self.estado_final=(self.fils-2, self.cols-2)


    # Seleciona una accion basada en epsilon-greedy
    def selecciona_accion(self, estado):
        import random
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(range(self.num_acciones))
        else:
            return max(range(self.num_acciones), key=lambda x: self.Q_table[estado[0]][estado[1]][x])

    # Actualiza la tabla Q
    def actualiza_Q_table(self, estado, accion, recompensa, sig_estado):
        best_next_action = max(range(self.num_acciones), key=lambda x: self.Q_table[sig_estado[0]][sig_estado[1]][x])
        self.Q_table[estado[0]][estado[1]][accion] += self.alpha * (recompensa + self.gamma * self.Q_table[sig_estado[0]][sig_estado[1]][best_next_action] - self.Q_table[estado[0]][estado[1]][accion])

    # Dentro del tablero, y no es pared
    def accion_valida(self, estado, accion):
        sig_estado = (estado[0] + accion[0], estado[1] + accion[1])
        return 0 <= sig_estado[0] < self.fils and 0 <= sig_estado[1] < self.cols and self.matriz[sig_estado[0]][sig_estado[1]] == 0


    def entrenamiento(self, episodios):
        
        for ep in range(episodios):
            estado = (1, 1)
            # Hasta que el agente llegue al objetivo
            while estado != self.estado_final:  
                accion = self.selecciona_accion(estado)
                if self.accion_valida(estado, self.acciones[accion]):
                    sig_estado = (estado[0] + self.acciones[accion][0], estado[1] + self.acciones[accion][1])
                    if self.matriz[sig_estado[0]][sig_estado[1]] == 1: 
                        recompensa = self.recompensas['pared']
                    elif sig_estado == self.estado_final: 
                        recompensa = self.recompensas['destino']
                    else: 
                        recompensa = self.recompensas['otro']
                    self.actualiza_Q_table(estado, accion, recompensa, sig_estado)
                    estado = sig_estado
            print("Ha terminado el episodio:",ep)

    def ejecuta(self):

        self.entrenamiento(100)
        print("Ha terminado el entrenamiento")

        # Evaluación del Agente
        
        estado = (1, 1) # Numero aleatorio
        while estado != self.estado_final:
            accion = max(range(self.num_acciones), key=lambda x: self.Q_table[estado[0]][estado[1]][x])
            if self.accion_valida(estado, self.acciones[accion]):
                estado = (estado[0] + self.acciones[accion][0], estado[1] + self.acciones[accion][1])
                print(f"Siguiente accion: {self.acciones[accion]}, Siguiente estado: {estado}")
            else:
                print("No puede avanzar")
                break


QL=Q_Learning()
QL.ejecuta()
