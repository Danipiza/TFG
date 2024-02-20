#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void leeArchivo(){
    FILE *archivo;
    char nombre_archivo[100];
    int archivoTam;

    int *parametros;
    int n=100;
   
    printf("Introduce el nombre del archivo: ");
    scanf("%s", nombre_archivo);
    archivoTam = strlen(nombre_archivo);
    strcat(nombre_archivo, ".txt");

    archivo = fopen(nombre_archivo, "r"); // Modo lectura
    if (archivo == NULL) {
        perror("Error al abrir el archivo");
        exit(1);
    }

    parametros = (int *)malloc(n * sizeof(int));
    // array = (int *)realloc(array, capacidad * sizeof(int)); // aumentar tamaño

    for (int i = 0; i < n; i++) {
        fscanf(archivo, "%d", &parametros[i]);
    }
    

    printf("Array:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", parametros[i]);
    }
    printf("\n");

    fclose(archivo);    
    free(parametros); // Libera memoria 
}

int main() {
    leeArchivo();

    return 0;
}
