## TFG: Optimización de algoritmos de búsqueda y ordenación utilizando técnicas de cómputo de alto rendimiento
---
#### Estudiante: Daniel Pizarro Gallego (GII)

#### Dirigido por: Alberto Núñez Covarrubias
---

# TODO

# Mejoras

---
## Búsquedas
---

## Busq. Lineal (Sequential Search)
### Division del Espacio de Búsqueda:
Cada hilo realiza una búsqueda lineal, asignando un espacio de busqueda a cada hilo, para reducir el tiempo de ejecución.
Se puede reducir el tiempo de ejecucion de lineal a logaritmico, produciendo, potencias de 2, hilos.

### Manejo de Sincronización:
Utilizando mecanismos de sincronización, como cerrojos, semáforos o monitores. Asi reduciendo el tiempo de cómputo de los hilos y terminar su ejecución cuando 1 hilo encuentre el parámetro buscado. Evitando problemas de concurrencia, y asegurando accesos seguros a los datos compartidos, en este caso a una posible variable booleana "encontrado".

### Manejo de Interrupciones y Cancelaciones:
Mecanismos que manejan interrupciones y cancelaciones de la búsqueda.

### Cálculo ideal del Número de Hilos:
Crear y gestionar demasiados hilos pueden generar un costo adicional, tanto en espacio como en tiempo.

### Uso de Bibliotecas Específicas para la Concurrencia:
Algunos lenguajes de programación ofrecen bibliotecas específicas para operaciones concurrentes y paralelas. (facilita la implementación)

---

## Busq. Binaria (Binary Search)





