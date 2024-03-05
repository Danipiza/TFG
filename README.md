## TFG: Optimización de algoritmos de búsqueda y ordenación utilizando técnicas de cómputo de alto rendimiento
---
#### Estudiante: Daniel Pizarro Gallego (GII)

#### Dirigido por: Alberto Núñez Covarrubias
---
# Índice

1. [MPI](#mpi)
2. [Aprendizaje por Refuerzo](aprendizaje-por-refuerzo)
3. [Programación Evolutiva](programación-evolutiva)
4. [Aprendizaje no Supervisado](aprendizaje-no-supervisado)
5. [Redes Neuronales](#redes-neuronales)

---
  

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

Mejorar un problema de aprendizaje por refuerzo con workers/hilos se puede lograr con varias estrategias. El contexto del problema es muy importante.

- __Distribución de Tareas__: Distribuir el trabajo en paralelo. EJ: Entrenando un agente en un entorno complejo, se puede dividir el proceso de entrenamiento en varios workers/hilos, cada uno responsable de explorar una parte del espacio de acciones o de estados.

- __Varias Exploraciones__: Cada worker/hilo realiza una exploración independiente y luego comparta sus experiencias con los demás hilos, de manera que el agente pueda aprender de varias experiencias simultaneas.
  
- __Explotación y evaluación simultáneas__: Además de explorar el entorno, puedes utilizar hilos para realizar simultáneamente la explotación (es decir, tomar decisiones basadas en el conocimiento actual del agente) y la evaluación (es decir, medir el desempeño del agente en el entorno). Esto puede acelerar el proceso de aprendizaje al permitir que el agente ajuste su estrategia más rápidamente.

- __Optimización de Hiperparámetros__: alpha, beta y gamma son los hiperparámetros que se usan para almacenar las experiencias del agente. Con vairos workers/hilos con diferentes hiperparámetros así comprobando de forma paralela cual sería la mejor configuracion. EJ, con técnicas como la __búsqueda aleatoria__ u __optimización bayesiana distribuida__ para encontrar la mejor configuración de hiperparámetros para el modelo de aprendizaje por refuerzo.

- __Implementación Eficiente de Algoritmos__: Hay algoritmos de aprendizaje por refuerzo, que se pueden paralelizar manera eficiente.

 [__A3C (Asynchronous Advantage Actor-Critic)__](https://www.activeloop.ai/resources/glossary/asynchronous-advantage-actor-critic-a-3-c/#:~:text=A3C%2C%20or%20Asynchronous%20Advantage%20Actor,form%20of%20rewards%20or%20penalties.)  visto en la asignatura IA1, básicamente el agente recibe un feedback de la operación que ha ejecutado, dando recompensas (si es negativa es una penalización).
 
 [__PPO (Proximal Policy Optimization)__](https://openai.com/research/openai-baselines-ppo)

---

## Programación Evolutiva

Los algoritmos genéticos son una herramienta dentro del campo de la inteligencia artificial que imita los procesos de selección natural y evolución para encontrar soluciones óptimas a problemas complejos.

__Plantilla básica de una Algoritmo Evolutivo__
``` 
poblacion = iniciar_poblacion(tam_poblacion);
evaluar_poblacion(poblacion);
while(<<condición>>){
  seleccion = seleccionar_poblacion();
  // Reproducción
  cruzar_poblacion(seleccion, prob_cruce);
  mutar_poblacion(seleccion, prob_muta);
  // Elegir que individuos pasan a la siguiente generacion
  eleccion_poblacion(poblacion, seleccionados);
  evaluar_poblacion();
}
```

- Inicializar Población:
Para inicializar la población, se pasa por parámetro el tamaño de la poblacion, y se inicializan todos los Individuos.

Los Individuos suelen ser un array de bits, por lo que se recorre el individuo, es decir, el cromosoma y con un numero random se genera cada alelo del cromosoma.

Cada individuo puede tener muchos bits, debido a un tamaño de cromosoma elevado. Si tenemos muchos individuos y el tamaño del cromosoma es muy grande se puede distribuir la carga
de trabajo entre varios workers/hilos para que generen una parte y envien al master lo generado.

- Evaluar Población:
Para evaluar la población, se reciben los individuos de la población y se calcula su fitness, como de buenos son estos individuos para el problema a resolver.

La funcion de aptitud calcula el fitness, recibiendo el array de bits de un individuo. 

Dependiendo del problema, puede ser un calculo rápido con el fenotipo asociado al individuo, o un cálculo que requiera recorrer todo el array de bits. Se puede distribuir la carga de trabajo entre varios workers/hilos para calcular el fitness de una parte de la población. (Como a la hora de inicializar)

- Seleccionar Población:
Para seleccionar la poblacion, hay varios métodos, ruleta, torneo, estocástico universal...

Se recibe el fitness de la población y el método se encarga de elegir individuos, puede elegir a los mejores o elegir de manera justa.

Por ejemplo en el método de ruleta se selecciona un número de individuos de la población de manera aleatoria, pero teniendo en cuenta su adaptabilidad, por lo que los mejores individuos tienen más probabilidades de ser escogidos. Se puede realizar un distribucion para que varios workers/hilos seleccionen una parte de la población.

- Cruzar Población:
Una vez seleccionados los individuos de la población, con una probabilidad de cruce que se pasa por parámetro se seleccionan 2 individuos aleatorios y se cruzan dependiendo de la probabilidad, si no se quedan como están.

Hay varios métodos para el cruce, unos mas simples y otros más complejos. Por ello se puede gestionar este proceso con workers/hilos que reciban una parte de los individuos seleccionados y devuelvan esa parte una vez realizada el cruce.

- Mutar Población:
Cuando ya se han cruzado los elementos seleccionados estos pasan a una etapa de mutación, en la cual con una probabilidad de mutación, se recorre los alelos de los individuos seleccionados y cruzados para aplicar diversidad.

Al igual que con el cruce hay varios métodos, simples y complejos, que se pueden paralelizar con workers/hilos. 


---

## Aprendizaje no Supervisado




---

## Redes Neuronales
