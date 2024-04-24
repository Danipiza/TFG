"""import random

ind1=[1,2,3,5,6,4]
ind2=[4,3,2,1,5,6]

print(ind1)

aviones=6

corte1 = 2
corte2 = 4
set1={""}
set2={""}

# Se añaden los elementos del padre opuesto
for j in range(corte1,corte2):                
    set1.add(ind2[j])
    set2.add(ind1[j])

# Hijo 1
# Si no esta en el set se deja, 
# Si esta es porque esta en el intervalo del otro padre y se pasa al siguiente elemento

k=corte2
j=corte2
cont=j
while j%aviones!=corte1:
    if ind1[cont] not in set1:
        ind1[j]=ind1[cont]
        j=(j+1)%aviones
    
    cont=(cont+1)%aviones

for j in range(corte1,corte2):                
    temp=ind1[j]
    ind1[j]=ind2[j]
    ind2[j]=temp

print(ind1)"""


"""
precision=0.01
print(precision)
precision/=10
print(precision)
"""
i=1
while True:
    print(i)
    i+=1