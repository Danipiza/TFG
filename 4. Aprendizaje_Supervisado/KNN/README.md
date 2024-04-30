# K-Nearest Neighbours (KNN)


## MPI 1: DIVIDE LA POBLACION INICIAL

ERROR, COMO SE DIVIDE LA POBLACION INICIAL, NO SE PUEDE PONER K=100 VECINOS CON MAS DE 10 WORKERS PORQUE, ASI CADA WORKER TIENE MENOS POBLACION INICIAL QUE LOS 100 VECINOS MAS CERCANOS Y DA FALLO DE COLA DE PRIORIDAD




Se trata de una técnica aplicable en problemas de regresión y de clasificación

Es simple pero potente. Se basa en la idea de que **los puntos de datos similares tienden a agruparse en el espacio de características**.
1. Empezar con una población inicial con categorías conocidas.
2. Añadir un nuevo individuo con categoría desconocida.
3. Clasificar el individuo con los k vecinos más cercanos.

Pertenece al **paradigma de aprendizaje perezoso** o basado en **instancias**:
- Perezoso: No calcula ningún modelo y demora todos los cálculos hasta el momento en que se le presenta un ejemplo nuevo
- Basado en instancias: Usa todos los individuos disponibles y ante un ejemplo nuevo recupera los más relevantes para componer la solución

Se puede aplicar a mapas de calor

## Índice

1. [Algoritmo](#algoritmo-para-predecir)
2. [Determinar K optima](determinar-k-optima)
3. [Mejoras (+ MPI)](Mejoras-(+-MPI))
4. [TODO](todo)

--- 

## Algoritmo para predecir
Damos un valor para k, el número de vecinos más cercanos.

Para cada individuo a predecir se recorre toda la población categorizada y se calcula la distancia con estos. Se escogen los k más cercanos y se asigna al valor a predecir la categoría con mayor repeticiones. Conforme avanza el algoritmo se actualiza la población con los nuevos valores.

### Complejidad
- Complejidad Temporal: O(M*N) = **O(n^2)** se ejecutan M veces (población a predecir) y se recorre todo N (población categorizada), N crece de manera uniforme conforme se recorre la población a predecir.
- Complejidad Espacial: O(N\*d + M\*d + N) = **O(n\*d)** guardamos los puntos en el espacio de la población categorizada (N) y población a predecir (M). _d_ es el número de dimensiones.

### Distancias 
- Manhattan: Suma de las diferencias en valor absoluto de todas las dimensiones del individuo.
- Euclídea: Raíz cuadrada de la suma de las diferencias al cuadrado de todas las dimensiones del individuo.
- Chebyshov: Máxima diferencia en valor absoluto de todas las dimensiones del individuo.
  

## Determinar K Óptima

No hay una forma de determinar el **mejor valor para k**, por lo que hay que probar con varias ejecuciones. valores pequeños de k crea sonido. Valores grandes con pocos datos hará que siempre sea la misma categoría
- Si es muy pequeño, corre el riesgo de sobre aprender (aprender conocimiento espúreo)
- Si es muy grande, corre el riesgo de generalizar demasiado

### Validación cruzada
1. Los datos se dividen aleatoriamente en k subconjuntos iguales 
2. Se entrena el conjunto con (k-1) y se valida con el restante 
3. Se repite k veces el paso 2, cambiando el conjunto que se usa para validar 
4. Como medida de error final se suele presentar la media de las k medidas de error de validación (aunque puede ser interesante comprobar que las k medidas sean similares)

![Validacion_Cruzada](https://github.com/Danipiza/TFG/assets/98972125/65c653df-86ef-49d6-a0a5-6f843f57ac47)

---

## Mejoras (+ MPI)

Se paralelizar el proceso de forma muy sencilla
### Población Inicial dividida entre Workers.
El Master envía a todos los Workers la población a predecir y una parte (distinta de cada Worker) de la población inicial. Cada uno se encarga de mandar al Master sus k vecinos más cercanos, y el master se encarga de recibir todos los vecinos y categorizar el individuo i-ésimo a predecir. 

#### Actualizar:
- Actualizando el valor i-ésimo a predicho en todas las poblaciones de los Workers.
- No actualizar (es mucho más rápido, pero menos preciso)

#### Complejidad
- Complejidad Temporal: **O(M\*(N/nWorkers))** se ejecutan M veces (población a predecir) y cada Worker (nWorkers) recorren su población categorizada. Si se actualiza, la N, aumenta de manera uniforme.
- Complejidad Espacial: **O(N\*d + (M\*d)\*nWorkers + N)** Aumenta el espacio, ya que cada Worker tiene que tener la población a predecir. **O(N\*d + (M\*d) + N)** Se puede reducir el espacio haciendo que el Master envía el inidividuo a predecir, TODO pero aumentaría el coste temporal?.

#### MPI
- [KnnMPI_1_M](https://github.com/Danipiza/TFG/blob/main/5.%20Aprendizaje_Supervisado/KNN/KnnMPI_1_M.py): manhattan sin actualizar
- [KnnMPI_1_E](https://github.com/Danipiza/TFG/blob/main/5.%20Aprendizaje_Supervisado/KNN/KnnMPI_1_E.py): euclidea sin actualizar
- [KnnMPI_1_act_M](https://github.com/Danipiza/TFG/blob/main/5.%20Aprendizaje_Supervisado/KNN/KnnMPI_1_act_M.py): manhattan actualizando
- [KnnMPI_1_act_E](https://github.com/Danipiza/TFG/blob/main/5.%20Aprendizaje_Supervisado/KNN/KnnMPI_1_act_E.py): euclidea sin actualizar

### Población a Predecir dividida entre los Workers.
El Master envía a todos los Workers la población inicial y una parte (distinta de cada Worker) de la población a predecir. Cada uno se encarga de predecir a los individuos. Cuando un Worker predice un individuo le envia el individuo y la categoría al Master.

#### Actualizar:
- Actualizando los -numWorkers valores de cada iteración en todas las poblaciones de los Workers. Es decir, en cada iteración se espera a que el master reciba todas las predicciones de los workers para que este los envíe a todos y actualice la población.
- No actualizar (es mucho más rápido, pero menos preciso)

### Complejidad
- Complejidad Temporal: **O((M/nWorkers)\*N)** se ejecutan M/nWorkers veces (población a predecir) ya que cada Worker se encarga de una parte de la población a predecir, y recorre toda la población categorizada. Si se actualiza, la N, aumenta de manera uniforme.
- Complejidad Espacial: **O((N\*d)\*nWorkers + M\*d + N)** Aumenta el espacio, ya que cada Worker tiene que tener la población categorizada entera. 
  
#### MPI
- [KnnMPI_2_M](https://github.com/Danipiza/TFG/blob/main/5.%20Aprendizaje_Supervisado/KNN/KnnMPI_2_M.py): manhattan sin actualizar
- [KnnMPI_2_E](https://github.com/Danipiza/TFG/blob/main/5.%20Aprendizaje_Supervisado/KNN/KnnMPI_2_E.py): euclidea sin actualizar
- [KnnMPI_2_act_M](https://github.com/Danipiza/TFG/blob/main/5.%20Aprendizaje_Supervisado/KNN/KnnMPI_2_act_M.py): manhattan actualizando
- [KnnMPI_2_act_E](https://github.com/Danipiza/TFG/blob/main/5.%20Aprendizaje_Supervisado/KNN/KnnMPI_2_act_E.py): euclidea sin actualizar

---


## TODO

### EXPLICAR (DESARROLLAR)
El k-NN funciona bien en problemas de pocas dimensiones (variables) con datos abundantes.
- En estos problemas, puede encontrar puntos cercanos relevantes

El k-NN sufre la maldición de la dimensionalidad
- Al aumentar los dimensiones los vecinos no suelen estar tan cerca

Además, su rendimiento empeora si hay variables irrelevantes
- P.ej. Un punto puede ser muy parecido a otro en cuanto a las variables más relevantes, pero si consideramos variables irrelevantes puede ser que no se le considere como uno de los vecinos más cercanos

### VALIDACION CRUZADA
Por tanto, se deben evitar incluir variables irrelevantes o redundantes (este tipo de tarea se llama selección de variables o feature selection)
- Si esto no se sabe a priori, se puede usar validación cruzada para seleccionar las variables de entrada que se considerarán de entre todas las posibles
- Se elegirá aquel subconjunto de variables que minimice el error de validación

### DETERMINAR K?

### MEJORAR COSTE ESPACIAL MPI_1, MASTER ENVIA EL INDIVIDUO A PREDECIR, EN VEZ DE COMPARTIR TODO EL ARRAY


