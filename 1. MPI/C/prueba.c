#include <stdio.h>
#include <stdlib.h>

// Función para llenar un array dinámico
int* llenarArray(int tamano, int* n) {
    int* array = (int *)malloc(tamano * sizeof(int));
    // Verificar si la asignación de memoria fue exitosa
    if (array == NULL) {
        printf("Error al asignar memoria.\n");
        return NULL; // Salir con código de error
    }
    for (int i = 0; i < tamano; i++) {
        printf("Ingrese el elemento %d: ", i + 1);
        scanf("%d", &array[i]);
    }
    *n=tamano;
    return array;
}

// Función para imprimir un array
void imprimirArray(int *array, int tamano) {
    printf("Array: ");
    for (int i = 0; i < tamano; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");
}

int main() {
    int tamano;
    
    // Pedir al usuario el tamaño del array
    printf("Ingrese el tamaño del array: ");
    scanf("%d", &tamano);

    // Llenar el array llamando a la función
    int n;
    int *miArray=llenarArray(tamano,&n);
    printf("n:%d\n",n);
    

    
    
    printf("Rellenado\n");
    // Imprimir el array llamando a otra función
    imprimirArray(miArray, tamano);

    // Liberar la memoria después de usar el array
    free(miArray);

    return 0; // Salir sin errores
}
