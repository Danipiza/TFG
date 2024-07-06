import pygame
import sys
import os
import random
import math
import signal
import time

from mpi4py import MPI

#import numpy as np
import collections

import ast # lee mas facilmente una lista de enteros desde un archivo .txt

# GHOSTS AI
# https://www.youtube.com/watch?v=ataGotQ7ir8&ab_channel=RetroGameMechanicsExplained

class PacmanGUI:
    
    """
    MOVEMENTS KEYS:
    "up"    or "w": UP
    "right" or "d": RIGHT
    "down"  or "s": DOWN
    "left"  or "a": LEFT
    """


    def __init__(self,file_name):
        self.file_name=file_name
        
        # -------------------------------------------------------------------------------------------------------------------
        # --- CONSTANTS -----------------------------------------------------------------------------------------------------
        
        self.EMPTY  =0
        self.WALL   =1
        self.COIN   =2
        self.POWER  =3
        self.AGENT  =4        
        self.RED    =5
        self.PINK   =6
        self.BLUE   =7
        self.ORANGE =8

        # actions.
        self.UP     ='up'
        self.LEFT   ='left'
        self.DOWN   ='down'        
        self.RIGHT  ='right'

        # directions. 
        # 0: UP 
        # 1: RIGHT 
        # 2: DOWN 
        # 3: LEFT
        self.mX=[-1,0,1,0]
        self.mY=[0,1,0,-1]
                

        self.ghosts_colors  =[5,6,7,8]
        self.state_ticks    =[60,30,30]

        # -------------------------------------------------------------------------------------------------------------------       
        # --- VARIABLES -----------------------------------------------------------------------------------------------------
        
        # state.
        # 0: CHASE          (chase certain targets)
            # RED:      target = agent position 
            # PINK:     target = agent position + 4 cells in the agent direction (up is an exeption, also add 4 to the left)
            # BLUE:     target = tmp + vector from red ghost to tmp.       
            #   where 
            #       tmp = agent position + 2 cells in the agent direction (up is an exeption, also add 2 to the left)                     
            # ORANGE:   target = if distante to agent > 8 -> agent. otherwise -> his scatter point
        # 1: SCATTER        (chase scatter point. borders of the maze)
        # 2: FRIGHTENED     (runaway from the aget)
        self.state=1
        
        self.scatter_targets=[]

        # number of ticks in the execution.
        self.exec_tick=0
        # number of ticks in the actual state.
        self.count_state=0

        # agent.
        self.agent_pos=None
        self.agent_dir=1
        self.agent_coins=0   

        # ghosts.
        self.ghosts_pos=[[0,0] for _ in range(4)]
        self.ghosts_dir=[1,2,0,0]
        self.ghosts_house=[False,True,True,True]
        # queue, for the leaving order. 0th: ghost id. 1th: home leaving tick
        self.ghost_inHouse=[[1,3],[2,6],[3,9]]
        
        # maze.
        self.maze           =[] # used for the walls, agent and ghosts positions in the GUI
        self.coins_matrix   =[] # used for the coins in the GUI         
        self.n=0                # number of rows
        self.m=0                # number of coloumns

        # finalization variable
        self.end=False

        self.reset()
    
        # screen config
        self.cell_size=30
        self.height=self.n*self.cell_size
        self.width=self.m*self.cell_size

        # init pygame
        pygame.init()       
        self.screen=pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Pac-Man') 

        # images.
        self.empty_img  =[]
        self.coin_img   =[]
        self.power_img  =[]
        self.walls_imgs =[]
        self.agent_imgs =[]
        self.ghosts_imgs=[]
        self.load_images(self.cell_size)

        self.execute()

    """
    Reseting the class variables.

    :type self: class    
    :rtype: None
    """
    def reset(self):

        self.exec_tick=0

        self.state=1
        self.count_state=0
        
        self.agent_pos=None
        self.agent_dir=1
        self.agent_coins=0   

        self.ghosts_pos=[[0,0] for _ in range(4)]
        self.ghosts_dir=[1,2,0,0]
        self.ghosts_house=[False,True,True,True]
        self.ghost_inHouse=[[1,3],[2,6],[3,9]]
        
        self.maze=[]
        self.coins_matrix=[]
        self.read_maze()
        self.n=len(self.maze)
        self.m=len(self.maze[0])

        self.scatter_targets=[[0,self.m],[0,0],[self.n,0],[self.n,self.m]]

        self.end=False

      

    """
    Reading the maze from a .txt file. 
    Also search for the positions of the agent and ghosts
    
    :type self: class        
    :rtype: None
    """
    def read_maze(self):  
        tmp=0

        # -------------------------------------------------------------------------------------------------------------------
        # --- READING -------------------------------------------------------------------------------------------------------

        with open(self.file_name, 'r') as file:        
            for line in file:
                row=list(map(int, line.split()))
                self.maze.append([0 for _ in range(len(row))])
                self.coins_matrix.append([0 for _ in range(len(row))])
                
                # remove the coins from the maze. 
                # "self.coins_matrix" is in charge of the coins
                for i in range(len(row)):   
                    if row[i]==2 or row[i]==3: self.maze[tmp][i]=0
                    else: self.maze[tmp][i]=row[i]
                                
                for i in range(len(row)):                    
                    self.coins_matrix[tmp][i]=row[i]                
                
                tmp+=1
                               
        
        #self.print_maze(self.maze)


        # -------------------------------------------------------------------------------------------------------------------
        # --- POSITIONS -----------------------------------------------------------------------------------------------------

        tmp=0
        # once all are located, break the loop
        for x in range(len(self.maze)):
            for y in range(len(self.maze[0])):                    
                if self.maze[x][y]==self.AGENT: 
                    self.agent_pos=[x,y]
                    tmp+=1
                    if tmp==5: break  

                elif self.maze[x][y]==self.RED: 
                    self.ghosts_pos[0]=[x,y]
                    self.salida_fants=[x,y]
                    tmp+=1
                    if tmp==5: break
                elif self.maze[x][y]==self.PINK: 
                    self.ghosts_pos[1]=[x,y]
                    self.ghosts_house[1]=[x,y]
                    tmp+=1
                    if tmp==5: break
                elif self.maze[x][y]==self.BLUE: 
                    self.ghosts_pos[2]=[x,y]
                    self.ghosts_house[2]=[x,y]
                    tmp+=1
                    if tmp==5: break
                elif self.maze[x][y]==self.ORANGE: 
                    self.ghosts_pos[3]=[x,y]
                    self.ghosts_house[3]=[x,y]
                    tmp+=1
                    if tmp==5: break
        
        
        
                    

    """
    Printing a matrix giving by parameter.
    
    :type self: class 
    :type matrix: int[][]       
    :rtype: None
    """
    def print_matrix(self, matrix):
        
        n=len(self.matrix)
        m=len(self.matrix[0])
        for x in range(n):
            for y in range(m):
                if matrix[x][y]<0: 
                    print(-1, end=" ")
                else: print(matrix[x][y], end=" ")
            print()

    

    """
    Moving the agent.
    eat ghosts or is eaten by a ghost
    
    return: 1, if the agent eat a coin. 
            0, otherwise
    
    :type self: class 
    :type mov: string
    :rtype: int
    """
    def move_agent(self, mov):
        x=self.agent_pos[0]
        y=self.agent_pos[1] 
        
        coin=0
        
        # increases the execution ticks
        self.exec_tick+=1

        # -------------------------------------------------------------------------------------------------------------------
        # --- MOVE ----------------------------------------------------------------------------------------------------------

        # POWER is only reachable by up and down actions

        if mov==self.UP:
            if x>0 and self.maze[x-1][y]>=0:                # dest position != wall
                if self.coins_matrix[x-1][y]==self.COIN:    # COIN. adds a coin
                    self.coins_matrix[x-1][y]=0
                    coin=1
                elif self.coins_matrix[x-1][y]==self.POWER: # POWER. change the game state to FRIGHTENED
                    self.coins_matrix[x-1][y]=0
                    self.state=2
                    self.count_state=0
                    
                    # change the directions of the ghosts
                    for i in range(4):                        
                        if not self.ghosts_house[i]:
                            self.ghosts_dir[i]+=2
                            self.ghosts_dir[i]%=4                        
                
                self.maze[x][y]=self.EMPTY
                x-=1

        elif mov==self.DOWN:
            if x<len(self.maze)-1 and self.maze[x+1][y]>=0: # dest position != wall
                if self.coins_matrix[x+1][y]==self.COIN:    # COIN. adds a coin
                    self.coins_matrix[x+1][y]=0
                    coin=1
                elif self.coins_matrix[x+1][y]==self.POWER: # POWER. change the game state to FRIGHTENED
                    self.coins_matrix[x+1][y]=0
                    self.state=2
                    self.count_state=0
                    for i in range(4):
                        if not self.ghosts_house[i]:
                            self.ghosts_dir[i]+=2
                            self.ghosts_dir[i]%=4
                
                self.maze[x][y]=self.EMPTY
                x+=1

        elif mov==self.LEFT:
            if y>0 and self.maze[x][y-1]>=0:                # dest position != wall
                if self.coins_matrix[x][y-1]==self.COIN:    # COIN. adds a coin
                    self.coins_matrix[x][y-1]=0
                    coin=1
                
                self.maze[x][y]=self.EMPTY
                y-=1
            elif y==0 and (x==5 or x==9):           # "portal"                                 
                self.maze[x][y]=self.EMPTY
                y=self.m-1

        elif mov==self.RIGHT:
            if y<self.m-1 and self.maze[x][y+1]>=0:         # dest position != wall
                if self.coins_matrix[x][y+1]==self.COIN:    # COIN. adds a coin
                    self.coins_matrix[x][y+1]=0
                    coin=1
                
                self.maze[x][y]=self.EMPTY
                y+=1
            elif y==self.m-1 and (x==5 or x==9):    # "portal"                             
                self.maze[x][y]=self.EMPTY
                y=0
        
        # -------------------------------------------------------------------------------------------------------------------
        # --- EAT/LOSE ------------------------------------------------------------------------------------------------------

        if self.state==2:   # eat.
            eaten=[]
            for i in range(4):
                if self.ghosts_pos[i][0]==x and self.ghosts_pos[i][1]==y:
                    eaten.append(i)
            
            tmp=1
            for i in eaten:
                # move the eaten ghost to the house cell.
                self.ghosts_pos[i][0]=self.salida_fants[0]+2
                self.ghosts_pos[i][1]=self.salida_fants[1]

                # add to the queue of ghosts in house
                # they leave in 3 ticks intervals
                self.ghost_inHouse.append([i,self.exec_tick+(3*tmp)])
                self.ghosts_house[i]=[self.ghosts_pos[i][0],self.ghosts_pos[i][1]]

                tmp+=1
        else:               # lose.
            for i in range(4):
                if self.ghosts_pos[i][0]==x and self.ghosts_pos[i][1]==y: 
                    self.end=True
                    self.maze[self.agent_pos[0]][self.agent_pos[1]]=self.EMPTY

        # if the player hasnt lose, he moves 
        if self.end!=True:
            self.maze[x][y]=self.AGENT
            self.agent_pos=[x,y]
            self.agent_coins+=coin
            
        return coin


    """
    Moving the ghosts.
    Also change the game state
           
    :type self: class     
    :rtype: None
    """
    def move_ghosts(self):
        
        # -------------------------------------------------------------------------------------------------------------------
        # --- MOVE ----------------------------------------------------------------------------------------------------------
                    
        self.move_ghost(0) 
        self.move_ghost(1)
        self.move_ghost(2)
        self.move_ghost(3)


        # -------------------------------------------------------------------------------------------------------------------
        # --- STATE ---------------------------------------------------------------------------------------------------------

        self.count_state+=1
        
        print("State=", self.count_state, "\tCoins=",self.agent_coins)
        
        if self.count_state==self.state_ticks[self.state]:                     
            if self.state==0: 
                self.state=1
                print("New state: SCATTER",end="")
            else: 
                self.state=0
                print("New state: CHASE",end="")

            for i in range(4):
                if not self.ghosts_house[i]:
                    self.ghosts_dir[i]+=2
                    self.ghosts_dir[i]%=4
            
            print("\nTurn 180º all ghosts")

            # reset
            self.count_state=0


    """
    Moving a ghost. (if the ghost is in the house, he doesnt moves)
    eat the player or is eaten by the player.

    If the current state is FRIGHTENED, moves one cell in two ticks
           
    :type self: class     
    :type ghost: int
    :rtype: None
    """
    def move_ghost(self, ghost):
        
        x=0
        y=0
        dir=0

        color=self.RED
        if ghost==1: color=self.PINK
        elif ghost==2: color=self.BLUE
        elif ghost==3: color=self.ORANGE

        aux_x=0
        aux_y=0
        
        
        if not self.ghosts_house[ghost] and (not(self.state==2 and self.count_state%2==0)):
            
            dir=self.ghosts_dir[ghost]
            x=self.ghosts_pos[ghost][0]
            y=self.ghosts_pos[ghost][1]

            if dir==0 or dir==2: aux_y=1
            else: aux_x=1
            
            self.maze[x][y]=self.EMPTY

            

            # intersection, moves in the same direction.
            if self.maze[x+aux_x][y+aux_y]<0 and self.maze[x-aux_x][y-aux_y]<0:
                if dir==0: x-=1
                elif dir==1: y+=1
                elif dir==2: x+=1
                else: y-=1

            else: 
                if self.state==2: # FRIGHTENED. moves randomly in the intersection
                    
                    # the oposite direction is not taken into account

                    opcs=[]
                    for k in range(4):
                        tmp_x=x+self.mX[k]
                        tmp_y=y+self.mY[k]
                        
                        # wall or oposite actual dir
                        if k==((dir+2)%4) or self.maze[tmp_x][tmp_y]<0: continue 
                        else: opcs.append(k)

                    # random.
                    opc=random.randint(0,len(opcs)-1)

                    x+=self.mX[opcs[opc]]
                    y+=self.mY[opcs[opc]]
                    self.ghosts_dir[ghost]=opcs[opc]


                else:

                    target=[0,0]

                    # CHASE (in the constructor is the information of how each ghost choose a target)
                    if self.state==0: 

                        if ghost==0:                                # RED. 
                            target[0]=self.agent_pos[0]
                            target[1]=self.agent_pos[1]
                        elif ghost==1:                              # PINK
                            target[0]=self.agent_pos[0]
                            target[1]=self.agent_pos[1]

                            if self.agent_dir==0: 
                                target[0]-=4
                                target[1]-=4
                            elif self.agent_dir==1: target[1]+=4
                            elif self.agent_dir==2: target[0]+=4
                            else: target[1]-=4
                            
                        elif ghost==2:                              # BLUE
                            tmp=[0,0]
                            tmp[0]=self.agent_pos[0]
                            tmp[1]=self.agent_pos[1]

                            if self.agent_dir==0: 
                                tmp[0]-=2
                                tmp[1]-=2
                            elif self.agent_dir==1: tmp[1]+=2
                            elif self.agent_dir==2: tmp[0]+=2
                            else: tmp[1]-=2

                            dif_x=tmp[0]-self.ghosts_pos[0][0]
                            dif_y=tmp[1]-self.ghosts_pos[0][1]
                            target[0]=tmp[0]+dif_x
                            target[1]=tmp[1]+dif_y
                        
                        elif ghost==3:                              # ORANGE
                            dist_manhattan=abs(self.agent_pos[0]-self.ghosts_pos[3][0])
                            dist_manhattan+=abs(self.agent_pos[1]-self.ghosts_pos[3][1])

                            if dist_manhattan<8: target=self.scatter_targets[3]
                            else: target=self.agent_pos

                    # SCATTER
                    else: target=self.scatter_targets[ghost]
                        
                    dist=float("inf")
                    tmp_x=0
                    tmp_y=0
                    dir_idx=0
                    tmp=0
                    for k in range(4):
                        tmp_x=x+self.mX[k]
                        tmp_y=y+self.mY[k]

                        # wall or oposite actual dir
                        if k==((dir+2)%4) or self.maze[tmp_x][tmp_y]<0: continue 
                        else: tmp=self.distance_cells(target,[tmp_x, tmp_y])
                        
                        if dist>tmp:
                            dist=tmp
                            dir_idx=k
                    
                    self.ghosts_dir[ghost]=dir_idx
                    
                    x+=self.mX[dir_idx]
                    y+=self.mY[dir_idx]
            
            # "portals"
            if y==self.m and (x==5 or x==9): y=0
            if y==-1 and (x==5 or x==9): y=self.m-1
            
            
            
            # collides with the agent
            if self.agent_pos[0]==x and self.agent_pos[1]==y:
                
                # FRIGHTENED. is eaten
                if self.state==2:       

                    self.maze[x][y]=self.EMPTY                   

                    self.ghosts_pos[ghost][0]=self.salida_fants[0]+2
                    self.ghosts_pos[ghost][1]=self.salida_fants[1]

                    self.ghost_inHouse.append([ghost,self.exec_tick+3])
                    self.ghosts_house[ghost]=[self.ghosts_pos[ghost][0],self.ghosts_pos[ghost][1]]
                # OTHERWIESE. eats the player
                else: 
                    self.ghosts_pos[ghost][0]=x
                    self.ghosts_pos[ghost][1]=y
                    self.maze[x][y]=color
                    self.end=True     
            else:
                self.ghosts_pos[ghost][0]=x
                self.ghosts_pos[ghost][1]=y
                self.maze[x][y]=color
        
    """
    Calculates the distance of two points given by parameters
           
    :type self: class     
    :type a: int[]
    :type b: int[]
    :rtype: int
    """
    def distance_cells(self, a, b):               
        return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

    # --------------------------------------------------------------------------------
    # --- GUI ------------------------------------------------------------------------
    # --------------------------------------------------------------------------------

    """
    Main loop.

    Waits for a key event, and execute an iteration. (moves the agent and ghosts).
    Prints the maze in the GUI.

    MOVEMENTS KEYS:
    "up"    or "w": UP
    "right" or "d": RIGHT
    "down"  or "s": DOWN
    "left"  or "a": LEFT

    Close the window for exiting the game.
           
    :type self: class  
    :rtype: int
    """
    def execute(self):       

        #self.print_maze()
         
        mov=None

        while True:
            
            while not self.end:            
                
                # -------------------------------------------------------------------------------------------------------------------
                # --- MOVE ----------------------------------------------------------------------------------------------------------
                
                # event = key pressed
                
                for event in pygame.event.get():
                    if event.type==pygame.QUIT: # ends the execution.
                        pygame.quit()
                        sys.exit()
                    elif event.type==pygame.KEYDOWN: # key pressed              
                        if event.key==pygame.K_UP or event.key==pygame.K_w: 
                            mov=self.UP                    
                            self.agent_dir=0
                        elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                            mov=self.RIGHT 
                            self.agent_dir=1
                        elif event.key==pygame.K_DOWN or event.key==pygame.K_s:  
                            mov=self.DOWN    
                            self.agent_dir=2
                        elif event.key==pygame.K_LEFT or event.key==pygame.K_a:  
                            mov=self.LEFT    
                            self.agent_dir=3
                        else: mov=None
                        
                        # run an iteration if the key pressed is binded 
                        if mov!=None:             
                                            
                            self.move_agent(mov)
                            # check for end condition
                            if self.agent_coins==132: self.end=True
                            
                            if self.end!=True:  # no end condition, continues
                                
                                self.move_ghosts()
                                
                                # a ghost leaves the house if is his time
                                if len(self.ghost_inHouse)!=0 and self.exec_tick==self.ghost_inHouse[0][1]:
                                    idx=self.ghost_inHouse.pop(0)[0]

                                    self.maze[self.ghosts_house[idx][0]][self.ghosts_house[idx][1]]=self.EMPTY
                                    self.maze[self.salida_fants[0]][self.salida_fants[1]]=self.ghosts_colors[idx]
                                    self.ghosts_house[idx]=False

                                    self.ghosts_pos[idx][0]=self.salida_fants[0]
                                    self.ghosts_pos[idx][1]=self.salida_fants[1]
                                
                                # update ghost positions (from lower to higher priority)
                                i=3
                                while i>=0:
                                    self.maze[self.ghosts_pos[i][0]][self.ghosts_pos[i][1]]=self.ghosts_colors[i]
                                    i-=1
                                # update agent position
                                if self.end!=True:
                                    self.maze[self.agent_pos[0]][self.agent_pos[1]]=self.AGENT
                            
                # -------------------------------------------------------------------------------------------------------------------
                # --- MAZE ----------------------------------------------------------------------------------------------------------           


                # paint the maze
                self.GUI_maze()

            # -------------------------------------------------------------------------------------------------------------------
            # --- END MESSAGE ---------------------------------------------------------------------------------------------------  

        
            if self.agent_coins==132:   # win condition
                print("\nYOU WIN!!!\n")
                for _ in range(3):
                    self.GUI_message(1)
                    pygame.display.flip()

                    time.sleep(1)

                    self.GUI_maze()
                    pygame.display.flip()

                    time.sleep(0.33)
                    
            else:                       # lose condition
                print("\nGAME OVER\n")

                for _ in range(3):
                    self.GUI_message(0)
                    pygame.display.flip()

                    time.sleep(1)

                    self.GUI_maze()
                    pygame.display.flip()

                    time.sleep(0.33)
                    


            pygame.display.flip()
                    

            self.reset()
    

    """
    Printing in the GUI, the actual state of the maze.
           
    :type self: class  
    :rtype: int
    """
    def GUI_maze(self):
        self.screen.fill((0, 0, 0))  # cleans the screen
                
        for x, row in enumerate(self.maze):
            self.GUI_line(x, row)
            
        # update
        pygame.display.flip()
    

    """
    Printing in the GUI, a message
           
    :type self: class     
    :type t: int
    :rtype: int
    """
    def GUI_message(self, t):

        aux=0 if t==0 else 1

        for x, row in enumerate(self.maze):
            
            if x!=9: self.GUI_line(x, row)
            
            # message row
            else: 

                tmp=0

                for y, cell in enumerate(row):
                    if (y>=6+aux and y<=9) or (y>=11 and y<=14-aux):
                        image=self.message_imgs[t][tmp]
                        tmp+=1
                    else:
                        image=self.GUI_cell(x,y,cell)
                    
                    # draw in the GUI, the actual position of the maze
                    self.screen.blit(image, (y*self.cell_size, x*self.cell_size))
    

    """
    Printing in the GUI, a line
           
    :type self: class     
    :type x: int
    :type row: int[]
    :rtype: None
    """
    def GUI_line(self, x, row):
        for y, cell in enumerate(row):
            image=self.GUI_cell(x,y,cell)

            # draw in the GUI, the actual position of the maze
            self.screen.blit(image, (y*self.cell_size, x*self.cell_size))
            
    
    """
    Printing in the GUI, a cell
           
    :type self: class     
    :type x: int
    :type y: int
    :type cell: int
    :rtype: image
    """
    def GUI_cell(self, x, y, cell):
        
        # walls
        if cell<0: image=self.walls_imgs[abs(cell)-1]  
            
        # ghosts exit door.
        elif cell==1: image=self.walls_imgs[-1]
        
        # in "self.maze" there are no coins. "self.coins_matrix" store the coins and power.
        elif cell==self.EMPTY: 
            if self.coins_matrix[x][y]==self.COIN:      image=self.coin_img
            elif self.coins_matrix[x][y]==self.POWER:   image=self.power_img
            else:                                       image=self.empty_img                                        
        
        # agent.         
        elif cell==self.AGENT: image=self.agent_imgs[self.agent_dir]
        
        # ghost.
        else:
            # FRIGHTENED mode.
            if self.state==2:
                if self.count_state<20: image=self.ghosts_imgs[-1][0]
                
                # blinks to advice the player is finishing the state
                else: 
                    if self.count_state%2==0:   image=self.ghosts_imgs[-1][1]
                    else:                       image=self.ghosts_imgs[-1][0]
            
            # normal mode.
            else:
                if cell==self.RED:      image=self.ghosts_imgs[0][self.ghosts_dir[0]]
                elif cell==self.PINK:   image=self.ghosts_imgs[1][self.ghosts_dir[1]]
                elif cell==self.BLUE:   image=self.ghosts_imgs[2][self.ghosts_dir[2]]
                else:                   image=self.ghosts_imgs[3][self.ghosts_dir[3]]
    
        return image
        
    """
    Loading all the game images. And scale all of them to the same size   
           
    :type self: class     
    :type size: int
    :rtype: int
    """
    def load_images(self, size):

        # -------------------------------------------------------------------------------------------------------------------
        # --- LOAD ----------------------------------------------------------------------------------------------------------      
        
        empty=pygame.image.load('images/empty.png').convert_alpha()    
        coin=pygame.image.load('images/coin.png').convert_alpha()
        power=pygame.image.load('images/power.png').convert_alpha()        
        
        walls=[]        
        names=["images/walls/wall_0.png","images/walls/wall_01.png","images/walls/wall_1.png","images/walls/wall_02.png",
               "images/walls/wall_2.png","images/walls/wall_03.png","images/walls/wall_3.png","images/walls/wall_012.png",
               "images/walls/wall_12.png","images/walls/wall_013.png","images/walls/wall_13.png","images/walls/wall_023.png",
               "images/walls/wall_23.png","images/walls/wall_123.png","images/walls/wall.png","images/walls/z0.png",
               "images/walls/z1.png","images/walls/z2.png","images/walls/z3.png","images/walls/z4.png","images/walls/ghost_exit.png"]
        for wall in names:
            walls.append(pygame.image.load(wall).convert_alpha())
               

        agent=[]
        names=['images/pacman_up.png','images/pacman_right.png','images/pacman_down.png','images/pacman_left.png']
        for dir in names:
            agent.append(pygame.image.load(dir).convert_alpha())
        

        names=[["images/red_up.png","images/red_right.png","images/red_down.png","images/red_left.png"],
               ["images/pink_up.png","images/pink_right.png","images/pink_down.png","images/pink_left.png"],
               ["images/blue_up.png","images/blue_right.png","images/blue_down.png","images/blue_left.png"],
               ["images/orange_up.png","images/orange_right.png","images/orange_down.png","images/orange_left.png"],
               ["images/fright_ghost1.png","images/fright_ghost2.png"]]
        ghosts=[]
        for ghost in names:
            tmp=[]
            for dir in ghost:
                tmp.append(pygame.image.load(dir).convert_alpha())
            ghosts.append(tmp)

        names=[["images/messages/G.png","images/messages/A.png","images/messages/M.png","images/messages/E.png",
                "images/messages/O.png","images/messages/V.png","images/messages/E.png","images/messages/R.png"],                
                ["images/messages/Y.png","images/messages/O_2.png","images/messages/U.png",
                "images/messages/W.png","images/messages/I.png","images/messages/N.png"]]
        messages=[]
        for message in names:
            tmp=[]
            for char in message:
                tmp.append(pygame.image.load(char).convert_alpha())
            messages.append(tmp)

        # -------------------------------------------------------------------------------------------------------------------
        # --- SCALE ---------------------------------------------------------------------------------------------------------      

        self.empty_img=pygame.transform.scale(empty, (size, size))    
        self.coin_img=pygame.transform.scale(coin, (size, size))
        self.power_img=pygame.transform.scale(power, (size, size))

        self.walls_imgs=[]
        self.agent_imgs=[]
        self.ghosts_imgs=[]
        self.message_imgs=[]

        for w in walls:
            self.walls_imgs.append(pygame.transform.scale(w, (size, size)))
        
        for dir in range(4):
            self.agent_imgs.append(pygame.transform.scale(agent[dir], (size, size)))

        
        for g in ghosts:
            tmp=[]
            for dir in g:
                tmp.append(pygame.transform.scale(dir, (size, size)))
                
            self.ghosts_imgs.append(tmp)

        
        for message in messages:
            tmp=[]
            for char in message:
                tmp.append(pygame.transform.scale(char, (size, size)))
                
            self.message_imgs.append(tmp)


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

        self.mX=[-1,0,1,0]
        self.mY=[0,1,0,-1]

        # Elementos del tablero
        self.VACIO=0
        self.MURO=1
        self.MONEDA=2
        self.POWER=3
        self.AGENTE=4
        # fantasmas
        self.ROJO=5
        self.ROSA=6
        self.AZUL=7
        self.NARANJA=8
        self.COLORES_FANTS=[5,6,7,8]

        # Acciones
        self.ARRIBA='arriba'
        self.ABAJO='abajo'
        self.IZQUIERDA='izquierda'
        self.DERECHA='derecha'
        
        self.acciones = [self.ARRIBA, self.DERECHA, self.ABAJO, self.IZQUIERDA]

        self.state_ticks=[60,30,30]

        
        
        self.reset()

        self.scatter_targets=[[0,self.m],[0,0],[self.n,0],[self.n,self.m]]
        

        if GUI==True:
            # conf: ventana
            self.tam_celda=30
            self.alto=self.n*self.tam_celda
            self.ancho=self.m*self.tam_celda

            # init pygame
            pygame.init()       
            self.pantalla=pygame.display.set_mode((self.ancho, self.alto))
            pygame.display.set_caption('Pac-Man') 

            # Imagenes
            self.empty_img=[]
            self.coin_img=[]
            self.power_img=[]
            self.walls_imgs=[]
            self.agente_imgs=[]
            self.ghosts_imgs=[]
            self.cargar_imagenes(self.tam_celda)

            self.mostrar_laberinto()

    def reset(self):
        self.cont=0
        # 0: CHASE, 1: SCATTER, 2: FRIGHTENED
        self.state=1
        self.cont_state=0

        # Agente
        self.posicion_agente=None
        self.direccion=1
        self.monedas=0   

        # Fantasmas
        self.posicion_fants=[[0,0] for _ in range(4)]
        self.direccion_fants=[1,2,0,0]
        self.casa_fants=[False,True,True,True]
        self.en_casa=[[1,3],[2,6],[3,9]]
        
        # Laberinto
        self.laberinto=[]
        self.monedas_matriz=[]
        self.leer_laberinto(self.archivo)
        self.n=len(self.laberinto)
        self.m=len(self.laberinto[0])

        self.fin=False

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
        fin=self.monedas==132 #TODO FANTASMAS
        #all(self.laberinto[i][j] != self.MONEDA for i in range(self.n) for j in range(self.m))
        
        return estado_sig, recompensa, fin

    # Leer el laberinto desde un archivo
    def leer_laberinto(self, archivo):  
        cont=0

        with open(archivo, 'r') as file:        
            for line in file:
                row=list(map(int, line.split()))
                self.laberinto.append([0 for _ in range(len(row))])
                self.monedas_matriz.append([0 for _ in range(len(row))])
                
                for i in range(len(row)):   
                    if row[i]==2: self.laberinto[cont][i]=0
                    else: self.laberinto[cont][i]=row[i]
                
                for i in range(len(row)):                    
                    self.monedas_matriz[cont][i]=row[i]
                
                
                cont+=1
                
                
        
        self.imprime_laberinto()

        cont=0
        for x in range(len(self.laberinto)):
            for y in range(len(self.laberinto[0])):                    
                if self.laberinto[x][y]==self.AGENTE: 
                    self.posicion_agente=[x,y]
                    cont+=1
                    if cont==5: break  

                elif self.laberinto[x][y]==self.ROJO: 
                    self.posicion_fants[0]=[x,y]
                    self.salida_fants=[x,y]
                    cont+=1
                    if cont==5: break
                elif self.laberinto[x][y]==self.ROSA: 
                    self.posicion_fants[1]=[x,y]
                    self.casa_fants[1]=[x,y]
                    cont+=1
                    if cont==5: break
                elif self.laberinto[x][y]==self.AZUL: 
                    self.posicion_fants[2]=[x,y]
                    self.casa_fants[2]=[x,y]
                    cont+=1
                    if cont==5: break
                elif self.laberinto[x][y]==self.NARANJA: 
                    self.posicion_fants[3]=[x,y]
                    self.casa_fants[3]=[x,y]
                    cont+=1
                    if cont==5: break
        
        
        
                    

    
    def imprime_laberinto(self):
        print("Laberinto")

        for x in range(len(self.laberinto)):
            for y in range(len(self.laberinto[0])):
                if self.laberinto[x][y]<0: 
                    print(-1, end=" ")
                else: print(self.laberinto[x][y], end=" ")
            print()

    def imprime_monedas(self):
        print("Matriz de Monedas")

        for x in range(len(self.monedas_matriz)):
            for y in range(len(self.monedas_matriz[0])):
                if self.monedas_matriz[x][y]<0: 
                    print(-1, end=" ")
                else: print(self.monedas_matriz[x][y], end=" ")
            print()

    # Mueve al agente
    def mover_agente(self, mov):
        x=self.posicion_agente[0]
        y=self.posicion_agente[1] 
        #m=len(self.laberinto[0])
        moneda=0
        
        self.cont+=1

        if mov==self.ARRIBA:
            if x>0 and self.laberinto[x-1][y]>=0:
                if self.monedas_matriz[x-1][y]==self.MONEDA: 
                    self.monedas_matriz[x-1][y]=0
                    moneda=1
                elif self.monedas_matriz[x-1][y]==self.POWER: 
                    self.monedas_matriz[x-1][y]=0
                    self.state=2
                    self.cont_state=0
                    for i in range(4):                        
                        if not self.casa_fants[i]:
                            self.direccion_fants[i]+=2
                            self.direccion_fants[i]%=4                        
                self.laberinto[x][y]=self.VACIO
                x-=1
        elif mov==self.ABAJO:
            if x<len(self.laberinto)-1 and self.laberinto[x+1][y]>=0:
                if self.monedas_matriz[x+1][y]==self.MONEDA: 
                    self.monedas_matriz[x+1][y]=0
                    moneda=1
                elif self.monedas_matriz[x+1][y]==self.POWER: 
                    self.monedas_matriz[x+1][y]=0
                    self.state=2
                    self.cont_state=0
                    for i in range(4):
                        if not self.casa_fants[i]:
                            self.direccion_fants[i]+=2
                            self.direccion_fants[i]%=4
                self.laberinto[x][y]=self.VACIO
                x+=1
        elif mov==self.IZQUIERDA:
            if y>0 and self.laberinto[x][y-1]>=0:
                if self.monedas_matriz[x][y-1]==self.MONEDA: 
                    self.monedas_matriz[x][y-1]=0
                    moneda=1
                self.laberinto[x][y]=self.VACIO
                y-=1
            elif y==0 and (x==5 or x==9): # TODO
                if self.monedas_matriz[x][self.m-1]==self.MONEDA: 
                    self.monedas_matriz[x][self.m-1]=0
                    moneda=1
                self.laberinto[x][y]=self.VACIO
                y=self.m-1
        elif mov==self.DERECHA:
            if y<self.m-1 and self.laberinto[x][y+1]>=0:
                if self.monedas_matriz[x][y+1]==self.MONEDA: 
                    self.monedas_matriz[x][y+1]=0
                    moneda=1
                self.laberinto[x][y]=self.VACIO
                y+=1
            elif y==self.m-1 and (x==5 or x==9): # TODO
                if self.monedas_matriz[x][0]==self.MONEDA: 
                    self.monedas_matriz[x][0]=0
                    moneda=1
                self.laberinto[x][y]=self.VACIO
                y=0
        
        if self.state==2:
            comidos=[]
            for i in range(4):
                if self.posicion_fants[i][0]==x and self.posicion_fants[i][1]==y:
                    comidos.append(i)
            
            contador=1
            for i in comidos:
                self.posicion_fants[i][0]=self.salida_fants[0]+2
                self.posicion_fants[i][1]=self.salida_fants[1]
                self.en_casa.append([i,self.cont+(3*contador)])
                self.casa_fants[i]=[self.posicion_fants[i][0],self.posicion_fants[i][1]]

                contador+=1
        else:
            for i in range(4):
                if self.posicion_fants[i][0]==x and self.posicion_fants[i][1]==y: 
                    self.fin=True
                    self.laberinto[self.posicion_agente[0]][self.posicion_agente[1]]=self.VACIO

        if self.fin!=True:
            self.laberinto[x][y]=self.AGENTE
            self.posicion_agente=[x,y]
            self.monedas+=moneda
        return moneda

    def mover_fants(self):
        
                          
        self.mover_fantasma(0) 
        self.mover_fantasma(1)
        self.mover_fantasma(2)
        self.mover_fantasma(3)


            

        self.cont_state+=1
        print("Estado=", self.cont_state, "\tMonedas=",self.monedas)
        if self.cont_state==self.state_ticks[self.state]:          
            
            if self.state==0: 
                self.state=1
                print("NUEVO ESTADO: SCATTER",end="")
            else: 
                self.state=0
                print("NUEVO ESTADO: CHASE",end="")

            for i in range(4):
                if not self.casa_fants[i]:
                    self.direccion_fants[i]+=2
                    self.direccion_fants[i]%=4
            
            print("\tGIRA 180º")

            self.cont_state=0

    def mover_fantasma(self, fantasma):
        x=0
        y=0
        dir=0
        color=self.ROJO
        if fantasma==1: color=self.ROSA
        elif fantasma==2: color=self.AZUL
        elif fantasma==3: color=self.NARANJA

        aux_x=0
        aux_y=0
        
        
        if not self.casa_fants[fantasma] and (not(self.state==2 and self.cont_state%2==0)):
            """print("SE MUEVE:",self.COLORES_FANTS[fantasma], "POS:", self.posicion_fants[fantasma])"""
            dir=self.direccion_fants[fantasma]
            x=self.posicion_fants[fantasma][0]
            y=self.posicion_fants[fantasma][1]
            if dir==0 or dir==2: aux_y=1
            else: aux_x=1
            
            self.laberinto[x][y]=self.VACIO

            """print(self.posicion_agente)"""

            # Se mueve para la direccion si no esta en una interseccion
            if self.laberinto[x+aux_x][y+aux_y]<0 and self.laberinto[x-aux_x][y-aux_y]<0:                                
                """print("MUEVE")"""

                if dir==0: x-=1
                elif dir==1: y+=1
                elif dir==2: x+=1
                else: y-=1
            
            
                
            else: 
                if self.state==2: # FRIGHTENED
                    """print("FRIGHTENED")"""
                    opcs=[]
                    for k in range(4):
                        tmp_x=x+self.mX[k]
                        tmp_y=y+self.mY[k]
                        if k==((dir+2)%4) or self.laberinto[tmp_x][tmp_y]<0: continue # no puede ir para atras
                        opcs.append(k)
                    opc=random.randint(0,len(opcs)-1)
                    x+=self.mX[opcs[opc]]
                    y+=self.mY[opcs[opc]]
                    self.direccion_fants[fantasma]=opcs[opc]


                else:
                    target=[0,0]
                    if self.state==0: # CHASE
                        """print("CHASE")"""
                        if fantasma==0: 
                            target[0]=self.posicion_agente[0]
                            target[1]=self.posicion_agente[1]
                        elif fantasma==1: 
                            target[0]=self.posicion_agente[0]
                            target[1]=self.posicion_agente[1]

                            if self.direccion==0: 
                                target[0]-=4
                                target[1]-=4
                            elif self.direccion==1: target[1]+=4
                            elif self.direccion==2: target[0]+=4
                            else: target[1]-=4
                            
                        elif fantasma==2: 
                            tmp=[0,0]
                            tmp[0]=self.posicion_agente[0]
                            tmp[1]=self.posicion_agente[1]

                            if self.direccion==0: 
                                tmp[0]-=2
                                tmp[1]-=2
                            elif self.direccion==1: tmp[1]+=2
                            elif self.direccion==2: tmp[0]+=2
                            else: tmp[1]-=2

                            dif_x=tmp[0]-self.posicion_fants[0][0]
                            dif_y=tmp[1]-self.posicion_fants[0][1]
                            target[0]=tmp[0]+dif_x
                            target[1]=tmp[1]+dif_y
                        
                        elif fantasma==3:
                            dist_manhattan=abs(self.posicion_agente[0]-self.posicion_fants[3][0])
                            dist_manhattan+=abs(self.posicion_agente[1]-self.posicion_fants[3][1])

                            if dist_manhattan<8: target=self.scatter_targets[3]
                            else: target=self.posicion_agente


                    else: # SCATTER
                        """print("SCATTER")"""
                        target=self.scatter_targets[fantasma]
                        
                    dist=float("inf")
                    tmp_x=0
                    tmp_y=0
                    dir_idx=0
                    tmp=0
                    for k in range(4):
                        tmp_x=x+self.mX[k]
                        tmp_y=y+self.mY[k]
                        if k==((dir+2)%4) or self.laberinto[tmp_x][tmp_y]<0: continue # no puede ir para atras
                        tmp=self.distancia_celda(target,[tmp_x, tmp_y])
                        """print("pos= {},{}\tdist= {}".format(tmp_x, tmp_y, tmp))"""
                        if dist>tmp:
                            dist=tmp
                            dir_idx=k
                    """print("direccion:", dir_idx)"""
                    self.direccion_fants[fantasma]=dir_idx
                    
                    x+=self.mX[dir_idx]
                    y+=self.mY[dir_idx]
            
            # "portales"
            if y==self.m and (x==5 or x==9): y=0
            if y==-1 and (x==5 or x==9): y=self.m-1
            
            """print(self.m, x, y)"""
            self.posicion_fants[fantasma][0]=x
            self.posicion_fants[fantasma][1]=y
            self.laberinto[x][y]=color

            if self.posicion_agente[0]==x and self.posicion_agente[1]==y:
                if self.state==2:
                    self.laberinto[x][y]=self.VACIO                   

                    self.posicion_fants[fantasma][0]=self.salida_fants[0]+2
                    self.posicion_fants[fantasma][1]=self.salida_fants[1]

                    self.en_casa.append([fantasma,self.cont+3])
                    self.casa_fants[fantasma]=[self.posicion_fants[fantasma][0],self.posicion_fants[fantasma][1]]
                else: self.fin=True
        """else:
            print("no MUEVE:",self.COLORES_FANTS[fantasma], "POS:", self.posicion_fants[fantasma])"""
    
    def distancia_celda(self, a, b):               
        return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


    """def ejecuta(self):

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

            pygame.display.flip()"""

    # --------------------------------------------------------------------------------
    # --- GUI ------------------------------------------------------------------------
    # --------------------------------------------------------------------------------

    # Función para inicializar pygame y mostrar el laberinto en una ventana
    def mostrar_laberinto(self):       

        #self.imprime_laberinto()
         
        mov=None
        imagen=None
        while True:

            # bucle principal
            while not self.fin:            
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
                            
                            self.mover_fants()
                            
                            if len(self.en_casa)!=0 and self.cont==self.en_casa[0][1]:
                                idx=self.en_casa.pop(0)[0]

                                self.laberinto[self.casa_fants[idx][0]][self.casa_fants[idx][1]]=self.VACIO
                                self.laberinto[self.salida_fants[0]][self.salida_fants[1]]=self.COLORES_FANTS[idx]
                                self.casa_fants[idx]=False

                                self.posicion_fants[idx][0]=self.salida_fants[0]
                                self.posicion_fants[idx][1]=self.salida_fants[1]
                            
                            # fantasmas
                            i=3
                            while i>=0:
                                self.laberinto[self.posicion_fants[i][0]][self.posicion_fants[i][1]]=self.COLORES_FANTS[i]
                                i-=1
                            # agente
                            if self.fin!=True:
                                self.laberinto[self.posicion_agente[0]][self.posicion_agente[1]]=self.AGENTE
                            
                            if self.monedas==132: self.fin=True


                # dibuja el laberinto
                self.GUI_laberinto()
            
            if self.fin==True:
                if self.monedas==132: 
                    print("\nGANASTE\n")
                    for _ in range(3):
                        self.GUI_mensaje(1)
                        pygame.display.flip()
                        time.sleep(1)
                        self.GUI_laberinto()
                        time.sleep(0.33)
                        pygame.display.flip()
                else: 
                    print("\nPERDISTE\n")

                    for _ in range(3):
                        self.GUI_mensaje(0)
                        pygame.display.flip()
                        time.sleep(1)
                        self.GUI_laberinto()
                        time.sleep(0.33)
                        pygame.display.flip()


                pygame.display.flip()
                    

                self.reset()
    
    def GUI_laberinto(self):
        self.pantalla.fill((0, 0, 0))  # limpia antes de dibujar
        
        # recorre el laberinto
        for x, fila in enumerate(self.laberinto):
            for y, celda in enumerate(fila):
                if celda<0:
                    imagen=self.walls_imgs[abs(celda)-1]  
                elif celda==1: imagen=self.walls_imgs[-1]
                elif celda==self.VACIO: 
                    if self.monedas_matriz[x][y]==self.MONEDA: imagen=self.coin_img
                    elif self.monedas_matriz[x][y]==self.POWER: imagen=self.power_img
                    else: imagen=self.empty_img                                        
                elif celda==self.POWER: imagen=self.power_img
                elif celda==self.AGENTE: imagen=self.agente_imgs[self.direccion] 
                else:
                    if self.state==2:
                        if self.cont_state<20: imagen=self.ghosts_imgs[-1][0]
                        else:
                            if self.cont_state%2==0: imagen=self.ghosts_imgs[-1][1]
                            else: imagen=self.ghosts_imgs[-1][0]
                    else:
                        if celda==self.ROJO: imagen=self.ghosts_imgs[0][self.direccion_fants[0]]
                        elif celda==self.ROSA: imagen=self.ghosts_imgs[1][self.direccion_fants[1]]
                        elif celda==self.AZUL: imagen=self.ghosts_imgs[2][self.direccion_fants[2]]
                        else: imagen=self.ghosts_imgs[3][self.direccion_fants[3]]
                

                self.pantalla.blit(imagen, (y*self.tam_celda, x*self.tam_celda))

        pygame.display.flip()
    
    def GUI_mensaje(self, tipo):
        aux=0 if tipo==0 else 1

        for x, fila in enumerate(self.laberinto):
            if x!=9:
                for y, celda in enumerate(fila):
                    if celda<0:
                        imagen=self.walls_imgs[abs(celda)-1]  
                    elif celda==1: imagen=self.walls_imgs[-1]
                    elif celda==self.VACIO: 
                        if self.monedas_matriz[x][y]==self.MONEDA: imagen=self.coin_img
                        elif self.monedas_matriz[x][y]==self.POWER: imagen=self.power_img
                        else: imagen=self.empty_img                                        
                    elif celda==self.POWER: imagen=self.power_img
                    elif celda==self.AGENTE: imagen=self.agente_imgs[self.direccion] 
                    else:
                        if self.state==2:
                            if self.cont_state<20: imagen=self.ghosts_imgs[-1][0]
                            else:
                                if self.cont_state%2==0: imagen=self.ghosts_imgs[-1][1]
                                else: imagen=self.ghosts_imgs[-1][0]
                        else:
                            if celda==self.ROJO: imagen=self.ghosts_imgs[0][self.direccion_fants[0]]
                            elif celda==self.ROSA: imagen=self.ghosts_imgs[1][self.direccion_fants[1]]
                            elif celda==self.AZUL: imagen=self.ghosts_imgs[2][self.direccion_fants[2]]
                            else: imagen=self.ghosts_imgs[3][self.direccion_fants[3]]
                    self.pantalla.blit(imagen, (y*self.tam_celda, x*self.tam_celda))
            else:
                contador=0
                for y, celda in enumerate(fila):
                    if (y>=6+aux and y<=9) or (y>=11 and y<=14-aux):
                        imagen=self.message_imgs[tipo][contador]
                        contador+=1
                    else:
                        if celda<0:
                            imagen=self.walls_imgs[abs(celda)-1]  
                        elif celda==1: imagen=self.walls_imgs[-1]
                        elif celda==self.VACIO: 
                            if self.monedas_matriz[x][y]==self.MONEDA: imagen=self.coin_img
                            elif self.monedas_matriz[x][y]==self.POWER: imagen=self.power_img
                            else: imagen=self.empty_img                                        
                        elif celda==self.POWER: imagen=self.power_img
                        elif celda==self.AGENTE: imagen=self.agente_imgs[self.direccion] 
                        else:
                            if self.state==2:
                                if self.cont_state<20: imagen=self.ghosts_imgs[-1][0]
                                else:
                                    if self.cont_state%2==0: imagen=self.ghosts_imgs[-1][1]
                                    else: imagen=self.ghosts_imgs[-1][0]
                            else:
                                if celda==self.ROJO: imagen=self.ghosts_imgs[0][self.direccion_fants[0]]
                                elif celda==self.ROSA: imagen=self.ghosts_imgs[1][self.direccion_fants[1]]
                                elif celda==self.AZUL: imagen=self.ghosts_imgs[2][self.direccion_fants[2]]
                                else: imagen=self.ghosts_imgs[3][self.direccion_fants[3]]
                    self.pantalla.blit(imagen, (y*self.tam_celda, x*self.tam_celda))
        

    def cargar_imagenes(self, tam):
        # leer las imagenes
        vacio=pygame.image.load('imagenes/empty.png').convert_alpha()    
        moneda=pygame.image.load('imagenes/coin.png').convert_alpha()
        power=pygame.image.load('imagenes/power.png').convert_alpha()
        
        
        walls=[]
        
        names=["imagenes/walls/wall_0.png","imagenes/walls/wall_01.png","imagenes/walls/wall_1.png","imagenes/walls/wall_02.png",
               "imagenes/walls/wall_2.png","imagenes/walls/wall_03.png","imagenes/walls/wall_3.png","imagenes/walls/wall_012.png",
               "imagenes/walls/wall_12.png","imagenes/walls/wall_013.png","imagenes/walls/wall_13.png","imagenes/walls/wall_023.png",
               "imagenes/walls/wall_23.png","imagenes/walls/wall_123.png","imagenes/walls/wall.png","imagenes/walls/z0.png",
               "imagenes/walls/z1.png","imagenes/walls/z2.png","imagenes/walls/z3.png","imagenes/walls/z4.png","imagenes/walls/ghost_exit.png"]
        for wall in names:
            walls.append(pygame.image.load(wall).convert_alpha())
               

        agente=[]
        agente.append(pygame.image.load('imagenes/pacman_up.png').convert_alpha())
        agente.append(pygame.image.load('imagenes/pacman_right.png').convert_alpha())
        agente.append(pygame.image.load('imagenes/pacman_down.png').convert_alpha())
        agente.append(pygame.image.load('imagenes/pacman_left.png').convert_alpha())

        names=[["imagenes/red_up.png","imagenes/red_right.png","imagenes/red_down.png","imagenes/red_left.png"],
               ["imagenes/pink_up.png","imagenes/pink_right.png","imagenes/pink_down.png","imagenes/pink_left.png"],
               ["imagenes/blue_up.png","imagenes/blue_right.png","imagenes/blue_down.png","imagenes/blue_left.png"],
               ["imagenes/orange_up.png","imagenes/orange_right.png","imagenes/orange_down.png","imagenes/orange_left.png"],
               ["imagenes/fright_ghost1.png","imagenes/fright_ghost2.png"]]
        ghosts=[]
        for color in names:
            tmp=[]
            for name in color:
                tmp.append(pygame.image.load(name).convert_alpha())
            ghosts.append(tmp)

        names=[["imagenes/messages/G.png","imagenes/messages/A.png","imagenes/messages/M.png","imagenes/messages/E.png",
                "imagenes/messages/O.png","imagenes/messages/V.png","imagenes/messages/E.png","imagenes/messages/R.png"],                
                ["imagenes/messages/Y.png","imagenes/messages/O_2.png","imagenes/messages/U.png",
                "imagenes/messages/W.png","imagenes/messages/I.png","imagenes/messages/N.png"]]
        messages=[]
        for message in names:
            tmp=[]
            for char in message:
                tmp.append(pygame.image.load(char).convert_alpha())
            messages.append(tmp)

        # escalar para que tengan el mismo tamaño
        self.empty_img=pygame.transform.scale(vacio, (tam, tam))    
        self.coin_img=pygame.transform.scale(moneda, (tam, tam))
        self.power_img=pygame.transform.scale(power, (tam, tam))

        self.walls_imgs=[]
        self.agente_imgs=[]
        for w in walls:
            self.walls_imgs.append(pygame.transform.scale(w, (tam, tam)))
        
        for i in range(4):
            self.agente_imgs.append(pygame.transform.scale(agente[i], (tam, tam)))

        self.ghosts_imgs=[]
        for g in ghosts:
            tmp=[]
            for dir in g:
                tmp.append(pygame.transform.scale(dir, (tam, tam)))
                
            self.ghosts_imgs.append(tmp)

        self.message_imgs=[]
        for message in messages:
            tmp=[]
            for char in message:
                tmp.append(pygame.transform.scale(char, (tam, tam)))
                
            self.message_imgs.append(tmp)
    

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
    
    """env=PacmanGUI(os.path.join("datos", "env.txt"),True)"""
    
    
