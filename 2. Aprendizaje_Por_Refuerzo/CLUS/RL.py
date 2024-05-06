from mpi4py import MPI
import os
import random

# EJECUTAR
# mpiexec -np 5 python RL_MPI1.py

"""
PROGRAMA QUE CALCULA LOS MEJORES HIPERPARAMETROS PARA CADA LABERINTO
"""

def leeArchivo(archivo):
    """
    return:
    array: int[].   Array con los enteros leidos
    tam: int.       Tamaño del array leido
    """
        
    dir=os.getcwd()
    print(dir)
    n=len(dir)

    """while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
        dir=os.path.dirname(dir)
        n=len(dir)

    if archivo==None: archivo=input("Introduce un nombre del fichero: ")    
    path=os.path.join(dir, ".Otros","ficheros","0.Laberintos", archivo+".txt")"""
    filas=0
    columnas=0 
    M=[]

    path=os.path.join(dir, archivo+".txt")
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

    episodios=1000
    archivo="100"
    maze="M{}x{}".format(str(archivo),str(archivo))

    if myrank==MASTER:
        matriz,fils,cols=leeArchivo(archivo)

  
    
    matriz=comm.bcast(matriz, root=MASTER) 
    fils=comm.bcast(fils, root=MASTER) 
    cols=comm.bcast(cols, root=MASTER) 


    directorio_script = os.path.dirname(os.path.abspath(__file__))

    

    if myrank==MASTER:
        ruta=os.path.join(directorio_script,'M{}x{}_Salida_MPI{}.txt'.format(fils,cols,numWorkers))
        precision=0.01

        alpha=0.01
        gamma=0.01
        epsilon=0.01

        for i in range(1,numWorkers+1):
            comm.send(alpha, dest=i) # alpha
            comm.send(gamma, dest=i) # gamma
            comm.send(epsilon, dest=i)
            epsilon+=precision
            
            if epsilon>=1:
                epsilon=0.01
                gamma+=precision
                if gamma>=1:
                    gamma=0.01
                    alpha+=precision
        
        id=None
        bucle=True
        while bucle:
            i=1
            while i<numWorkers+1: 
                a=comm.recv(source=i)   
                g=comm.recv(source=i)   
                e=comm.recv(source=i)   

                ent=comm.recv(source=i)   
                eval=comm.recv(source=i)   
                tiempo=comm.recv(source=i)   
                movimientos=comm.recv(source=i)   

                if movimientos!=0:
                    with open(ruta, 'a') as archivo:                                                 
                        archivo.write("a:{} g:{} e:{} BE:{} BP:{} T(3):{} M: {}\n".
                                    format(round(a,2),round(g,2),round(e,2),ent,eval,round(tiempo,3),movimientos))     
                
                

                
                epsilon+=precision
                if epsilon>=1:
                    epsilon=0.01
                    gamma+=precision
                    if gamma>=1:
                        gamma=0.01
                        alpha+=precision
                        if alpha>=1:
                            comm.send(END_OF_PROCESSING, dest=i)
                            bucle=False
                            id=i
                            break
                
                
                comm.send(alpha, dest=i)
                comm.send(gamma, dest=i)
                comm.send(epsilon, dest=i)
                
                i+=1
        
        
        for i in range(1,numWorkers+1):            
            if i==id: continue

            data=comm.recv(source=i)          
            


            comm.send(END_OF_PROCESSING, dest=i)

    else:
                

        alpha=comm.recv(source=MASTER)
        if alpha==END_OF_PROCESSING: exit(1)
        gamma=comm.recv(source=MASTER)
        epsilon=comm.recv(source=MASTER)

        

        while True:            
               
            
            ent=0
            eval=0
            tiempo=0
            movsMedia=0
            timeStart=MPI.Wtime()
            """for i in range(3):                
                QL=Q_Learning(alpha,gamma,epsilon,episodios,
                              matriz,fils,cols,)
                time,movs=QL.ejecuta()
                
                if movs==-1:eval+=1
                elif movs==-2: ent+=1
                else:
                    tiempo+=time
                    movsMedia+=movs"""
            timeEndEnt=MPI.Wtime()

            comm.send(alpha,dest=MASTER)
            comm.send(gamma,dest=MASTER)
            comm.send(epsilon,dest=MASTER)

            comm.send(ent,dest=MASTER)
            comm.send(eval,dest=MASTER)
            comm.send(timeEndEnt-timeStart,dest=MASTER)
            if (ent+eval)==3: 
                comm.send(0,dest=MASTER)
            else:                
                comm.send((movsMedia/3-(ent+eval)),dest=MASTER)
                

           
                
            
            alpha=comm.recv(source=MASTER)
            if alpha==END_OF_PROCESSING: exit(1)
            gamma=comm.recv(source=MASTER)
            epsilon=comm.recv(source=MASTER)

   


main()