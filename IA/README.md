# Aprendizaje Automático

## Aprendizaje no supervisado
- Algoritmos de agrupamiento jerárquico
- Algoritmos de agrupamiento basado en particiones
## Aprendizaje supervisado
- k vecinos más cercanos
- Árboles de decisión
- Perceptrón multicapa

La __capacidad de aprendizaje__ permite realizar nuevas tareas que previamente no podían realizarse, o bien realizar mejor (más rápidamente, con mayor exactitud, etc.) las que ya se realizaban, como resultado de los cambios producidos en el sistema al resolver problemas anteriores.

__La capacidad de aprendizaje no puede añadirse a posteriori.__


La __IA simbólica__ trata con representaciones simbólicas de alto nivel (cercanas al entendimiento humano). Adecuada para:
- Representar conocimiento humano y razonar con él
- Resolver problemas bien-definidos o de índole lógica

La __IA subsimbólica__ es capaz de tratar con representaciones cercanas al problema y extraer conocimiento de ellas.

## Aprendizaje Automático (machine learning) e IA subsimbólica
En el aprendizaje automático, mediante algoritmos de aprendizaje se extraen “reglas” o “patrones” de los datos. Las aproximaciones de aprendizaje subsimbólico proporcionan
- Mayor robustez frente al ruido
- Mayor capacidad de escalamiento (nuevos ejemplos o nuevas variables)
- Mayor capacidad para trabajar con cantidades ingentes de datos
- Menor dependencia del experto

__Aprendizaje supervisado:__ Hay que suministrar al sistema ejemplos clasificados. El objetivo es descubrir "reglas" de clasificación 

__Aprendizaje no supervisado__ o por descubrimiento: No hay información sobre la clase a la que pertenecen los ejemplos. Objetivo: descubrir patrones en el conjunto de entrenamiento que permitan agrupar y diferenciar unos ejemplos de otros

### Representación de los individuos
Partimos de datos que son un conjunto de descripciones de objetos. Tendremos un número de individuos o elementos (n) descrito por un conjunto de variables (m).

Los datos se representan en forma de matriz 𝒏𝒏 × 𝒎𝒎 donde las filas son los individuos y las columnas las variables
- Variable Cuantitativa: variables reales o enteras
- Variable Cualitativa: variables categóricas u ordinales (p.ej. grupos de edad) 
![Representacion_Individuos](https://github.com/Danipiza/TFG/assets/98972125/20d52cd6-40df-4873-9ba0-d791fca48396)
Si tenemos 3 variables cuantitativas nuestros individuos pueden considerarse como puntos en un espacio tridimensional