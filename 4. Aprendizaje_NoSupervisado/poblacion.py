import random

def generar_matriz(d, N, min_valor, max_valor):
    poblacion = []
    for i in range(N):
        ind=[]
        for j in range(d):
            ind.append(random.uniform(min_valor, max_valor))
        poblacion.append(ind)
    return poblacion


d = 3  # Numero de dimensiones
N = 5  # tam_poblacion
min_valor = 0  # valor mínimo 
max_valor = 10  # valor máximo 

poblacion_generada = generar_matriz(d, N, min_valor, max_valor)
print("Matriz generada:")
for ind in poblacion_generada:
    print(ind)
