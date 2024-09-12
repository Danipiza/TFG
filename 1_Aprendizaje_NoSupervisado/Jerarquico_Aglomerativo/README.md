# Jerárquico Aglomerativo

El objetivo es dividir los N o individuos en un número de clusters *k* (valor de entrada del algoritmo). Lo que hace este algoritmo es dividir nuestro espacio de representación d-dimensional en k regiones, siendo *d* las variables consideradas.


## Índice


1. [Algoritmo](#algoritmo)
2. [Mejoras (+ MPI)](#estrategias-mpi)
3. [Implementaciones](#implementaciones)




## Algoritmo


<a href="https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative.py">
    <img src="https://github.com/Danipiza/TFG/tree/main/.Otros/Imagenes/Algorithm_JA.webp">
</a>

### Complejidad
- Complejidad Temporal: **O(N\^3)**

En cada iteteración, recorre toda la matriz para comprobar la menor distancia y así agrupar los clusters que representan la fila y columna de la celda con menor tamaño.

- Complejidad Espacial: O(N^2+N) = **O(N\^2)** 

Matriz con las distancias de cada cluster que se va reduciendo con las iteraciones. Para centroides se necesita un array con los centroides N y para simple y completo se necesita un array con los individuos, para comprobar la distancia más cercana o lejana.


---



## Estrategias MPI

### Dividir la matriz entre los procesos

#### Inicialización
El _master_ asigna a cada _worker_ unas filas para gestionar. Como la matriz de distancias D es un triángulo superior si asignamos filas por orden habrá un _worker_ con muchas distancias y otro con muy pocas. Por este motivo se asigna la primera fila sin asignar superior con la primera inferior, para que así todos los _worker_ tengan el mismo número de distancias que gestionar.

#### Algoritmo

1. El _master_ pide a los _workers_ la celda con menor valor (menor distancia entre los clusters _i_ y _j_, siendo estos la fila y columna).
2. El _master_, con los valores recibidos, pide la fila (_i_) y la columna (_j_) del _worker_ con menor distancia. Con estos datos, el _master_ envía a todos los procesos estos índices, así como los _ids_ de los _workers_ que tienen que eliminar o actualizar la fila con mayor o menor índice respectivamente.
3. Todos los _workers_ eliminan la columna con mayor índice. El _worker_ que tiene que eliminar la fila la elimina. Mientras que el que tiene que actualizar la actualiza, con o sin ayuda de los demás _workers_.

## Implementaciones
[Código](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative.py). Algoritmo Secuencial

- Estrategia sin dividir el cálculo de la fila a actualizar.

[Código](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Cent_E.py). Distancia entre Cluster por centroide. Distancia Euclidea entre individuos.

[Código](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Cent_M.py). Distancia entre Cluster por centroide. Distancia Manhattan entre individuos.

- Distancia entre Cluster por centroide. Distancia Manhattan entre individuos. 
- a
- a
- a
<a href="https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative.py">
    <img src="https://github.com/Danipiza/TFG/tree/main/.Otros/Imagenes/Algorithm_JA.webp">
</a>


