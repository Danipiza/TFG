from mpi4py import MPI
import sys
import os
import signal
import random

# EJECUTAR
# mpiexec -np 5 python RL_MPI1.py

"""
PROGRAMA QUE CALCULA LOS MEJORES HIPERPARAMETROS PARA CADA LABERINTO
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
                 matriz,fils,cols):
        # Definir el laberinto 0: vacio, 1: pared
        
        #self.matriz,self.fils,self.cols=leeArchivo(archivo)
        self.matriz=matriz
        self.fils=fils
        self.cols=cols
        
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
        Estados=[(0,0) for _ in range(4)]   # AQUI
        Acciones=[0 for _ in range(4)]      # AQUI
       
        for ep in range(episodios):
            estado = (1, 1)
            timeStart=MPI.Wtime()
            while estado != self.estado_final:  
                
                accion = self.selecciona_accion(estado)
                Estados[i]=estado
                Acciones[i]=accion
                i=(i+1)%4               # AQUI

                if self.accion_valida(estado, self.acciones[accion]):
                    sig_estado = (estado[0] + self.acciones[accion][0], estado[1] + self.acciones[accion][1])
                    if self.matriz[sig_estado[0]][sig_estado[1]] == 1: 
                        recompensa = self.recompensas['pared']
                    elif sig_estado == self.estado_final: 
                        recompensa = self.recompensas['destino']
                    else: recompensa = self.recompensas['otro']
                    self.actualiza_Q_table(estado, accion, recompensa, sig_estado)
                    if self.matriz[sig_estado[0]][sig_estado[1]]!=1: estado = sig_estado
                
                timeEnd=MPI.Wtime()

                if timeEnd-timeStart>2:
                    """print("Bucle")"""
                    return -1
        return 1
                
       

    def ejecuta(self):
        timeStart=MPI.Wtime()
        ent=self.entrenamiento(self.episodios)        
        timeEndEnt=MPI.Wtime()
        #print("Ha terminado el entrenamiento en: {} \n".format(timeEndEnt-timeStart))
        if ent==-1: return timeEndEnt-timeStart,-2
        
        i=0
        Estados=[(0,0) for _ in range(4)] #AQUI
        Acciones=[0 for _ in range(4)] #AQUI
        
        estado = (1, 1) 
        accion = self.selecciona_accion(estado)
        
        cont=0
        while estado != self.estado_final:
            cont+=1

            Estados[i]=estado
            Acciones[i]=accion
            i=(i+1)%4 #AQUI
            
            tmp=0
            maximo=self.Q_table[estado[0]][estado[1]][0]
            accion=0		
            for k in range(1,self.num_acciones):
                tmp=self.Q_table[estado[0]][estado[1]][k]
                if maximo<tmp: 
                    maximo=tmp
                    accion=k
            
            if self.accion_valida(estado, self.acciones[accion]): 
                estado = (estado[0] + self.acciones[accion][0], estado[1] + self.acciones[accion][1])
            
            if Estados[0]==Estados[2] and Estados[1]==Estados[3] and Estados[0]!=Estados[1]:                
                return (timeEndEnt-timeStart), -1
                
            
        """print("Ejecucion final:", (timeEnd-timeEndEnt))"""
        return (timeEndEnt-timeStart), cont
        
from mpi4py import MPI  # Al importar la biblioteca en Python se genera el entorno automaticamente

tag=0                   # tag para mas informacion      
comm=MPI.COMM_WORLD     # Comunicador
status = MPI.Status()   # Status
myrank=comm.Get_rank()  # id de cada procesp
numProc=comm.Get_size() # Numero de procesadores

if myrank==0: 
    # TODO
else:
    # TODO


    x=1



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

    tag=0
    comm=MPI.COMM_WORLD    
    status = MPI.Status()
    myrank=comm.Get_rank()
    numProc=comm.Get_size()
    numWorkers=numProc-1

    epsilon=0.1
    episodios=1000
    archivo="100"
    maze="M{}x{}".format(str(archivo),str(archivo))

    if myrank==MASTER:
        matriz,fils,cols=leeArchivo(archivo)

    matriz=comm.bcast(matriz, root=MASTER) 
    fils=comm.bcast(fils, root=MASTER) 
    cols=comm.bcast(cols, root=MASTER) 

    if myrank==MASTER:
        izq=0.1
        for i in range(1,numWorkers+1):
            comm.send(0.1, dest=i) # alpha
            comm.send(izq, dest=i) # gamma
            izq+=0.1
        
        gamma=izq-0.1
        
        while True:

            data=comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)            
            source_rank=status.Get_source()
            
            
            gamma+=0.1

            if gamma>=1:
                gamma=0.1
                alpha+=0.1
                if alpha>=1: 
                    comm.send(END_OF_PROCESSING, dest=source_rank)
                    break
            
            comm.send(alpha, dest=source_rank)
            comm.send(gamma, dest=source_rank)
            
        for i in range(1,numWorkers):
            data=comm.recv(source=MPI.ANY_SOURCE, tag=tag,status=status)            
            source_rank=status.Get_source()
            comm.send(END_OF_PROCESSING, dest=source_rank)

    else:
        
        directorio_script = os.path.dirname(os.path.abspath(__file__))
    
        ruta_dir=os.path.join(directorio_script, 'Pruebas_Parametros')
        

        alpha=comm.recv(source=MASTER)
        if alpha==END_OF_PROCESSING: exit(1)
        gamma=comm.recv(source=MASTER)

        

        while True:            
            ruta=os.path.join(ruta_dir,'{}_Eps{}Alpha{}.txt'.format(maze,episodios,round(alpha,1)))   
            epsilon=0.1
            

            for i in range(8):
                
                QL=Q_Learning(alpha,gamma,epsilon,episodios, 
                              matriz,fils,cols)
                time,movs=QL.ejecuta()
                
                
                
                
                if movs!=-1 and movs!=-2:                
                    with open(ruta, 'a') as archivo:                              
                        archivo.write("W{}. Gamma: {}\tEpsilon: {}\t Tiempo: {}s\tMovimientos: {}\n".format(
                            myrank,round(gamma,1),round(epsilon,1),time,movs))
                else:
                    bucle="Bucle en Entrenamiento"
                    if movs==-1: bucle="Bucle en Prueba"
                    with open(ruta, 'a') as archivo:                              
                        archivo.write("W{}. Gamma: {}\tEpsilon: {}\t Tiempo: {}s\t{}\n".format(
                            myrank, round(gamma,1),round(epsilon,1), time, bucle))
                epsilon+=0.1
            
            comm.send(0,dest=MASTER)

            alpha=comm.recv(source=MASTER)
            if alpha==END_OF_PROCESSING: exit(1)
            gamma=comm.recv(source=MASTER)

   


main()