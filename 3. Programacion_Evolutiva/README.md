# Programación genética

---

## Mejoras (+MPI)

### Dividir cada funcion entre los workers

### Cada Worker se encarga de unas generaciones (No mejora rendimiento, mejora la eficacia)

### Pipe-Lining = Segmentacion Computadores

### Enviar mensajes entre procesos

Master inicializa y evalua

worker1 -> seleccionar

worker2 -> cruzar

worker3 -> mutar

worker4 -> evaluar


Worker1 -> Worker2 -> Worker3 -> Worker4



## Guia de Uso
El proyecto se ejecuta en la clase Main. Aparece la interfaz y se rellenan los datos. 
- Prob. Cruce y Prob. Mutación: son “double”, con un intervalo de [0, 1]
- Precisión es un “double” y se tiene que introducir de la forma 0.1, 0.01, 0.001…
- Elitismo es un porcentaje, por lo que es un intervalo de [0, 100]


## Arquitectura
__Main__ es la clase principal que llama a la clase __MainWindow__ la cual ejecuta la interfaz.
En esta interfaz se rellenan las variables y se ejecuta con el botón _Ejecuta_. En esta misma clase se inicializa __AlgoritmoGenetico__, clase en la cual está el bucle principal del programa y llama a todas las funciones.

- El método _InicializaPoblacion_ se desarrolla en mediante la clase __Individuo__, que genera aleatoriamente la poblacion.
Los siguientes métodos se eligen en la interfaz.
- El método _evaluaPoblacion_ se implementa mediante clases abstractas y herencia. Se ejecutan en la clase __Funcion__, cada una con su función de fitness.
- El método _seleccionaPoblacion_, se ejecuta con la clase __Seleccion__.
- El método _cruzaPoblacion_, se ejecuta con la clase __Cruce__.
- El método _mutaPoblacion_, se ejecuta con la clase __Mutacion__.


---

## Ejemplo
- Tamaño de poblacion: 10000
- Número de genes: 2
- Tamaño de gen: 1000
- Generaciones: 100

### Funciones
- Inicialización
- 100x ->
- Evaluación f(x1 , x2) = x1^2 + 2x^2
- Cruce monopunto (punto aleatorio)
- Mutacion  básica

![tiempo_geneticaEJ1](https://github.com/Danipiza/TFG/assets/98972125/4a44ddf2-259a-4eca-9ec0-a427696bb993)
