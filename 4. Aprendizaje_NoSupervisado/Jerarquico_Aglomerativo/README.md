# Jerárquico Aglomerativo

El objetivo es dividir los N o individuos en un número de clusters *k* (valor de entrada del algoritmo). Lo que hace este algoritmo es dividir nuestro espacio de representación d-dimensional en k regiones, siendo *d* las variables consideradas.


## Índice


1. [Algoritmo](#algoritmo)
2. [Mejoras (+ MPI)](Mejoras-(+-MPI))
3. [TODO](todo)




## Algoritmo


```
FASE 1: Crear la matriz de distancias inicial D 
  Es una matriz simétrica (basta con usar una de las matrices triangulares) - 
FASE 2: Agrupación de Individuos 
    - Partición inicial P0: Cada objeto es un cluster 
    - Calcular la partición siguiente usando la matriz de distancias D
        • Elegir los dos clusters más cercanos. Serán la fila y la columna del mínimo de la matriz D 
        • Agrupar los dos en un cluster. Eliminar de la matriz la fila y columna de los clusters agrupados.
        • Generar la nueva matriz de distancias D. 
            o Añadir una fila y una columna con el cluster nuevo 
	    o Calcular la distancia del resto de clusters al cluster nuevo 
    - Repetir paso 2 hasta tener sólo un cluster con todos los individuos
	• Representar el dendograma (árbol de clasificación) 
```



### Complejidad
- Complejidad Temporal: La complejidad con los enlaces simple y completo tienen un coste cúbico O(n^3). Existen implementaciones más eficientes (n^2).
- Complejidad Espacial: O(N^2+N) = **O(N\^2)** Matriz con las distancias de cada cluster que se va reduciendo con las iteraciones. Para centroides se necesita un array con los centroides N y para simple y completo se necesita un array con los individuos, para comprobar la distancia más cercana o lejana.


---



## Mejoras (+ MPI)

### Cada Worker se encarga de unas filas

#### Inicialización
El Master asigna a cada Worker unas filas para gestionar. Como la matriz de distancias D es un triángulo superior si asignamos filas por orden habrá un Worker con muchas distancias y otro con muy pocas, por eso se asigna la primera fila sin asignar superior con la primera inferior, para que así todos los workers tengan el mismo número de distancias que gestionar.

#### Algoritmo
Cada Worker se encarga de sus filas asignadas por lo que se reduce el tiempo de buscar el mínimo en la matriz de distancias *D*. También se reduce el tiempo de recalcular las nuevas distancias al cluster actualizado de la pareja con distancia mínima, ya que se dividen entre los Workers el cálculo.

#### Complejidad
- Complejidad Temporal: La complejidad con los enlaces simple y completo tienen un coste cúbico O(n^3). Existen implementaciones más eficientes (n^2).
- Complejidad Espacial: O(N^2+N) = **O(N\^2)** Matriz con las distancias de cada cluster que se va reduciendo con las iteraciones. Para centroides se necesita un array con los centroides N y para simple y completo se necesita un array con los individuos, para comprobar la distancia más cercana o lejana.



---


## TODO

### REVISAR, REFINAR Y TERMINAR Simple y Completo

### COMPLEJIDAD?

### SPEEDUP

# COMPROBAR TODO
