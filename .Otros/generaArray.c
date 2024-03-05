#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int duplicados, neg, ordenado;

void menu(){
    printf("MENU -------------------\n");

    printf("Ordenado:\n");
    printf("0: No ordenado\n");    
    printf("1: Ordenado\n");    
    scanf("%d", &ordenado);

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
    int* nums = (int*)malloc(n*sizeof(int));

    // Inicialización del array nums
    if (!neg) {  // [1, n]
        for (int i=0;i<n;i++) {
            nums[i]=i+1;
        }
    } else {  // [-n/2, n/2)
        for (int i=0;i<n;i++) {
            nums[i]=i-n/2;
        }
    }

    srand(time(NULL)); // Inicialización de la semilla para la generación de números aleatorios
    int j=0;
    for (int i=0;i<n;i++) {
        j=rand()%(n-i);
        a[i]=nums[j];

        // Eliminar el elemento seleccionado del array nums
        for (int k=j;k<n-i-1;k++) {
            nums[k]=nums[k+1];
        }
    }

    free(nums);
}

void crearArrayConDuplicados(int a[], int n, int neg) {
    srand(time(NULL));

    if (!neg) {  // [1, n]
        for (int i=0;i<n;i++) {
            a[i]=rand()%n+1;
        }
    } else {  // [-n/2, n/2]
        for (int i=0;i<n;i++) {
            a[i]=rand()%(n+1)-n/2;
        }
    }
}

void crearArrayOrdenadoSinDuplicados(int a[], int n, int neg){
    for(int i=0; i < n;i++){
        a[i]=i-((n/2)*neg);
    }
}

void crearArrayOrdenadoDescSinDuplicados(int a[], int n, int neg){
    for(int i=n; i>=0;i--){
        a[n-i]=i-((n/2)*neg);
    }
}

void crearArrayOrdenadoConDuplicados(int a[], int n, int neg){
    int i, j, r;
    
    i=0;
    j=0-((n/2)*neg);
    srand(time(NULL));
    while(i<n){
        r=rand()%10;
        if(r<5) a[i++]=j;  
        else j++;       
    }
}

void crearArrayOrdenadoDescConDuplicados(int a[], int n, int neg){
    int i, j, r;
    
    i=0;
    j=n*(0.5)*neg;
    srand(time(NULL));
    while(i<n){
        r=rand()%10;
        if(r<5) a[i++]=j;  
        else j--;       
    }
}


int main(int argc, char** argv) {    
    //char archivo[96]; 
    char* archivo; 
    size_t archivoTam;
    int arrayTam;

    //printf("Ingrese una cadena de caracteres para el archivo: ");
    //scanf("%s", archivo);
    archivo=argv[1];
    archivoTam = strlen(archivo);    
    strcat(archivo, "Desc.txt");
    

    //printf("Ingrese el tamaño del array: ");
    //scanf("%d", &arrayTam);
    arrayTam=atoi(argv[1]);
    int *array = (int *)malloc(arrayTam*sizeof(int));
    
    /*menu();
    if(duplicados){
        if(ordenado) crearArrayOrdenadoConDuplicados(array, arrayTam, neg);
        else crearArrayConDuplicados(array, arrayTam, neg);
    }
    else {
        if(ordenado) crearArrayOrdenadoSinDuplicados(array, arrayTam, neg);
        else crearArraySinDuplicados(array, arrayTam, neg);
    }*/
    crearArrayOrdenadoDescSinDuplicados(array, arrayTam, 0);

    FILE *file;
    // Abre el archivo en modo escritura (No existe, lo crea. Si existe, lo trunca)
    file = fopen(archivo, "w");
    if (file == NULL) {
        fprintf(stderr, "No se pudo abrir el archivo %s\n", archivo);
        exit(EXIT_FAILURE);  
    }

    // Escribe el array en el archivo
    for (int i=0;i<arrayTam;i++) {
        fprintf(file, "%d ", array[i]);
    }

    
    fclose(file); // Cierra el archivo abierto
    free(array); // Libera la memoria 

    printf("Datos almacenados en %s correctamente.\n", archivo);    
    
	return 0;
}