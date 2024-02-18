#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define INPUT_SIZE 2
#define HIDDEN_SIZE 3
#define OUTPUT_SIZE 1

// Estructura para representar una capa de la red neuronal
// También se puede hacer con una matriz
typedef struct {
    double weights[INPUT_SIZE][HIDDEN_SIZE];
    double bias[HIDDEN_SIZE];
} HiddenLayer;

typedef struct {
    double weights[HIDDEN_SIZE][OUTPUT_SIZE];
    double bias[OUTPUT_SIZE];
} OutputLayer;



// Función de activación ReLU
double f(double x) {
    return fmax(0, x);
}



// -----------------------------------------------------------------------
// Inicializacion de la red neuronal -------------------------------------

// - Inicialización de pesos aleatorios entre -1 y 1

void init(HiddenLayer *layer, OutputLayer *layer){
	// Capas ocultas 
	for (int i=0;i<INPUT_SIZE;i++) {
        for (int j=0;j<HIDDEN_SIZE;j++) {
            layer->weights[i][j] = ((double)rand() / RAND_MAX) * 2 - 1; 
        }
    }

    for (int j=0;j<HIDDEN_SIZE;j++) {
        layer->bias[j] = 0.0;
    }
	
	// Capa de salida 
	for (int i=0;i<HIDDEN_SIZE;i++) {
        for (int j=0;j<OUTPUT_SIZE;j++) {
            layer->weights[i][j] = ((double)rand() / RAND_MAX) * 2 - 1; 
        }
    }

    for (int j=0;j<OUTPUT_SIZE;j++) {
        layer->bias[j] = 0.0;
    }
}


// -----------------------------------------------------------------------

// -----------------------------------------------------------------------
// Función de propagación hacia adelante ---------------------------------
double forward(HiddenLayer *hidden_layer, OutputLayer *output_layer) {
    
	
	

    return output[0]; 
}
// -----------------------------------------------------------------------

int main() {
    HiddenLayer hidden_layer;
    OutputLayer output_layer;
	
	init(&hidden_layer, &output_layer)

    // Entrada 
    double input[INPUT_SIZE] = {0.5, 0.7};
	
	// TODO
	// Entrenamiento
	

    
	
	// TODO
	// Comprobacion de resultados
	// Optimizar: tasa de acierto, capas ocultas,
	// Aplicar algoritmo de backpropagation
	
	
	// Propagación hacia adelante TODO
    double output = forward(&hidden_layer, &output_layer);

    printf("Output: %f\n", output);

    return 0;
}