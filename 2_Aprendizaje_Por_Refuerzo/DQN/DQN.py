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
        self.version=int(file_name[8])
        self.win_condition=132 if self.version==1 else 21
        
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
                
        
        self.ghosts_colors  =[]
        self.state_ticks    =[]
        if self.version==1:
            self.ghosts_colors  =[5,6,7,8]
            self.state_ticks    =[60,30,30]
        else:
            self.ghosts_colors  =[5]
            self.state_ticks    =[20,10,10]

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
        self.n_ghosts=4 if self.version==1 else 1
        self.ghosts_pos=[[0,0] for _ in range(self.n_ghosts)]
        if self.version==1:
            self.ghosts_dir=[1,2,0,0]
            self.ghosts_house=[False,True,True,True]
            # queue, for the leaving order. 0th: ghost id. 1th: home leaving tick
            self.ghost_inHouse=[[1,3],[2,6],[3,9]]
        else:
            self.ghosts_dir=[3]
            self.ghosts_house=[False]
            # queue, for the leaving order. 0th: ghost id. 1th: home leaving tick
            self.ghost_inHouse=[]
        
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

        self.ghosts_pos=[[0,0] for _ in range(self.n_ghosts)]
        if self.version==1:
            self.ghosts_dir=[1,2,0,0]
            self.ghosts_house=[False,True,True,True]
            # queue, for the leaving order. 0th: ghost id. 1th: home leaving tick
            self.ghost_inHouse=[[1,3],[2,6],[3,9]]
        else:
            self.ghosts_dir=[3]
            self.ghosts_house=[False]
            # queue, for the leaving order. 0th: ghost id. 1th: home leaving tick
            self.ghost_inHouse=[]
        
        self.maze=[]
        self.coins_matrix=[]
        self.read_maze()
        self.n=len(self.maze)
        self.m=len(self.maze[0])

        if self.version==1:
            self.scatter_targets=[[0,self.m],[0,0],[self.n,self.m],[self.n,0]]
        else:  self.scatter_targets=[[0,4]]

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
                    for i in range(self.n_ghosts):                        
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
                    for i in range(self.n_ghosts):
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
                elif self.coins_matrix[x][y-1]==self.POWER: # POWER. change the game state to FRIGHTENED
                    self.coins_matrix[x][y-1]=0
                    self.state=2
                    self.count_state=0
                    
                    # change the directions of the ghosts
                    for i in range(self.n_ghosts):                        
                        if not self.ghosts_house[i]:
                            self.ghosts_dir[i]+=2
                            self.ghosts_dir[i]%=4 
                
                self.maze[x][y]=self.EMPTY
                y-=1
                
            elif y==0 and self.portal_gates(x):           # "portal"                                 
                self.maze[x][y]=self.EMPTY
                y=self.m-1

        elif mov==self.RIGHT:
            if y<self.m-1 and self.maze[x][y+1]>=0:         # dest position != wall
                if self.coins_matrix[x][y+1]==self.COIN:    # COIN. adds a coin
                    self.coins_matrix[x][y+1]=0
                    coin=1
                elif self.coins_matrix[x][y+1]==self.POWER: # POWER. change the game state to FRIGHTENED
                    self.coins_matrix[x][y+1]=0
                    self.state=2
                    self.count_state=0
                    for i in range(self.n_ghosts):
                        if not self.ghosts_house[i]:
                            self.ghosts_dir[i]+=2
                            self.ghosts_dir[i]%=4
                
                self.maze[x][y]=self.EMPTY
                y+=1
                
            elif y==self.m-1 and self.portal_gates(x):    # "portal"                             
                self.maze[x][y]=self.EMPTY
                y=0
        
        # -------------------------------------------------------------------------------------------------------------------
        # --- EAT/LOSE ------------------------------------------------------------------------------------------------------

        if self.state==2:   # eat.
            eaten=[]
            for i in range(self.n_ghosts):
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
            for i in range(self.n_ghosts):
                if self.ghosts_pos[i][0]==x and self.ghosts_pos[i][1]==y: 
                    self.end=True
                    self.maze[self.agent_pos[0]][self.agent_pos[1]]=self.EMPTY

        # if the player hasnt lose, he moves 
        if self.end!=True:
            self.maze[x][y]=self.AGENT
            self.agent_pos=[x,y]
            self.agent_coins+=coin
            
        return coin


    def portal_gates(self, x):
        if self.version==0: return (x==5 or x==9)
        else: return x==4

    """
    Moving the ghosts.
    Also change the game state
           
    :type self: class     
    :rtype: None
    """
    def move_ghosts(self):
        
        # -------------------------------------------------------------------------------------------------------------------
        # --- MOVE ----------------------------------------------------------------------------------------------------------

        for i in range(self.n_ghosts):
            self.move_ghost(i) 
        

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

            for i in range(self.n_ghosts):
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
            if y==self.m and self.portal_gates(x): y=0
            if y==-1 and self.portal_gates(x): y=self.m-1
            
            
            
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
                            if self.agent_coins==self.win_condition: self.end=True
                            
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
                                i=self.n_ghosts-1
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

        
            if self.agent_coins==self.win_condition:   # win condition
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
            return random.randint(0, 3)  
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

    def __init__(self,file_name):
        self.file_name=file_name
        self.version=int(file_name[8]) 
        self.win_condition=132 if self.version==1 else 21
        
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
        self.RIGHT  ='right'        
        self.DOWN   ='down' 
        self.LEFT   ='left'       
        

        self.actions=[self.UP,self.RIGHT, self.DOWN, self.LEFT]

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
        self.n_ghosts=4 if self.version==1 else 1
        if self.n_ghosts==4:
            self.ghosts_pos=[[0,0] for _ in range(4)]
            self.ghosts_dir=[1,2,0,0]
            self.ghosts_house=[False,True,True,True]
            # queue, for the leaving order. 0th: ghost id. 1th: home leaving tick
            self.ghost_inHouse=[[1,3],[2,6],[3,9]]
        else:
            self.ghosts_pos=[[0,0]]
            self.ghosts_dir=[3]
            self.ghosts_house=[False]
            # queue, for the leaving order. 0th: ghost id. 1th: home leaving tick
            self.ghost_inHouse=[]
        
        # maze.
        self.maze=[]    # used for the walls, agent and ghosts positions in the GUI                
        self.n=0        # number of rows
        self.m=0        # number of coloumns

        # finalization variable
        self.end=False

        self.reset(True,None,None,None,None)
    
        

        #self.execute()
        

        

    """
    Getting the actual state.
    
    Return an array=flatten the maze, and add the positions of the agent and ghosts

    :type self: class    
    :rtype: int[]
    """  
    def get_state(self):

        state=[]
        for row in self.maze:
            state.extend(row)

        state.append(self.agent_pos[0])
        state.append(self.agent_pos[1])
        #state.append(self.agent_coins) # not useful
        for i in range(self.n_ghosts):
            state.append(self.ghosts_pos[i][0])
            state.append(self.ghosts_pos[i][1])

        return state

    def step(self, accion):                
        eat=self.move_agent(self.actions[accion])
        self.move_ghosts()
        
        next_state=self.get_state()

        aux=""
        
        
        reward=-1           # move without eating

        if eat==1:          # power        
            reward=5        
            aux="POWER"
        elif eat==2:        # coin
            reward=10      
            aux="COIN"
        elif eat==3:        # portal
            reward=20      
            aux="PORTAL"
        elif eat==4:        # ghost
            reward=100     
            aux="GHOST"
        elif eat==5:        # has been eaten by a ghost
            reward=-100    
            aux="PIERDE"
        
        # has been eaten by a ghost
        if self.end==True:
            if self.agent_coins!=self.win_condition: 
                reward=-100
                aux="PIERDE"
            else:                 
                reward=1000
                aux="GANA"
        
        a="N"
        if accion==1: a="E"
        elif accion==2: a="S"
        elif accion==3: a="W"
        print("{}\tTick={}  \tState={}  \tCoins={}  \t{}\tAgent= {}\tGhost= {}".format(a,self.exec_tick, 
                                                                                                 self.count_state, self.agent_coins,aux,
                                                                                                 self.agent_pos, self.ghosts_pos[0]))
        
        

        
        return next_state, reward, self.end

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


    """
    Reseting the class variables.

    :type self: class    
    :rtype: None
    """
    def reset(self,init,positions,coins,states,dirs):

        self.exec_tick=0

        self.state=1
        self.count_state=0
        
        self.agent_pos=None
        self.agent_dir=1
        self.agent_coins=0   
        
        if self.n_ghosts==4:
            self.ghosts_pos=[[0,0] for _ in range(4)]
            self.ghosts_dir=[1,2,0,0]
            self.ghosts_house=[False,True,True,True]
            # queue, for the leaving order. 0th: ghost id. 1th: home leaving tick
            self.ghost_inHouse=[[1,3],[2,6],[3,9]]
        else:
            self.ghosts_pos=[[0,0]]
            self.ghosts_dir=[3]
            self.ghosts_house=[False]
            # queue, for the leaving order. 0th: ghost id. 1th: home leaving tick
            self.ghost_inHouse=[]
        
        self.maze=[]
        self.read_maze()
        self.n=len(self.maze)
        self.m=len(self.maze[0])

        if self.version==1:
            self.scatter_targets=[[0,self.m],[0,0],[self.n,self.m],[self.n,0]]
        else:  self.scatter_targets=[[0,4]]

        self.end=False

        if init==False:
            idx=int(self.file_name[10])            
            if idx>0:
                self.ghosts_house=[False,False,False,False]
                self.ghost_inHouse=[]

                self.exec_tick=states[idx]            
                self.count_state=states[idx]
                self.agent_coins=coins[idx]

                if self.version==1:
                    self.salida_fants=[5,10]
                else: self.salida_fants=[2,5]
                
                for g in range(self.n_ghosts):
                    self.ghosts_pos[g][0]=positions[idx][g][0]
                    self.ghosts_pos[g][1]=positions[idx][g][1]
                    self.ghosts_dir[g]=dirs[idx][g]



        return self.get_state()
    
    """
    Reading the maze from a .txt file. 
    Also search for the positions of the agent and ghosts
    
    :type self: class        
    :rtype: None
    """
    """
    Reading the maze from a .txt file. 
    Also search for the positions of the agent and ghosts
    
    :type self: class        
    :rtype: None
    """
    def read_maze(self):                

        with open(self.file_name, 'r') as file:        
            for x, line in enumerate(file):
                row=list(map(int, line.split()))
                self.maze.append([0 for _ in range(len(row))])
                
                for y in range(len(row)):                                          
                    
                    if row[y]==self.AGENT: 
                        self.maze[x][y]=0
                        self.agent_pos=[x,y]
                    
                    elif row[y]==self.RED: 
                        self.maze[x][y]=0
                        self.ghosts_pos[0]=[x,y]                    
                        self.salida_fants=[x,y]

                    elif row[y]==self.PINK: 
                        self.maze[x][y]=0
                        self.ghosts_pos[1]=[x,y]
                        self.ghosts_house[1]=[x,y]
                        

                    elif row[y]==self.BLUE: 
                        self.maze[x][y]=0
                        self.ghosts_pos[2]=[x,y]
                        self.ghosts_house[2]=[x,y]

                    elif row[y]==self.ORANGE: 
                        self.maze[x][y]=0
                        self.ghosts_pos[3]=[x,y]
                        self.ghosts_house[3]=[x,y]

                    else: 
                        self.maze[x][y]=row[y]

        
                               
                
                               
        
        
    
    """
    Moving the agent.
    eat ghosts or is eaten by a ghost
    
    return: 1, if the agent eat a coin. 
            0, otherwise
    
    :type self: class 
    :type mov: string
    :rtype: (int, int)
    """
    def move_agent(self, mov):
        x=self.agent_pos[0]
        y=self.agent_pos[1] 
        
        ret=0
        
        

        # -------------------------------------------------------------------------------------------------------------------
        # --- MOVE ----------------------------------------------------------------------------------------------------------

        # POWER is only reachable by up and down actions

        if mov==self.UP:            
            if x>0 and self.maze[x-1][y]!=1:                # dest position != wall
                if self.maze[x-1][y]==self.COIN:    # COIN. adds a coin
                    self.maze[x-1][y]=0
                    ret=2

                elif self.maze[x-1][y]==self.POWER: # POWER. change the game state to FRIGHTENED
                    self.maze[x-1][y]=0
                    self.state=2
                    self.count_state=0
                    ret=1

                    # change the directions of the ghosts
                    for i in range(self.n_ghosts):                        
                        if not self.ghosts_house[i]:
                            self.ghosts_dir[i]+=2
                            self.ghosts_dir[i]%=4                        
                
                
                x-=1

        elif mov==self.DOWN:
            if x<len(self.maze)-1 and self.maze[x+1][y]!=1: # dest position != wall
                if self.maze[x+1][y]==self.COIN:    # COIN. adds a coin
                    self.maze[x+1][y]=0
                    ret=2

                elif self.maze[x+1][y]==self.POWER: # POWER. change the game state to FRIGHTENED
                    self.maze[x+1][y]=0
                    self.state=2
                    self.count_state=0
                    ret=1

                    for i in range(self.n_ghosts):
                        if not self.ghosts_house[i]:
                            self.ghosts_dir[i]+=2
                            self.ghosts_dir[i]%=4
                
                
                x+=1

        elif mov==self.LEFT:
            if y>0 and self.maze[x][y-1]!=1:                # dest position != wall
                if self.maze[x][y-1]==self.COIN:    # COIN. adds a coin
                    self.maze[x][y-1]=0
                    ret=2 
                elif self.maze[x][y-1]==self.POWER: # POWER. change the game state to FRIGHTENED
                    self.maze[x][y-1]=0
                    self.state=2
                    self.count_state=0
                    ret=1

                    for i in range(self.n_ghosts):
                        if not self.ghosts_house[i]:
                            self.ghosts_dir[i]+=2
                            self.ghosts_dir[i]%=4               
                
                y-=1
            elif y==0 and self.portal_gates(x):           # "portal"                                                 
                y=self.m-1
                ret=3

        elif mov==self.RIGHT:
            if y<self.m-1 and self.maze[x][y+1]!=1:         # dest position != wall
                if self.maze[x][y+1]==self.COIN:    # COIN. adds a coin
                    self.maze[x][y+1]=0
                    ret=2                
                
                y+=1
            elif y==self.m-1 and self.portal_gates(x):    # "portal"                                             
                y=0
                ret=3
        
        # -------------------------------------------------------------------------------------------------------------------
        # --- EAT/LOSE ------------------------------------------------------------------------------------------------------

        if self.state==2:   # eat.
            eaten=[]
            for i in range(self.n_ghosts):
                if self.ghosts_pos[i][0]==x and self.ghosts_pos[i][1]==y:
                    eaten.append(i)
            
            tmp=1
            for i in eaten:
                ret=4

                # move the eaten ghost to the house cell.
                self.ghosts_pos[i][0]=self.salida_fants[0]+2
                self.ghosts_pos[i][1]=self.salida_fants[1]

                # add to the queue of ghosts in house
                # they leave in 3 ticks intervals
                self.ghost_inHouse.append([i,self.exec_tick+(3*tmp)])
                self.ghosts_house[i]=[self.ghosts_pos[i][0],self.ghosts_pos[i][1]]

                tmp+=1
        else:               # lose.
            for i in range(self.n_ghosts):
                if self.ghosts_pos[i][0]==x and self.ghosts_pos[i][1]==y: 
                    
                    ret=5
                    self.end=True                    
                    

        # if the player hasnt lose, he moves 
        if self.end!=True:            
            self.agent_pos=[x,y]
            self.agent_coins+=(1 if ret==2 else 0)
            
        return ret


    def portal_gates(self, x):
        if self.version==0: return (x==5 or x==9)
        else: return x==4

    """
    Moving the ghosts.
    Also change the game state
           
    :type self: class     
    :rtype: None
    """
    def move_ghosts(self):
        
        # -------------------------------------------------------------------------------------------------------------------
        # --- MOVE ----------------------------------------------------------------------------------------------------------

        for i in range(self.n_ghosts):
            self.move_ghost(i) 
        
        

        # -------------------------------------------------------------------------------------------------------------------
        # --- STATE ---------------------------------------------------------------------------------------------------------

        

        # a ghost leaves the house if is his time
        if len(self.ghost_inHouse)!=0 and self.exec_tick==self.ghost_inHouse[0][1]:
            idx=self.ghost_inHouse.pop(0)[0]
            
            self.ghosts_house[idx]=False

            self.ghosts_pos[idx][0]=self.salida_fants[0]
            self.ghosts_pos[idx][1]=self.salida_fants[1]
        
        # increases the execution ticks
        self.exec_tick+=1
        self.count_state+=1

        
        
        if self.count_state==self.state_ticks[self.state]:                     
            if self.state==0: 
                self.state=1
                print("New state: SCATTER",end="")
            else: 
                self.state=0
                print("New state: CHASE",end="")

            for i in range(self.n_ghosts):
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
            
            

            

            # intersection, moves in the same direction.            
            if self.maze[x+aux_x][y+aux_y]==1 and self.maze[x-aux_x][y-aux_y]==1:
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
                        if k==((dir+2)%4) or self.maze[tmp_x][tmp_y]==1: continue 
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
                        if k==((dir+2)%4) or self.maze[tmp_x][tmp_y]==1: continue 
                        else: tmp=self.distance_cells(target,[tmp_x, tmp_y])
                        
                        if dist>tmp:
                            dist=tmp
                            dir_idx=k
                    
                    self.ghosts_dir[ghost]=dir_idx
                    
                    x+=self.mX[dir_idx]
                    y+=self.mY[dir_idx]
            
            # "portals"
            if y==self.m and self.portal_gates(x): y=0
            if y==-1 and self.portal_gates(x): y=self.m-1
            
            
            
            # collides with the agent
            if self.agent_pos[0]==x and self.agent_pos[1]==y:
                
                # FRIGHTENED. is eaten
                if self.state==2:       

                                    

                    self.ghosts_pos[ghost][0]=self.salida_fants[0]+2
                    self.ghosts_pos[ghost][1]=self.salida_fants[1]

                    self.ghost_inHouse.append([ghost,self.exec_tick+3])
                    self.ghosts_house[ghost]=[self.ghosts_pos[ghost][0],self.ghosts_pos[ghost][1]]
                # OTHERWIESE. eats the player
                else: 
                    self.ghosts_pos[ghost][0]=x
                    self.ghosts_pos[ghost][1]=y
                    
                    self.end=True     
            else:
                self.ghosts_pos[ghost][0]=x
                self.ghosts_pos[ghost][1]=y
                
    
    """
    Calculates the distance of two points given by parameters
           
    :type self: class     
    :type a: int[]
    :type b: int[]
    :rtype: int
    """
    def distance_cells(self, a, b):               
        return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
   

    """
    Printing a matrix giving by parameter.
    
    :type self: class 
    :type matrix: int[][]       
    :rtype: None
    """
    def print_matrix(self, matrix):
        
        n=len(matrix)
        m=len(matrix[0])
        for x in range(n):
            for y in range(m):
                print(matrix[x][y], end=" ")
            print()


    

#FASE 4: ENTRENAR DQN
class Main:
    def signal_handler(self, sig, frame):
        self.timeEnd=MPI.Wtime()

        for i in self.accionesR:
            print(i)


        path=os.path.join("entrenamiento", "model_Neu{}.txt".format(self.version))
        with open(path, "a") as archivo:
            archivo.write(str(self.agent.model.pesos) + "\n\n")        
        path=os.path.join("data", "model_Neu{}.txt".format(self.version))
        with open(path, "w") as archivo:
            archivo.write(str(self.agent.model.pesos))
        
        path=os.path.join("entrenamiento", "target_model_Neu{}.txt".format(self.version))
        with open(path, "a") as archivo:
            archivo.write(str(self.agent.target_model.pesos) + "\n\n")
        path=os.path.join("data", "target_model_Neu{}.txt".format(self.version))
        with open(path, "w") as archivo:
            archivo.write(str(self.agent.target_model.pesos))

        path=os.path.join("entrenamiento", "times{}.txt".format(self.version))
        with open(path, "a") as archivo:
            archivo.write(str(self.timeEnd-self.timeStart) + "\n\n")
        
        print("\nCtrl+C pressed. Variable written to file.")
        sys.exit(0)
    

    
    def train_dqn(self, episodes):
        signal.signal(signal.SIGINT, self.signal_handler)

        env = Pacman(os.path.join("data", "env2_0.txt"))
        input_size = len(env.get_state())
        self.version=env.version

        """posiciones=[[],
                    [[1, 17],[2, 1],[9, 15],[8, 7]],
                    [[3, 19],[3, 4],[11, 19],[12, 7]],
                    [[1, 16],[1, 1],[9, 16],[9, 7]], 
                    [[3, 18],[4, 4],[6, 13],[5, 9]]]

        dirs=[[],
              [3,0,1,2],
              [1,2,1,1],
              [3,0,1,2],
              [1,0,2,3]]

        coins=[0, 8,11,8,5]
        states=[0, 15,21,16,10]"""

        posiciones=[[],
                    [[1, 2]],
                    [[3, 1]],
                    [[2, 1]]]

        dirs=[[],
              [3],
              [2],
              [2]]

        coins=[0, 3,7,5]
        states=[0, 4,7,6]

        

        #agent = DQNAgent(input_size=4, hidden_size=16, output_size=4, learning_rate=0.01, gamma=0.99, epsilon=1.0)
        self.agent = DQNAgent(input_size=input_size, hidden_size=[16], output_size=4, learning_rate=0.01, gamma=0.99, epsilon=0.50,
                            #archivo1=None,archivo2=None)
                            archivo1=os.path.join("data", "model_Neu{}.txt".format(self.version)),
                            archivo2=os.path.join("data", "target_model_Neu{}.txt".format(self.version))) # Usar (None) para que no lea unos pesos ya entrenados
        
        try:      
            for i in range(1,4):      
                env = Pacman(os.path.join("data", "env2_{}.txt".format(i)))                
                
                self.accionesR=[0,0,0,0]
                
                self.timeStart=MPI.Wtime()
                for episode in range(1000):
                    state = env.reset(init=False,positions=posiciones,coins=coins,states=states,dirs=dirs)#positions=None,coins=None,states=None,dirs=None)
                    done = False
                    total_reward = 0
                    print("Empieza: ", episode+1)
                    tStart=MPI.Wtime()
                    while not done:
                        """action = self.agent.choose_action(state)"""
                        action=random.randint(0, 3)  
                        self.accionesR[action]+=1
                        next_state, reward, done = env.step(action)
                        
                        self.agent.remember(state, action, reward, next_state, done)
                        self.agent.replay()
                        
                        state = next_state
                        total_reward += reward
                    tEnd=MPI.Wtime()
                    print("Ha terminado un episodio entrenamiento en: {} \n".format(tEnd-tStart))  
                    self.agent.update_target_model()
                    
                    print(f"Episode {episode + 1}: Total Reward: {total_reward}")
                    env.print_matrix(env.maze)

                    """random.seed(random.randint(1,1000000))"""

                
            
            while(True):
                x=0


        except KeyboardInterrupt:
            # Handle the KeyboardInterrupt exception if needed
            print("\nKeyboardInterrupt caught. Exiting gracefully.")







if __name__ == "__main__":
    main=Main()
    main.train_dqn(500)
    
    #env=PacmanGUI(os.path.join("data", "env2.txt"))
    #env=Pacman(os.path.join("data", "env1_0.txt"))
    
    
    
