#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int duplicados, neg;

void menu(){
    printf("MENU -------------------\n");

    printf("Elige:\n");
    printf("0: Sin duplicados\n");    
    printf("1: Con duplicados\n");    
    scanf("%d", &duplicados);

    printf("Elige:\n");
    printf("0: Sin valores negativos\n"); 
    printf("1: Con valores negativos\n");    
    scanf("%d", &neg);   

    printf("-------------------------\n");
}

void crearArraySinDuplicados(int a[], int n, int neg) {
    int* nums = (int*)malloc(n * sizeof(int));

    // Inicialización del array nums
    if (!neg) {  // [1, n]
        for (int i = 0; i < n; i++) {
            nums[i] = i + 1;
        }
    } else {  // [-n/2, n/2)
        for (int i = 0; i < n; i++) {
            nums[i] = i - n / 2;
        }
    }

    srand(time(NULL)); // Inicialización de la semilla para la generación de números aleatorios
    int j = 0;
    for (int i = 0; i < n; i++) {
        j = rand() % (n - i);
        a[i] = nums[j];

        // Eliminar el elemento seleccionado del array nums
        for (int k = j; k < n - i - 1; k++) {
            nums[k] = nums[k + 1];
        }
    }

    free(nums);
}

void crearArrayConDuplicados(int a[], int n, int neg) {
    srand(time(NULL));

    if (!neg) {  // [1, n]
        for (int i = 0; i < n; i++) {
            a[i] = rand() % n + 1;
        }
    } else {  // [-n/2, n/2]
        for (int i = 0; i < n; i++) {
            a[i] = rand() % (n + 1) - n / 2;
        }
    }
}


int main() {    
    char archivo[96]; 
    size_t archivoTam;
    int arrayTam;

    printf("Ingrese una cadena de caracteres para el archivo: ");
    scanf("%s", archivo);
    archivoTam = strlen(archivo);    
    strcat(archivo, ".txt");
    

    printf("Ingrese el tamaño del array: ");
    scanf("%d", &arrayTam);
    int *array = (int *)malloc(arrayTam * sizeof(int));
    
    menu();
    if(duplicados>0) crearArraySinDuplicados(array, arrayTam, neg);
    else crearArraySinDuplicados(array, arrayTam, neg);

    FILE *file;
    // Abre el archivo en modo escritura (No existe, lo crea. Si existe, lo trunca)
    file = fopen(archivo, "w");
    if (file == NULL) {
        fprintf(stderr, "No se pudo abrir el archivo %s\n", archivo);
        exit(EXIT_FAILURE);  
    }

    // Escribe el array en el archivo
    for (int i = 0; i < arrayTam; i++) {
        fprintf(file, "%d ", array[i]);
    }

    
    fclose(file); // Cierra el archivo abierto
    free(array); // Libera la memoria 

    printf("Datos almacenados en %s correctamente.\n", archivo);    
    
	return 0;
}