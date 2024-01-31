## TFG: Optimización de algoritmos de búsqueda y ordenación utilizando técnicas de cómputo de alto rendimiento
---
#### Estudiante: Daniel Pizarro Gallego (GII)

#### Dirigido por: Alberto Núñez Covarrubias
---

# TODO

## Reducir el tiempo de ejecución
- No usar recursión
- No acceder mucho a memoria, tambien accesos secuenciales, mejora la eficiencia debido al rendimiento del caché. 
- Paralelismo
- Bibliotecas estándar

# Mejoras

---
## Búsquedas
---

## [Busq. Lineal](https://www.geeksforgeeks.org/linear-search/)
Es la búsqueda más sencilla y simple, recorre todos los elementos de un array buscando un elemento, si no encuentra el valor en la posicion i-esima, avanza a la siguiente posicion, así hasta encontrar el valor o recorrer todo el array.
### Costes
#### Temporal: O(n), en el caso peor recorre todo el array.
#### Espacial. O(1), solo se necesita un puntero para recorrer el array.
---
### Mejoras

### Division del Espacio de Búsqueda
Cada hilo realiza una búsqueda lineal, asignando un espacio de busqueda a cada hilo, para reducir el tiempo de ejecución.
Se puede reducir el tiempo de ejecucion de lineal a logaritmico, produciendo, potencias de 2, hilos.

### Manejo de Sincronización
Utilizando mecanismos de sincronización, como cerrojos, semáforos o monitores. Asi reduciendo el tiempo de cómputo de los hilos y terminar su ejecución cuando 1 hilo encuentre el parámetro buscado. Evitando problemas de concurrencia, y asegurando accesos seguros a los datos compartidos, en este caso a una posible variable booleana "encontrado".

### Manejo de Interrupciones y Cancelaciones
Mecanismos que manejan interrupciones y cancelaciones de la búsqueda.

### Cálculo ideal del Número de Hilos
Crear y gestionar demasiados hilos pueden generar un costo adicional, tanto en espacio como en tiempo.

### Uso de Bibliotecas Específicas para la Concurrencia
Algunos lenguajes de programación ofrecen bibliotecas específicas para operaciones concurrentes y paralelas. (facilita la implementación)

---
---

## Busq. Binaria (Binary Search)
Búsqueda que implementa un algoritmo de divide y vencerás. Divide el espacio de busqueda a la mitad con cada iteracion del bucle. El array tiene que estar ordenado puesto que haciendo la comparacion con el valor medio del espacio de búsqueda, se queda con el espacio donde podría estar el valor deseado.
### Costes
#### Temporal: O(log n), en el caso peor hace logaritmo en base 2 de n comparaciones, es cuando no está en el array o encuentra el valor cuando el espacio de búsqueda solo tiene ese elemento.
#### Espacial. O(1), solo se necesitan dos punteros para recorrer el array, inicio, fin de la búsqueda y m, para la posicion del medio de la búsqueda.
---
### Mejoras

### Uso de optimizaciones específicas de cada lenguaje
Las características específicas de cada lenguaje de programación, ayuda a reducir el tiempo de cómputo. Ej. C++; funciones de la biblioteca estándar como std::lower_bound.

### Evitar el uso de recursión: 
Las llamadas recursivas introducen sobrecarga. Una implementación iterativa casi siempre suele ser más eficiente.

### Uso de paralelismo: 
Puede ser interesante reducir el tiempo de ejecucion añadiendo hilos que procesan partes del espacio de búsqueda, en el caso de que una parte no contenga el valor buscado, no se continua con el procesado de este hilo. Crear varios hilos y antes de comenzar la busqueda binaria preguntar al primer y último valor del espacio para saber si es posible que se encuentre el valor buscado, si no se encuentra finaliza ese hilo. En muchos casos este implementación puede no ser beneficiosa, si gestionar esta concurrencia ralentiza el procesamiento. 

### Cálculo ideal del Número de Hilos
Crear y gestionar demasiados hilos pueden generar un costo adicional, tanto en espacio como en tiempo.






