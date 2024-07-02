from mpi4py import MPI
import sys
import os
import signal
import random

# EJECUTAR
# mpiexec -np 5 python RL_MPI_2_1.py

"""
INTENTO DE MEJORA:

CADA WORKER EJECUTA SU ENTRENAMIENTO DIVIDIENDO EL NUMERO DE EPISODIOS.
    CADA WORKER INICIA EN PUNTOS DIFERENTES (AL MENOS 1 EN EL PUNTO DE ORIGEN DE LA EVALUACION)

CUANDO TERMINAN LE PASAN LAS Q-TABLE AL MASTER Y ESTE HACE LA MEDIA Y EJECUTA LA EVALUACION
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


class Q_Learning():
    
    def __init__(self, alpha,gamma,epsilon, episodios, 
                 Q_table, A_table, estado_inicial,
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

        if estado_inicial==None: self.estado_inicial=(1,1)
        else: self.estado_inicial=estado_inicial

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
       
        for ep in range(episodios):
            #estado = (1, 1)
            estado=self.estado_inicial
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
            
    def ejecuta(self):
        timeStart=MPI.Wtime()
        self.entrenamiento(self.episodios)        
        timeEndEnt=MPI.Wtime()
        

        # Evaluación del Agente
        i=0
        Estados=[(0,0) for _ in range(10)]
        Acciones=[0 for _ in range(10)]
        
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
            
    
    def evalua(self):
        # Evaluación del Agente
        i=0
        Estados=[(0,0) for _ in range(10)]
        Acciones=[0 for _ in range(10)]
        
        estado=(1, 1) # Numero aleatorio
        accion, indice=self.selecciona_accion(estado)
        
        movimientos=0
        while estado != self.estado_final:
            movimientos+=1
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
        
        return movimientos   
            

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
    MASTER = 0              # int.      Master     
    END_OF_PROCESSING = -1  # End of processing
    
    alpha=0
    gamma=0
    epsilon=0
    episodios=0
    matriz=[]
    fils=0
    cols=0

    Q_table=[]
    A_table=[]

    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    epsilon=0.1
    episodios=500
    archivo="30"
    maze="M{}x{}".format(str(archivo),str(archivo))

    if myrank==MASTER:
        matriz,fils,cols=leeArchivo(archivo)
        
        # TODO CAMBIAR ENTRE WORKERS?
        alpha=0.5
        gamma=0.6
        epsilon=0.3

        Q_table,A_table=procesarMatriz(matriz,fils,cols)

    timeStart=MPI.Wtime()

    matriz=comm.bcast(matriz, root=MASTER) 
    fils=comm.bcast(fils, root=MASTER) 
    cols=comm.bcast(cols, root=MASTER) 

    Q_table=comm.bcast(Q_table, root=MASTER) 
    A_table=comm.bcast(A_table, root=MASTER) 


    alpha=comm.bcast(alpha, root=MASTER) 
    gamma=comm.bcast(gamma, root=MASTER) 
    epsilon=comm.bcast(epsilon, root=MASTER) 

    if myrank==MASTER:   
        comm.send((1,1),dest=1)
                
        for i in range(2,numWorkers+1):
            while True:
                fila=random.randint(1,fils-1)
                col=random.randint(1,cols-1)
                
                if len(Q_table[fila][col])!=0: break
            print(fila, col)
            comm.send((fila,col),dest=i)
        
        
        
        for i in range(1,numWorkers+1):
            dataQ=comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)            
            #source_rank=status.Get_source()            

            for i in range(len(Q_table)):                
                for j in range(len(Q_table[i])): 
                    for a in range(len(Q_table[i][j])):                                          
                        Q_table[i][j][a]+=(dataQ[i][j][a]/numWorkers)
        
        """#self.acciones = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        print("Q:",Q_table[29][28])    
        print("A:",A_table[29][28])"""
        timeEnd=MPI.Wtime()
        print("\nM{}X{}\nHa terminado el entrenamiento en: {} \n".format(fils, cols,
                                                                          timeEnd-timeStart))     
        QL=Q_Learning(alpha,gamma,epsilon,episodios, 
                  Q_table, A_table, None,
                  matriz,fils,cols) 
        movs=QL.evalua()

        print("Evaluacion final en {} movimientos\n".format(movs))
        
        
            
        
        

    else: 

        estado_inicial=comm.recv(source=MASTER)
               
        QL=Q_Learning(alpha,gamma,epsilon,episodios, 
                  Q_table, A_table, estado_inicial,
                  matriz,fils,cols)       
        
        

        QL.entrenamiento(episodios)
        comm.send(QL.Q_table,dest=MASTER)
        #comm.send(QL.A_table,dest=MASTER)
        print("Worker termina id:",myrank)
        exit(1)

   


main()
