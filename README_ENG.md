*[ENGLISH](https://github.com/Danipiza/TFG/blob/main/README_ENG.md) ∙ [ESPAÑOL](README.md)* <img align="right" src="https://visitor-badge.laobi.icu/badge?page_id=danipiza.TFG" />

<hr>

<h1 align="center">
    Optimization of AI algorithms by applying high-performance computing techniques
</h1>
<h2 align="center">
    Optimización de algoritmos de IA aplicando técnicas enfocadas al cómputo de alto rendimiento 
</h2>

<br>

<div align="center">
  <img src="https://github.com/user-attachments/assets/ffad1fd9-b830-4bdf-936b-dc2295f9bfe0" alt="escudo_ucm" width="200">
</div>

<h3 align="center">
TRABAJO DE FIN DE GRADO
<br>
</h3>
<h3 align="center">
DANIEL PIZARRO GALLEGO
</h3>
<h4 align="center">
Director:
Alberto Núñez Covarrubias
</h4>
<br>
<h4 align="center">
Facultad de Informática

Complutense University of Madrid
	
September 13, 2024
</h4>

<hr>

## Index
1. [MPI](#mpi)
2. [Unsupervised Learning](#unsupervised-learning)
3. [Reinforcement Learning](#reinforcement-learning)
4. [Evolutionary Programming](#evolutionary-programming)
5. [Supervised Learning](#supervised-learning)


<h3> <img src="https://skillicons.dev/icons?i=python" alt="C Language Icon" width="20" height="20" /> Python </h3>

It is one of the most popular languages ​​for AI due to its simple syntax, wide variety of AI libraries (such as TensorFlow, PyTorch, scikit-learn, etc.), and a large developer community. But it is a fairly slow language, which means that when executing the code it will take a long time to finish.

I'm going to be programming in Python, and testing ways to reduce the execution time.
<hr>


## MPI
It is a standard for a message passing library, which aims to facilitate parallel programming in distributed environments, allowing multiple independent processes to communicate to solve tasks efficiently.

There are currently several implementations: [Open MPI](http://www.open-mpi.org/), [MPICH](http://www.mpich.org/) , [MVAPICH](http://mvapich.cse.ohio-state.edu/), [IBM Platform MPI](http://www.ibm.com/systems/es/platformcomputing/products/mpi/), [Intel MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html). En este proyecto se usa [mpi4py](https://mpi4py.readthedocs.io/en/stable/).

### Single Program Multiple Data (SPMD) 
**1 program** executed in parallel. The same program is **copied to all nodes**. Each process has its own ID (Rank) 

The main difference between **shared memory** and **distributed** lies in how memory resources are organized and managed in parallel computing systems. Shared memory has a single memory that is shared between all processes, having to execute techniques to guarantee synchronization. In its counterpart, distributed memory uses independent memories between each process, so these problems do not occur. However, communication between processes turns out to be more expensive in distributed systems.

<div align="center">
   <img  src="https://github.com/Danipiza/TFG/blob/main/.Otros/Imagenes/MPI.png" width="600" height="300"/> 
</div>

<br>

Basic scheme to run a MPI program in Python:
```python
 from mpi4py import MPI # Al importar la biblioteca en Python se genera el Environment.

 comm = MPI.COMM_WORLD     	# Communicator
 status = MPI.Status()   	# Status
 myrank = comm.Get_rank() 	# ID of each process
 numProc = comm.Get_size() 	# Number of process

 if myrank==0:           	# Master
    # Load the data set. Divide and send them.
    # Receive all processed data.
 else:                   	# Workers    
    # Receives the subset of data assigned by the Master.
    # Process the data and sends them.
```


### Directory with the code is [HERE](https://github.com/Danipiza/TFG/tree/main/0_MPI).
<hr>

## Unsupervised Learning

Unsupervised methods are machine learning algorithms that base their process on training with unlabeled data. This means, a priori, no objective value is known, whether categorical or numerical. The goal of this learning is to find patterns or structures in the data provided. These algorithms are useful in scenarios in which labeled data is scarce or unavailable.

In this project we are going to reduce the execution time of _clustering_ techniques that are responsible for grouping individuals based on some measure of similarity. The implemented algorithms are the folowings:

1. [Aglomerative](#hierarchical-agglomerative)
2. [KMeans](#kmeans)

### Hierarchical Agglomerative
```python
PHASE 1: Create the initial distance matrix D. It is a symmetric matrix (it is only necessary one triangular matrix) 
PHASE 2: Grouping of Individuals 
    o 2.1. Initial partition P0: Each object is a cluster 
    o 2.2. Calculate the following partition using the distance matrix D
         Choose the two closest clusters. They will be the row and column of the minimum value in the matrix D 
         Group the two into a cluster. Eliminate the row and column of the greater index of the grouped clusters.
	  Generate the new distance matrix D. 
	    • Update the row of the two clusters that are grouped together.
            • Calculate the distance from the rest of the clusters to the new cluster 

	 Repeat this step 2.2. until you have only one cluster with all the individuals
PHASE 3 (OPTIONAL): Represent the dendrogram.

The complexity with single and full links has a cubic cost O(N^3). There are more efficient implementations (N^2).
```

## Sequential algorithms
- [Algorithm](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative.py)

## MPI strategies implemented
### Split the matrix between processes
Split the matrix among all processes. The _master_ process is responsible for managing communication between processes to divide the algorithm between them. Depending on the distance there are more or fewer implementations.

Distance by centroids:
- [Implementation](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Cent_E.py)

Distances per simple/complete link, (greater complexity than the previous distance):
- The process that updates the row works alone.
	- [Implementation 1](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Simple_E_1.py)
- The process that updates the row works with all _workers_.
	- [Implementation 2_0](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Simple_E_2_0.py)
 	- [Implementation 2_1](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Simple_E_2_1.py)
  	- [Implementation 2_2](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Simple_E_2_2.py)


### Directory with the code is [HERE](https://github.com/Danipiza/TFG/tree/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo).

<br>
 
### Kmeans

```python
PHASE 1: Initialize the K centers of the clusters randomly.
    • Generating random points in dimensional space
    • Randomly selecting individuals
PHASE 2: Repeat this phase until the centers do not change.
    o 2.1. (Assignment): Calculate the closest cluster for each individual.
	Requires the use of a distance (usually Euclidean or Manhattan).
    o 2.2. (Update): Calculate the new centers with the calculated assignment of the individuals.
	It is calculated with the average of the values ​​of the individuals in each cluster.

Since the clusters are generated randomly, it will not always give a good result the first time.
Therefore, it is advisable to run this algorithm several times to find the best assignment.
```
## Sequential algorithms
- [Algorithm and search](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/K-Medias/KMedias.py)

## MPI strategies implemented
### Divide the population
Divide the population of individuals among all processes. The _master_ process is responsible for managing and calculating the new centers in each iteration.

Euclidean distance:
- [Implementation](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/K-Medias/KMediasMPI_uno_E.py)

Manhattan distance:
- [Implementation](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/K-Medias/KMediasMPI_uno_M.py)

### Search of the best assignment
For the search, a main loop is executed with the maximum number of centers that we want to study, that is, the algorithm is executed for the values ​​of _K_ between _\[2, K_max\]_. This main loop repeats 5 times to find the best assignment for each value of _K_. There are two implementations, the MPI strategy discussed in the previous subsection, or executing the sequential algorithm in several processes with different values ​​of _K_, but same centers.
- [Divide the population](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/K-Medias/KMediasMPI_busqueda_E_1.py)
- [Parallel sequential executions](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/K-Medias/KMediasMPI_busqueda_E_2.py)

### Directory with the code is [HERE](https://github.com/Danipiza/TFG/tree/main/1_Aprendizaje_NoSupervisado/K-Medias).

<hr>

## Reinforcement Learning
Se basa en experiencias y simulaciones, con prueba y error, recibiendo recompensas con las acciones tomadas (también pueden ser negativas). Nadie le dice al agente que hacer, éste toma las decisiones con diferentes estrategias. Se realiza una etapa de entrenamiento para que aprenda a moverse por el Environment, tomando las decisiones que maximicen las recompensas obtenidas en experiencias pasadas.

It is based on experiences and simulations, with trial and error, receiving rewards with the actions taken (they can also be negative). Nobody tells the agent what to do, he makes decisions with different strategies. A training stage is carried out so that it learns to move through the environment, making decisions that maximize the rewards obtained in past experiences.

The algorithms developed in this project are the following:
1. [Q-Learning](#q-learning)
2. [DQN](#dqn)

### Q-Learning
Mix between dynamic programming and Monte Carlo. 
- R = Reward matrix.
- Q=Matrix (States x Actions). What action to choose in each state. (highest value)

### Environment 
For this algorithm it is a maze. The agent is trained to travel from a source point to a destination point in the fewest number of actions posible.

### Hyper-parameters:
- α (learning rate): This hyper-parameter controls how much a new experience modifies.
- γ (factor de descuento): Represents how much importance we set on future rewards.
- ϵ (factor de exploración-explotación): This hyper-parameter controls the balance between exploration and exploitation. As further of the initial execution the agent is, the lower exploration actions are requiered and more exploitation to get more utility from our policy, so instead of using a fixed value, as trials increase, epsilon should decrease. At first, a high epsilon generates more episodes of exploration and at the end, a low epsilon exploits the learned knowledge.

The function used to store experiences in the Q-Table is the following:

```Q(S, A) = (1−α)*Q(S, A) + α*(R(S, A) + γ*maxi Q(S’, Ai))```


Being _S_ the current state, _A_ the action taken, _S'_ the next state and _Ai_ an action among all the agent's actions.

## Sequential algorithms
- [Algorithm](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_1.py)
- [Algorithm with preprocessing](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_2.py)

## MPI strategies implemented

### Split the environment between processes
By dividing the maze between processes, each process controls an area, and a constant flow of episodes (algorithm iterations) is generated. When an agent leaves the domain of a process, it sends a message to the process that controls that part of the maze with the position in which it enters.
- [Implementation](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_MPI_3.py)

### Parallel executions and pooling experiences
The _master_ collects the experiences of the _workers_, averaging the Q-values ​​obtained from the processes, thus calculating the best actions for each state.
- [Implementation 1](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_MPI_2_1.py)
- [Implementation 2](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_MPI_2_2.py)


### Search of hyper-parameters
Same as the previous improvement, but this time to find hyper-parameters. Each process executes different combinations and stores the results obtained in files (End, Loop, ...)
- [Implementation](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_MPI_1.py)

### Directory with the code is [HERE](https://github.com/Danipiza/TFG/tree/main/2_Aprendizaje_Por_Refuerzo/RL).
<br>

### DQN
This algorithm combines neural networks with the basis of reinforcement learning, thus eliminating the Q-Table.

The structure of the neural network depends on the problem environment. The hidden layer values ​​can be modified depending on the programmer's needs, but the input and output layer depends on the problem. The input is adapted to receive a state from the environment, such as an image represented as a matrix. The output of the network will have as many nodes as the agent has actions.

### Environment
The game Pacman, designed by the company _Namco_, and in particular the _Atari 2600_ version. The game consists of collecting all the coins in the maze without being eaten by a ghost. We implement the game -from scratch- to shape the implementation according to our interests and make the DQN algorithm more efficient and simple.

<div align="center">
  <img src="https://github.com/user-attachments/assets/ff437eec-2092-4d0c-9aad-0e1f43159c55" alt="pacman" width="400">
</div>

### Hyper-parameters:
- Gamma (discount factor \[0, 1\]). Used to know how much is subtracted from the acquired reward when performing an action in a state.
- Epsilon (exploration rate \[0, 1\]). Probability used to execute a random action or the best one so far.
- Learning rate (learning rate \[0, 1\]). For back propagation of neural networks. Essentially, it measures how much the node weights change upon failure.

In addition to these parameters, the algorithm has other variables to develop the neural networks.
- Epsilon decay. Used to not always use the same epsilon value. This variable marks how much the epsilon variable is reduced between episodes.
- Number of training examples (batch size}. Used to update the parameters of the neural network during a single training iteration.
- Hidden layer size. Set the number of neurons in each layer.

## Sequential algorithms
- [Algorithm & Pacman](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/DQN/DQN.py)


## MPI strategies implemented

### Search of hyper-parameters
Same search strategy as used in the Q-Learning algorithm.
- [Implementation](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/DQN/DQN_mpi.py)

### Same strategies as in the [NeuralNetworks](#neural-networks)

### Directory with the code is [HERE](https://github.com/Danipiza/TFG/tree/main/2_Aprendizaje_Por_Refuerzo/DQN).
<hr>

## Evolutionary Programming

Evolutionary programming is an optimization technique inspired by the theory of biological evolution. It is based on the concept of natural selection and evolution of populations to find solutions to complex problems.

A population is made up of individuals, which are subjected to evaluation, selection, crossing and mutation methods to, with the passage of generations, maximize or minimize a fitness value. An individual has a chromosome, which has one or more genes, which in turn each gene has one or more alleles. Individuals can be represented in the following ways: 
- Binary: Each allele is one bit. 
- Real: Each allele is a real number. These individuals are easier to handle.
- Trees: Each allele is a node of the tree.

### Basic template of an Evolutionary Algorithm
```python
population = init_population(size_population)
evaluate_population(population)
while(<<condicion>>):
  selection = select_population()
  # Reproduction
  population = cross_population(seleccion, prob_cruce)
  population = mutate_population(seleccion, prob_muta)  
  evaluate_population(population)
```
## Sequential algorithms
- [Terminal](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/0_terminal/main.py)
- [GUI](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/1_gui/main.py)

## MPI strategies implemented

### Divide the population
The population is divided between the generated processes. The _master_ is in charge of managing communications so that the population evolves.
- [Implementation](https://github.com/Danipiza/TFG/tree/main/3_Programacion_Evolutiva/2_MPI/1DividirPob.py)

### Island model
The population is divided into subpopulations distributed among the executed processes, to, in parallel, evolve to the general population. The processes communicate from time to time to restart the populations with the best individuals from all the processes.
- [Implementation](https://github.com/Danipiza/TFG/tree/main/3_Programacion_Evolutiva/2_MPI/2ModeloIslas_1.py)

### Pipeline
Each part of the algorithm is divided between processes. The _master_ generates subpopulations, and the executed _workers_ are in charge of evaluating, selecting, crossing and mutating the populations they receive from the previous process. Once they process the received data, they send it forward and wait to receive new data. Each process is responsible for a part, generating a constant flow of messages between the processes.
- [General](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/2_MPI/3PipeLine.py)
- [Bynary \(4 processes\)](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/2_MPI/3PipeLineBin_1.py)
- [Bynary \(7 processes\)](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/2_MPI/3PipeLineBin_2.py)
- [Real \(5 processes\)](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/2_MPI/3PipeLineReal_2.py)
- [Real \(10 processes\)](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/2_MPI/3PipeLineReal_3.py)


### Directory with the code is [HERE](https://github.com/Danipiza/TFG/tree/main/3_Programacion_Evolutiva).
<hr>


## Supervised Learning
1. [KNN](#knn)
2. [Neural Networks](#neural-networks)

### KNN
Simple but powerful. Very effective for classification and regression tasks. It is based on the idea that similar data points tend to group together in feature space. This algorithm belongs to the lazy or instance-based learning paradigm.

```python
FASE 1: Inicializar las poblaciones categorizadas y a predecir, y la variable K
FASE 2: For each individual. Classify it alongside the categorized groups
    o 2.1. Recorrer todos los individuos de la población categorizada, y almacenar las K individuos más cercanos.
    o 2.2. Asignar el cluster con más repeticiones al individuo actual.
    o 2.3. (opcional) Añadir el individuo actual a la población categorizada.

No hay una forma de determinar el mejor valor para k, por lo que hay que probar con varias ejecuciones. 
Valores pequeños de K crea sonido. 
Valores grandes con pocos datos hará que siempre sea la misma categoría

PHASE 1: Initialize the categorized and predicted populations, and the variable K
PHASE 2: For each individual. Classify it alongside the categorized groups
    o 2.1. Loop through all the individuals in the categorized population, and store the K closest individuals.
    o 2.2. Assign the cluster with the most repetitions to the current individual.
    o 2.3. (optional) Add the current individual to the categorized population.

There is no way to determine the best value for k, so you have to execute the algorithm several times with different K values 
Small values ​​of K create sound. 
Large values ​​with a small dataset will always classify the same cluster
```
## Sequential algorithms
- [Algorithm](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN.py)

## MPI strategies implemented
Las estrategias se dividen en dos principales implementaciones, actualizando la población categorizada conforme se categorizan nuevos individuos, o no actualizando. Si se actualiza se obtienen mejores resultados en cuanto a predicciones se refiere, pero el tiempo de ejecución es mucho mayor.

The strategies are divided into two main implementations, updating the categorized population as new individuals are categorized, or not updating. If it is updated, better results are obtained in terms of predictions, but the execution time is increased.

### Divide the categorized population
The categorized population is divided between the processes so that they work in parallel on the same individual. That is, each _worker_ sends the _K_ nearest neighbors of its categorized subpopulation.
Without updating:
- [Euclidean](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_1_E_NoAct.py)
- [Manhattan](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_1_M_NoAct.py)

Updating:
- [Euclidean](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_1_E_Act.py)
- [Manhattan](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_1_M_Act.py)


### Divide the population to be predicted
The population to be predicted is divided between the processes so that they work independently in parallel. That is, each _worker_ sends a different individual to the _master_ process when finishing a process.
Does not update:
- [Euclidean](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_2_E_NoAct.py)
- [Manhattan](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_2_M_NoAct.py)

Updating:
- [Euclidean](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_2_E_Act.py)
- [Manhattan](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_2_M_Act.py)



### Directory with the code is [HERE](https://github.com/Danipiza/TFG/tree/main/4_Aprendizaje_Supervisado/KNN).
<br>



### Neural Networks
Neural networks are a computational model inspired by the functioning and structure of neurons in the human brain. Essentially, they consist of layers of interconnected nodes, called artificial neurons. The neural network is made up of the following layers:
- Input layer, in which there will be as many neurons as there are input variables in the prediction model.
- Hidden layer, represented with one or more internal layers. Each one contains a certain number of neurons.
- Output layer. As in the input, it will have a number of neurons related to the output variables.

<div align="center">
  <img src="https://github.com/Danipiza/TFG/assets/98972125/cf25aa2b-00e0-45e7-877f-d97f891f1ec4" alt="escudo_ucm">
</div>




Cada neurona hace una operación simple. Suma los valores de todas las neuronas de la columna anterior. Estos valores multiplicados por un peso que determina la importancia de conexión entre las dos neuronas. Todas las neuronas conectadas tienen un peso que irán cambiando durante el proceso de aprendizaje. Además, un valor bias puede ser añado al valor calculado. Con el valor calculado se aplica a una función de activación, para obtener el valor final. 

Each neuron does a simple operation. Add the values ​​of all the neurons in the previous column (layer). These values ​​are multiplied by a weight that determines the importance of the connection between the two neurons. All connected neurons have a weight that will change during the learning process. Additionally, a bias value can be added to the calculated value. With the calculated value it is applied to an activation function, to obtain the final value.

Learning/training process:
```python
PHASE 1: Initialize the neural network weights with the initialization data
PHASE 2: Training
    o 2.1. (Forward) Send an individual through the neural network. Add the value received from the previous layer multiplied
	by the weights of the current layer with the next one. This determines the importance of connection between neurons.
	With the calculated value it is applied to an activation function and passed to the next layer until reaching the output.
    o 2.2. (Backpropagation) Send the error made backwards. The predicted value calculated at the output is compared with
	the label, and the error is calculated. This error is sent back by updating the weights. Multiplication is added
	of the predicted value in each layer with the learning rate and the error.
```

## Sequential algorithms
- [Algorithm](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_1_2.py)
- [Search of hyper-parameters](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_2_1.py)

## MPI strategies implemented

### Pipeline
As in evolutionary algorithms, each process is responsible for a part of the model to generate a constant flow of messages. In this case each _worker_ is in charge of a layer.
- [Synchronous](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_MPI_1_3.py)
- [Asynchronous](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_MPI_1_4.py)

### Split the training
Se divide la población de entrenamiento entre los procesos. Al final se juntan las experiencias haciendo la media. (No funciona correctamente, da malas predicciones)
The training population is divided between the processes. In the end the experiences are combined to calculate the average. (Does not work correctly, gives bad predictions)
- [Implementation](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_MPI_3_1.py)

### Search of hyper-parameters
As in other algorithms, sequential executions are executed in parallel, where each process stores the results.
- [Implementation](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_MPI_2_1.py)

### Directory with the code is [HERE](https://github.com/Danipiza/TFG/tree/main/4_Aprendizaje_Supervisado/Redes_Neuronales).
<hr>
