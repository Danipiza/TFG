"""import random

a=[False, [0,0]]


if not a[0]: print(0)

if a[1]: print(1)


print("numero aleatorio:", random.randint(0,1))"""

"""matrix=[[i+(5*j) for i in range(1,6)] for j in range(5)]

for x, fila in enumerate(matrix):   
    for y, celda in enumerate(fila):
        print("x={}, y={}\tval={}".format(x,y,celda))"""


"""print("Tick={}  \tState={}  \tCoins={}  \t{}".format(1000000, 1000, 100, "COIN"))
print("Tick={}  \tState={}  \tCoins={}  \t{}".format(100, 10, 10, "COIN"))"""

import random

class DQN:
    def choose_action(epsilon=1.0):
        if random.uniform(0,1)<1.0:
            return random.randint(0, 3)  
        else:
            return 0

class Main:

    def main():
        dqn=DQN()
        acciones=[0,0,0,0]


        for i in range(10000):
            #acciones[random.randint(0, 3)]+=1
            acciones[dqn.choose_action()]+=1

        for i in acciones:
            print(i)
    
main=Main

main.main()