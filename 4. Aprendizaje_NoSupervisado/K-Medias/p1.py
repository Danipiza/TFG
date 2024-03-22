import sys
import os

#dir=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))
dir=os.getcwd()
n=len(dir)

while(dir[n-3]!='T' and dir[n-2]!='F' and dir[n-1]!='G'):
    dir=os.path.dirname(dir)
    n=len(dir)

print(dir)

