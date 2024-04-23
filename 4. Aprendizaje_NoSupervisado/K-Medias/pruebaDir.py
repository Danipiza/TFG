import os
import sys


dir=os.getcwd()
n=len(dir)

while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
    dir=os.path.dirname(dir)
    n=len(dir)

path=os.path.join(dir, ".Otros","ficheros","Cluster")
archivos = os.listdir(path)   

for x in archivos:
    print(x)