## TFG: Optimización de algoritmos de búsqueda y ordenación utilizando técnicas de cómputo de alto rendimiento
---
#### Estudiante: Daniel Pizarro Gallego (GII)

#### Dirigido por: Alberto Núñez Covarrubias
---
# Índice

1. [Algoritmos Básicos](#algoritmos-básicos)
2. [MPI](#mpi)
3. [Aprendizaje por Refuerzo](aprendizaje-por-refuerzo)
4. [Programación Evolutiva](programación-evolutiva)
5. [Aprendizaje no Supervisado](aprendizaje-no-supervisado)
6. [Redes Neuronales](#redes-neuronales)

---
  
## Algoritmos Básicos

### Búsquedas

#### Busq. Lineal (Sequential Search)
(Array) Es la búsqueda más sencilla y simple, recorre todos los elementos de un array buscando un elemento, si no encuentra el valor en la posicion i-esima, avanza a la siguiente posición.

__Costes__
``` 
Temporal: O(n), en el caso peor recorre todo el array.
Espacial. O(1), solo se necesita un puntero para recorrer el array.
```

#### Busq. Binaria (Binary Search)
(Array) Búsqueda que implementa un algoritmo de divide y vencerás. El array tiene que estar ordenado, así divide el espacio de busqueda a la mitad con cada iteracion del bucle.

__Costes__
```
Temporal: O(log n), en el caso peor hace logaritmo en base 2 de n comparaciones.
Espacial. O(1), solo se necesitan dos punteros para recorrer el array.
```

#### Busq. en Anchura (BFS)
(Grafo) Búsqueda que se implementa con una cola. Se parte de un vértice y se expande por niveles.
__Costes__
```
Temporal: O(V+A), en el caso peor recorre todos los vertices y las aristas del grafo.
Espacial. O(V), en el caso peor almacena todos los vertices en la cola.
```

#### Busq. en Profundidad (DFS)
(Grafo) Búsqueda que implementa un algoritmo de vuelta atrás. Se puede usar una pila para que no sea recursivo. Se parte de un vértice y se expande hasta que no pueda más, y vuelve atrás.

__Costes__
```
Temporal: O(V+A), en el caso peor recorre todos los vertices y las aristas del grafo.
Espacial. O(V), en el caso peor almacena todos los vertices en la cola.
```

#### Busq. por Dijkstra 


__Costes__
```
Temporal: 
Espacial.
```

#### Busq. por Floyd 
Búsqueda que implementa 

__Costes__
```
Temporal: O(V^3)
Espacial. 
```

---

### Ordenaciones

#### BubbleSort
Búsqueda que implementa 

__Costes__
```
Temporal: O(V^3)
Espacial. 
```
#### InsertionSort
Búsqueda que implementa 

__Costes__
```
Temporal: O(V^3)
Espacial. 
```
#### MergeSort
Búsqueda que implementa 

__Costes__
```
Temporal: O(V^3)
Espacial. 
```
#### QuickSort
Búsqueda que implementa 

__Costes__
```
Temporal: O(V^3)
Espacial. 
```

#### SelectionSort
Búsqueda que implementa 

__Costes__
```
Temporal: O(V^3)
Espacial. 
```

### Mejoras



## Reducir el tiempo de ejecución
- No usar recursión
- No acceder mucho a memoria, tambien accesos secuenciales, mejora la eficiencia debido al rendimiento del caché. 
- Paralelismo
- Bibliotecas estándar

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


## Ordenaciones


## MPI
MPI es un estándar para una biblioteca de paso de mensajes. El objetivo es comunicar procesos en ordenadores remotos.

Actualmente hay varias implementaciones: [Open MPI](http://www.open-mpi.org/), [MPICH](http://www.mpich.org/) , [MVAPICH](http://mvapich.cse.ohio-state.edu/), [IBM Platform MPI](http://www.ibm.com/systems/es/platformcomputing/products/mpi/), [Intel MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html)

MPI 2.0 tiene más de 100 funciones. Se intercambia información usando paso de mensajes.

### La Ley de Amdahl (1967)
```
Acceleración = 1/((1-p) + p/n)
```
### Memoria Compartida
Lecturas en paralelo, escrituras con exclusión mutua (Mutex). **1 Nodo, n procesos.**
### Memoria Distribuida
Un proceso sólo tiene acceso a su espacio de memoria. El proceso **X le envía al proceso Y datos**. **n Nodos, n procesos.**

Taxonomía de Flynn
- SISD (Single Instruction, Single Data stream) 
- SIMD (Single Instruction, Multiple Data streams) 
- MISD (Multiple Instruction, Single Data stream), Poco común 
- MIMD (Multiple Instruction, Multiple Data streams)

## Single Program Multiple Data (SPMD) 
**1 programa** ejecutado en paralelo. El mismo programa se **copia a todos los nodos**. Cada proceso tiene su propio su ID (Rank) 

![MPI](https://github.com/Danipiza/TFG/assets/98972125/9725df3b-60ba-4d4d-9726-0f5087f5c37b)

---

## Funciones 
### Funciones de Entorno
**MPI_COMM_WORLD** agrupa los procesos en “comunicadores”. Los procesos que intercambian mensajes comparten comunicador 


**MPI_Init**. Establece un entorno de MPI, solo se invoca una vez por proceso.

```int MPI_Init(int *argc, char *argv[])```

**MPI_Finalize**. Termina el procesamiento de MPI. Tiene que ser la ultima llamada MPI.

```int MPI_Finalize(void);```

**MPI_Comm_size**. Devuelve el número de procesos relacionados con el comunicador

```int MPI_Comm_size(MPI_Comm comm, int* size); comm: comunicador (entrada), size: número de procesos en este comunicador (salida)```

**MPI_Comm_rank**. Devuelve el ID (rank) del proceso asociado a un comunicador [0,(size-1)]

```int MPI_Comm_rank(MPI_Comm comm, int* rank); comm: comunicador (entrada), rank: rank del proceso llamante en el comunicador (salida)```

**MPI_Abort**. Fuerza la finalización de todos los procesos MPI

```int MPI_Abort(MPI_Comm comm, int errorcode);```

### Esquema de programas MPI
```
#include <stdio.h>
#include “mpi.h”
...

int main(int argc, char *argv[]){ 
 MPI_Init(&argc, &argv);
 MPI_Comm_rank(MPI_COMM_WORLD,&myrank); 
 MPI_Comm_size(MPI_COMM_WORLD, &size);

 // Logica del programa...

 MPI_Finalize();
}
```
---

### Funciones Punto a Punto
Proceso **emisor y receptor** del mensaje

**SÍNCRONA**: El proceso **emisor espera** a que se realice el envío del mensaje. Comunicación **bloqueante**

**MPI_Send**. Envía un mensaje de forma síncrona. Mensaje lo puede recibir un proceso mediante MPI_Recv o MPI_IRecv

```int MPI_Send(void* buf, int count, MPI_Datatype datatype, int destination, int tag, MPI_Comm comm );```
- buf: puntero a los datos que se envían (mensaje)
- count: número de elementos en el mensaje
- datatype: tipo de los datos enviados
- destination: rank del proceso al que se le envía el mensaje
- tag: etiqueta que puede servir de ID único del mensaje (en particular, para ligar envío y recepción)
- comm: comunicador


**MPI_Recv**. Recibe un mensaje de forma síncrona

```int MPI_Recv(void* buf /*out*/, int count, MPI_Datatype datatype, int source, int tag, MPI_Comm comm, MPI_Status *status /*out*/);```
- buf: puntero donde se van a almacenar los datos recibidos (mensaje)
- count: maximum número de elementos en el mensaje
- datatype: tipo de los datos enviados
- source: rank del proceso del que se espera recibir el mensaje
- MPI_ANY_SOURCE indica que se puede recibir un mensaje de cualquier proceso
- tag: etiqueta que puede servir de ID único del mensaje (en particular, para ligar envío y recepción)
- comm: Comunicador
- MPI_Status: contiene source y tag (puede haber usado MPI_ANY_SOURCE y MPI_ANY_TAG) y el count (el parámetro solo contiene el máximo posible) y, posiblemente otras informaciones)


**MPI_Get_count**. Para saber cuantos bytes se reciben
```MPI_Get_count( MPI_Status* status, MPI_Datatype datatype, int* count)```

**ASÍNCRONA**: El proceso emisor envía el mensaje y **continúa su ejecución** sin asegurarse de que el proceso receptor haya solicitado el mensaje. Comunicación **no bloqueante**

**MPI_ISend**. Envía un mensaje de forma asíncrona. Mensaje lo puede recibir un proceso mediante MPI_Recv o MPI_IRecv

```int MPI_ISend(void* buf, int count, MPI_Datatype datatype, int destination, int tag, MPI_Comm comm, MPI_Request *request /*out*/ );```
- MPI_Request: Identificador que se puede usar posteriormente para saber si la recepción ha terminado
**MPI_Test():** Devuelve un flag que indica si la operación se ha completado

**MPI_Wait():** Devuelve el control de la ejecución si la operación se ha completado, espera 
a que finalice en caso contrario

**MPI_IRecv**. Recibe un mensaje de forma asíncrona
```int MPI_IRecv(void* buf, int count, MPI_Datatype datatype, int destination, int tag, MPI_Comm comm, MPI_Request *request /*out*/ );```

  
### Ejemplo
```
#include “mpi.h”
int rank, nproc;

int main (int argc, char* argv[] ) { 
  int isbuf, irbuf; 
  MPI_Status status;

  MPI_Init( &argc, &argv ); 
  MPI_Comm_size( MPI_COMM_WORLD, &nproc); 
  MPI_Comm_rank( MPI_COMM_WORLD, &rank);
  
  if (rank == 0){ 
    isbuf = 9;
    MPI_Send(&isbuf, 1, MPI_INTEGER, 1, 1, MPI_COMM_WORLD);
  } 
  else if(rank == 1) {
    MPI_Recv( &irbuf, 1, MPI_INTEGER, 0, 1, MPI_COMM_WORLD, &status);
    printf( “%d\n”, irbuf );
  }

  MPI_Finalize();
}
```
![Master_Worker](https://github.com/Danipiza/TFG/assets/98972125/bb3bb7ab-b896-4638-a83b-ec256823baf5)

---

## Aprendizaje por Refuerzo

## Programación Evolutiva

## Aprendizaje no Supervisado




---

## Redes Neuronales
