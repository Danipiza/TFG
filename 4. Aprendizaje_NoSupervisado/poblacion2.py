import random
import matplotlib.pyplot as plt

def generate_clustered_matrix(dimensiones, N, min_valor, max_valor):
    puntos_por_cluster = N // 5
    puntos = []
    centroides = []
    for _ in range(5):
        centroide = [random.uniform(min_valor, max_valor) for _ in range(dimensiones)]
        centroides.append(centroide)
    
    for centroide in centroides:
        for _ in range(puntos_por_cluster):
            punto = []
            for i in range(dimensiones):
                punto.append(random.uniform(centroide[i] - 0.1*(max_valor - min_valor), centroide[i] + 0.1*(max_valor - min_valor)))
            puntos.append(punto)
    
    puntos_faltantes = N - len(puntos)
    for _ in range(puntos_faltantes):
        punto = [random.uniform(min_valor, max_valor) for _ in range(dimensiones)]
        puntos.append(punto)
    
    return puntos

# Generar la matriz de puntos
d = 2
N = 500
min_valor = 0
max_valor = 10
matriz_clusterizada = generate_clustered_matrix(d, N, min_valor, max_valor)

# Extraer las coordenadas de x e y de los puntos para graficar
x = [p[0] for p in matriz_clusterizada]
y = [p[1] for p in matriz_clusterizada]

# Graficar los puntos
plt.scatter(x, y, color='b', marker='.')
plt.title('España')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
