import pygame
import sys
import os
import random
import math
import signal

from mpi4py import MPI

#import numpy as np
import collections

import ast # lee mas facilmente una lista de enteros desde un archivo .txt

#FASE 1: RED NEURONAL
class RedNeuronal:
    def __init__(self, tam_entrada, tam_capas_ocultas, tam_salida, learning_rate, archivo):
        self.tam_entrada=tam_entrada
        self.tam_capas_ocultas=tam_capas_ocultas
        self.tam_salida=tam_salida

        self.learning_rate=learning_rate
        
        self.capas=[tam_entrada]+tam_capas_ocultas+[tam_salida]
        
        self.pesos=[]
        # Inicializar los pesos de manera aleatoria
        if archivo==None:            
            for i in range(len(self.capas)-1):
                pesos_capa = [[random.uniform(-1, 1) for _ in range(self.capas[i + 1])] for _ in range(self.capas[i])]
                self.pesos.append(pesos_capa)
        else: # lee de un archivo
            self.lee_pesos(archivo)

    def lee_pesos(self, path):
        try:
            with open(path, 'r') as file:            
                tmp=file.read()            
                self.pesos=ast.literal_eval(tmp)
                
        except Exception as e:
            print(f"Error al leer los pesos: {e}")
            return None        
    
    # Funcion de activacion
    def sigmoide(self, x):
        return 1/(1+math.exp(-x))
    #Derivada (para el entrenamiento)
    def sigmoide_derivado(self, x):
        return x*(1-x)
        

    # Propagación hacia adelante (forward propagation)
    def forward(self,entrada):
        self.salidas=[entrada]
        # Recorre todas las capas (menos la de salida) 
        for i in range(len(self.capas)-1):
            entradas_capa=self.salidas[-1]
            salidas_capa=[0 for _ in range(self.capas[i+1])]
            # Recorre todos los nodos de la capa siguiente
            for j in range(self.capas[i+1]):    
                suma=0
                # Suma todos los nodos de la capa actual con los pesos
                for k in range(self.capas[i]):            
                    suma+=entradas_capa[k]*self.pesos[i][k][j]
                salidas_capa[j]=self.sigmoide(suma) # Aplica funcion de activacion
            
            self.salidas.append(salidas_capa)
        
        # Devuelve el ultimo elemento        
        return self.salidas[-1] 

    # Retropropagación (backpropagation)
    def backward(self, entrada, etiqueta):
        #self.forward(entrada)
        errores=[]
        for i in range(self.tam_salida):
            errores.append((etiqueta[i]-self.salidas[-1][i])*self.sigmoide_derivado(self.salidas[-1][i]))
                        
        # Recorre todas las capas (menos la de entrada) en orden inverso
        for i in range(len(self.capas) - 2, -1, -1):
            nuevos_errores=[0 for _ in range(self.capas[i])]
            # Recorre todos los nodos de la capa actual
            for j in range(self.capas[i]):
                suma=0
                # Suma todos los nodos de la capa siguiente (sin orden inverso, es decir, la derecha)
                for k in range(self.capas[i+1]):            
                    suma+=errores[k]*self.pesos[i][j][k]
                nuevos_errores[j]=suma*self.sigmoide_derivado(self.salidas[i][j])

                # Actualiza los nodos
                for k in range(self.capas[i+1]):
                    self.pesos[i][j][k]+=self.learning_rate*errores[k]*self.salidas[i][j]

            errores = nuevos_errores
    
    
    
    def entrenar(self, entrada, etiqueta):
        self.forward(entrada)
        self.backward(entrada, etiqueta)

    def predecir(self, inputs):
        return self.forward(inputs)


#FASE 2: ALGORITMO Q-LEARNING
class DQNAgent:
    def __init__(self, input_size, hidden_size, output_size, learning_rate, gamma, epsilon, archivo1, archivo2):
        self.model = RedNeuronal(input_size, hidden_size, output_size, learning_rate, archivo1)
        self.target_model = RedNeuronal(input_size, hidden_size, output_size, learning_rate, archivo2)

        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate

        self.memory = collections.deque(maxlen=2000)
        self.batch_size = 64

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, 3)  # Assuming 4 possible actions
        else:
            q_values = self.model.predecir(state)
            return q_values.index(max(q_values))
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    """def train(self, state, action, reward, next_state, done):
        q_values = self.model.predict(state)
        next_q_values = self.model.predict(next_state)
        
        if done:
            target = reward
        else:
            target = reward + self.gamma * max(next_q_values)
        
        q_values[action] = target
        self.model.train(state, q_values)"""
    

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        
        batch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in batch:
            q_values = self.model.predecir(state)
            next_q_values = self.target_model.predecir(next_state)
            
            if done:
                target = reward
            else:
                target = reward + self.gamma * max(next_q_values)
            
            q_values[action] = target
            self.model.entrenar(state, q_values)
        
        if self.epsilon > 0.01:
            self.epsilon *= 0.995

    def update_target_model(self):
        self.target_model.pesos = self.model.pesos.copy()


#FASE 3: ENTORNO


class Pacman:

    def __init__(self,archivo, GUI):
        self.archivo=archivo

        # Elementos del tablero
        self.VACIO=0
        self.MURO=1
        self.MONEDA=2
        self.POWER=3
        self.AGENTE=4

        # Acciones
        self.ARRIBA='arriba'
        self.ABAJO='abajo'
        self.IZQUIERDA='izquierda'
        self.DERECHA='derecha'
        
        self.acciones = [self.ARRIBA, self.DERECHA, self.ABAJO, self.IZQUIERDA]
        
        self.reset()

        if GUI==True:
            # conf: ventana
            self.tam_celda=30
            self.alto=self.n*self.tam_celda
            self.ancho=self.m*self.tam_celda

            # init pygame
            pygame.init()       
            self.pantalla=pygame.display.set_mode((self.ancho, self.alto))
            pygame.display.set_caption('Laberinto') 

            # Imagenes
            self.empty_img=[]
            self.coin_img=[]
            self.power_img=[]
            self.walls_imgs=[]
            self.agente_imgs=[]
            self.cargar_imagenes(self.tam_celda)

            self.mostrar_laberinto()

    def reset(self):
        # Agente
        self.posicion_agente=None
        self.direccion=1
        self.monedas=0
        
        # Laberinto
        self.laberinto=[]
        self.leer_laberinto(self.archivo)
        self.n=len(self.laberinto)
        self.m=len(self.laberinto[0])

        return self.get_state()
        
    def get_state(self):
        # convertir la matriz en un array y añadir la posicion del agente y numero de monedas
        state=[]
        for row in self.laberinto:
            state.extend(row)

        state.append(self.posicion_agente[0])
        state.append(self.posicion_agente[1])
        state.append(self.monedas)
        return state

    def step(self, accion):                
        moneda=self.mover_agente(self.acciones[accion])
        
        estado_sig=self.get_state()
        recompensa=10 if moneda == 1 else -1
        #recompensa=self.monedas        
        fin=self.monedas==159
        #all(self.laberinto[i][j] != self.MONEDA for i in range(self.n) for j in range(self.m))
        
        return estado_sig, recompensa, fin

    # Leer el laberinto desde un archivo
    def leer_laberinto(self, archivo):  

        with open(archivo, 'r') as file:        
            for line in file:
                row=list(map(int, line.split()))
                self.laberinto.append(row)
        

        for x in range(len(self.laberinto)):
            for y in range(len(self.laberinto[0])):
                if self.laberinto[x][y]==self.AGENTE: 
                    self.posicion_agente=(x, y)
                    break
    
    def imprime_laberinto(self):
        for x in range(len(self.laberinto)):
            for y in range(len(self.laberinto[0])):
                if self.laberinto[x][y]<0: 
                    print(-1, end=" ")
                else: print(self.laberinto[x][y], end=" ")
            print()

    # Mueve al agente
    def mover_agente(self, mov):
        x, y = self.posicion_agente
        m=len(self.laberinto[0])
        moneda=0

        if mov==self.ARRIBA:
            if x>0 and self.laberinto[x-1][y]>=0:
                if self.laberinto[x-1][y]==self.MONEDA: moneda=1
                self.laberinto[x][y]=self.VACIO
                x-=1
        elif mov==self.ABAJO:
            if x<len(self.laberinto)-1 and self.laberinto[x+1][y]>=0:
                if self.laberinto[x+1][y]==self.MONEDA: moneda=1
                self.laberinto[x][y]=self.VACIO
                x+=1
        elif mov==self.IZQUIERDA:
            if y>0 and self.laberinto[x][y-1]>=0:
                if self.laberinto[x][y-1]==self.MONEDA: moneda=1
                self.laberinto[x][y]=self.VACIO
                y-=1
            elif y==0 and (x==5 or x==9):
                if self.laberinto[x][m-1]==self.MONEDA: moneda=1
                self.laberinto[x][y]=self.VACIO
                y=m-1
        elif mov==self.DERECHA:
            if y<m-1 and self.laberinto[x][y+1]>=0:
                if self.laberinto[x][y+1]==self.MONEDA: moneda=1
                self.laberinto[x][y]=self.VACIO
                y+=1
            elif y==m-1 and (x==5 or x==9):
                if self.laberinto[x][0]==self.MONEDA: moneda=1
                self.laberinto[x][y]=self.VACIO
                y=0

        self.laberinto[x][y]=self.AGENTE
        self.posicion_agente=(x, y)
        self.monedas+=moneda
        return moneda

    def ejecuta(self):

        while True:            
            # evento = pulsa alguna tecla
            for evento in pygame.event.get():
                if evento.type==pygame.QUIT: # cerrar GUI
                    pygame.quit()
                    sys.exit()
                elif evento.type==pygame.KEYDOWN: # pulsa tecla                
                    if evento.key==pygame.K_UP: 
                        mov=self.ARRIBA                    
                        self.direccion=0
                    elif evento.key==pygame.K_RIGHT: 
                        mov=self.DERECHA 
                        self.direccion=1
                    elif evento.key==pygame.K_DOWN: 
                        mov=self.ABAJO    
                        self.direccion=2
                    elif evento.key==pygame.K_LEFT: 
                        mov=self.IZQUIERDA    
                        self.direccion=3
                    else: mov=None
                    
                    if mov!=None: 
                        self.mover_agente(mov)
                        #print(self.monedas)
                        #self.imprime_laberinto()                        
                        print("Monedas: {}".format(self.monedas))


            # dibuja el laberinto
            self.pantalla.fill((0, 0, 0))  # limpia antes de dibujar

            # recorre el laberinto
            for x, fila in enumerate(self.laberinto):
                for y, celda in enumerate(fila):
                    if celda<0:
                        imagen=self.walls_imgs[abs(celda)-1]  
                    elif celda==1: imagen=self.walls_imgs[-1]
                    elif celda==self.VACIO: imagen=self.empty_img                
                    elif celda==self.MONEDA: imagen=self.coin_img
                    elif celda==self.POWER: imagen=self.power_img
                    else: imagen=self.agente_imgs[self.direccion] 
                    

                    self.pantalla.blit(imagen, (y*self.tam_celda, x*self.tam_celda))

            pygame.display.flip()

    # --------------------------------------------------------------------------------
    # --- GUI ------------------------------------------------------------------------
    # --------------------------------------------------------------------------------

    # Función para inicializar pygame y mostrar el laberinto en una ventana
    def mostrar_laberinto(self):       

        #self.imprime_laberinto()
         
        mov=None
        imagen=None

        # bucle principal
        while True:            
            # evento = pulsa alguna tecla
            for evento in pygame.event.get():
                if evento.type==pygame.QUIT: # cerrar GUI
                    pygame.quit()
                    sys.exit()
                elif evento.type==pygame.KEYDOWN: # pulsa tecla                
                    if evento.key==pygame.K_UP: 
                        mov=self.ARRIBA                    
                        self.direccion=0
                    elif evento.key==pygame.K_RIGHT: 
                        mov=self.DERECHA 
                        self.direccion=1
                    elif evento.key==pygame.K_DOWN: 
                        mov=self.ABAJO    
                        self.direccion=2
                    elif evento.key==pygame.K_LEFT: 
                        mov=self.IZQUIERDA    
                        self.direccion=3
                    else: mov=None
                    
                    if mov!=None: 
                        self.mover_agente(mov)
                        #print(self.monedas)
                        #self.imprime_laberinto()                        
                        print("Monedas: {}".format(self.monedas))


            # dibuja el laberinto
            self.pantalla.fill((0, 0, 0))  # limpia antes de dibujar

            # recorre el laberinto
            for x, fila in enumerate(self.laberinto):
                for y, celda in enumerate(fila):
                    if celda<0:
                        imagen=self.walls_imgs[abs(celda)-1]  
                    elif celda==1: imagen=self.walls_imgs[-1]
                    elif celda==self.VACIO: imagen=self.empty_img                
                    elif celda==self.MONEDA: imagen=self.coin_img
                    elif celda==self.POWER: imagen=self.power_img
                    else: imagen=self.agente_imgs[self.direccion] 
                    

                    self.pantalla.blit(imagen, (y*self.tam_celda, x*self.tam_celda))

            pygame.display.flip()

    def cargar_imagenes(self, tam):
        # leer las imagenes
        vacio=pygame.image.load('imagenes/empty.png').convert_alpha()    
        moneda=pygame.image.load('imagenes/coin.png').convert_alpha()
        power=pygame.image.load('imagenes/power.png').convert_alpha()
        
        walls=[]
        #walls.append(pygame.image.load('imagenes/wall_0.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_0.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_01.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_1.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_02.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_2.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_03.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_3.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_012.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_12.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_013.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_13.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_023.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_23.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall_123.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/wall.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/z0.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/z1.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/z2.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/z3.png').convert_alpha())
        walls.append(pygame.image.load('imagenes/z4.png').convert_alpha())
        

        agente=[]
        agente.append(pygame.image.load('imagenes/pacman_up.png').convert_alpha())
        agente.append(pygame.image.load('imagenes/pacman_right.png').convert_alpha())
        agente.append(pygame.image.load('imagenes/pacman_down.png').convert_alpha())
        agente.append(pygame.image.load('imagenes/pacman_left.png').convert_alpha())

        # escalar para que tengan el mismo tamaño
        self.empty_img=pygame.transform.scale(vacio, (tam, tam))    
        self.coin_img=pygame.transform.scale(moneda, (tam, tam))
        self.power_img=pygame.transform.scale(power, (tam, tam))

        self.walls_imgs=[]
        self.agente_imgs=[]
        for i in range(20):
            self.walls_imgs.append(pygame.transform.scale(walls[i], (tam, tam)))
        
        for i in range(4):
            self.agente_imgs.append(pygame.transform.scale(agente[i], (tam, tam)))
  

#FASE 4: ENTRENAR DQN
class Main:
    def signal_handler(self, sig, frame):
        self.timeEnd=MPI.Wtime()
        path=os.path.join("entrenamiento", "model_Neu.txt")
        with open(path, "a") as archivo:
            archivo.write(str(self.agent.model.pesos) + "\n\n")
        
        path=os.path.join("entrenamiento", "target_model_Neu.txt")
        with open(path, "a") as archivo:
            archivo.write(str(self.agent.target_model.pesos) + "\n\n")

        path=os.path.join("entrenamiento", "times.txt")
        with open(path, "a") as archivo:
            archivo.write(str(self.timeEnd-self.timeStart) + "\n\n")
        
        print("\nCtrl+C pressed. Variable written to file.")
        sys.exit(0)
    

    
    def train_dqn(self, episodes):
        signal.signal(signal.SIGINT, self.signal_handler)
        try:            
            env = Pacman(os.path.join("datos", "env.txt"), False)
            input_size = len(env.get_state())
            #agent = DQNAgent(input_size=4, hidden_size=16, output_size=4, learning_rate=0.01, gamma=0.99, epsilon=1.0)
            self.agent = DQNAgent(input_size=input_size, hidden_size=[16], output_size=4, learning_rate=0.01, gamma=0.99, epsilon=1.0,
                                  archivo1=os.path.join("datos", "model_Neu.txt"),
                                  archivo2=os.path.join("datos", "target_model_Neu.txt")) # Usar (None) para que no lea unos pesos ya entrenados
            
            self.timeStart=MPI.Wtime()
            for episode in range(episodes):
                state = env.reset()
                done = False
                total_reward = 0
                print("Empieza: ", episode+1)
                tStart=MPI.Wtime()
                while not done:
                    action = self.agent.choose_action(state)
                    next_state, reward, done = env.step(action)
                    
                    self.agent.remember(state, action, reward, next_state, done)
                    self.agent.replay()
                    
                    state = next_state
                    total_reward += reward
                    print(env.monedas)
                tEnd=MPI.Wtime()
                print("Ha terminado un episodio entrenamiento en: {} \n".format(tEnd-tStart))  
                self.agent.update_target_model()
                
                print(f"Episode {episode + 1}: Total Reward: {total_reward}")
            
            os.kill(os.getpid(), signal.SIGINT)

        except KeyboardInterrupt:
            # Handle the KeyboardInterrupt exception if needed
            print("\nKeyboardInterrupt caught. Exiting gracefully.")







if __name__ == "__main__":
    main=Main()
    main.train_dqn(1000)
    #env=Pacman("env.txt",True)
    
    
