from mpi4py import MPI
import sys
import os
import signal
import random

# EJECUTAR
# mpiexec -np 5 python RL_MPI_2_3.py

# NO FUNCIONA, POR ALGUNA RAZON SE QUEDA DANDO VUELTAS
# SI LE PASAMOS UN Q-TABLE ENTRENADA SI FUNCIONA

"""
INTENTO DE MEJORA:

CADA WORKER EJECUTA SU ENTRENAMIENTO DIVIDIENDO EL NUMERO DE EPISODIOS.
    CADA WORKER INICIA EN PUNTOS DIFERENTES (AL MENOS 1 EN EL PUNTO DE ORIGEN DE LA EVALUACION)

CUANDO TERMINAN LE PASAN LAS Q-TABLE AL MASTER Y ESTE HACE LA MEDIA Y EJECUTA LA EVALUACION

TODOS DESDE EL MISMO PUNTO
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
    n=[]
    m=[]
    limites=[]

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
        epsilon=0.1

        """alpha=0.5
        gamma=0.7
        epsilon=0.4"""

        n=[1,15]
        m=[1,15]
        limites=[2,1]

        comm.send([1,15],dest=1)
        comm.send([16,29],dest=1)
        comm.send([3,-1],dest=1)

        comm.send([16,29],dest=2)
        comm.send([1,15],dest=2)
        comm.send([-1,3],dest=2)

        comm.send([16,29],dest=3)
        comm.send([16,29],dest=3)
        comm.send([1,2],dest=3)

        Q_table,A_table=procesarMatriz(matriz,fils,cols)
    else: 
        n=comm.recv(source=MASTER)
        m=comm.recv(source=MASTER)
        limites=comm.recv(source=MASTER)
    
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
            
        QL=Q_Learning(alpha,gamma,epsilon,episodios, 
                  Q_table, A_table,
                  matriz,fils,cols) 
        
        for cont in range(episodios):
            i=0
            Estados=[(0,0) for _ in range(10)]
            Acciones=[0 for _ in range(10)]

            """if cont==100:
                print("Destino",myrank)
                exit(1)"""

            
            estado = (1, 1)
            while True:#estado != self.estado_final:  
                
                accion, indice=QL.selecciona_accion(estado)
                Estados[i]=estado
                Acciones[i]=accion
                i=(i+1)%10

                sig_estado = (estado[0] + QL.acciones[accion][0], estado[1] + QL.acciones[accion][1])
                
                if sig_estado == QL.estado_final: 
                    recompensa = QL.recompensas['destino']
                    break
                else: recompensa = QL.recompensas['otro']
                
                QL.actualiza_Q_table(estado, accion, indice, recompensa, sig_estado)
                if QL.matriz[sig_estado[0]][sig_estado[1]]!=1: 
                    if sig_estado[0]>=n[0] and sig_estado[0]<=n[1] and sig_estado[1]>=m[0] and sig_estado[1]<=m[1]:
                        estado=sig_estado
                        #print("Mantiene, E:",estado)
                    else:
                        #print("Envia, E:",sig_estado)
                        id=1
                        if sig_estado[0]<n[0] or sig_estado[0]>n[1]:
                            id=0
                        if limites[id]!=-1: # El master no puede recibir
                            comm.send(sig_estado,dest=limites[id])
                            #print("Envia",limites[id])
                            break              
        #exit(1)
        
        for cont in range(episodios):
            data=comm.recv(source=numWorkers)
        
        for i in range(1,numWorkers+1):
            comm.send(END_OF_PROCESSING,dest=i)

        comm.Barrier()

        timeEnd=MPI.Wtime()
        """print("\nM{}X{}\nHa terminado el entrenamiento en: {} \n".format(fils, cols,
                                                                          timeEnd-timeStart)) """
        
        

        """print("Evaluacion final en {} movimientos\n".format(movs))"""
        

    else: 
              
        QL=Q_Learning(alpha,gamma,epsilon,episodios, 
                  Q_table, A_table,
                  matriz,fils,cols)       
        
        while True:
            estado=comm.recv(source=MPI.ANY_SOURCE)
            if estado==END_OF_PROCESSING: 
                timeEnd=MPI.Wtime()
                comm.Barrier()
                #print("WORKER {} termina en: {}s\n".format(myrank,timeEnd-timeStart))
                
                exit(1)
                
            """print("W {} recibe e: {}".format(myrank, estado))"""
            
            i=0
            Estados=[(0,0) for _ in range(10)]
            Acciones=[0 for _ in range(10)]
            
            
            
            
            while True:#estado != self.estado_final:  
                
                accion, indice=QL.selecciona_accion(estado)
                
                
                Estados[i]=estado
                Acciones[i]=accion
                i=(i+1)%10

                #if self.accion_valida(estado, self.acciones[accion]):
                sig_estado = (estado[0] + QL.acciones[accion][0], estado[1] + QL.acciones[accion][1])
                """print("W{}: estado: {}\tacciones: {}\tsig_estado:{}".format(
                    myrank, estado, QL.A_table[estado[0]][estado[1]], sig_estado))"""
                
                if sig_estado == QL.estado_final: 
                    recompensa = QL.recompensas['destino']
                    print("Destino",myrank)
                    comm.send(1,dest=MASTER)
                    #exit(1)
                    break
                else: recompensa = QL.recompensas['otro']
                
                QL.actualiza_Q_table(estado, accion, indice, recompensa, sig_estado)
                if QL.matriz[sig_estado[0]][sig_estado[1]]!=1: 
                    if sig_estado[0]>=n[0] and sig_estado[0]<=n[1] and sig_estado[1]>=m[0] and sig_estado[1]<=m[1]:
                        estado=sig_estado
                        #print("Mantiene, E:",estado)
                    else:                        
                        
                        id=1
                        if sig_estado[0]<n[0] or sig_estado[0]>n[1]: id=0
                        
                        if limites[id]!=-1: # El master no puede recibir
                            print(myrank,"Envia, E:",sig_estado)
                            comm.send(sig_estado,dest=limites[id])
                            #print("Envia",limites[id])
                            #exit(1)
                            break 

         
            




   


main()
