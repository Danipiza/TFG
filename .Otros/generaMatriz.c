#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>



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
    size_t filas, columnas;
    int arrayTam;

    // M100x100
    archivo=argv[1];
    //archivoTam = strlen(archivo);    
    
    
    

    //printf("Ingrese el numero de filas para la matriz: ");
    //scanf("%d", &filas);
    //printf("Ingrese el numero de columnas para la matriz: ");
    //scanf("%d", &columnas);

    // Encuentra la x en el nombre
    char *x_pos = strchr(argv[1], 'x');
    filas = atoi(argv[1] + 1); // Skip 'M'
    columnas = atoi(argv[1] + 1); // Skip 'x'
    printf("Nombre: %s, Filas: %d, Columnas:%d\n",argv[1],filas,columnas);
    
    int** matriz = (int**)malloc(filas * sizeof(int*));
    for (int i=0;i<filas;++i){
        matriz[i] = (int*)malloc(columnas*sizeof(int));
    }
    
    int numero_maximo=atoi(argv[2]);
    srand(time(NULL));    
    for (int i=0;i<filas;i++) {
        for (int j=0;j<columnas;j++) {
            matriz[i][j]=rand()%numero_maximo;
        }
    }

    
    FILE *file;
    strcat(archivo, ".txt");
    // Abre el archivo en modo escritura (No existe, lo crea. Si existe, lo trunca)
    file = fopen(archivo, "w");
    if (file == NULL) {
        fprintf(stderr, "No se pudo abrir el archivo %s\n", archivo);
        exit(EXIT_FAILURE);  
    }

    // Escribe la matriz en el archivo
    for (int i=0;i<filas;i++) {
        for (int j=0;j<columnas;j++) {
            fprintf(file, "%d ", matriz[i][j]);
        }
        fprintf(file, "\n");
    }

    
    fclose(file); // Cierra el archivo abierto
    free(matriz); // Libera la memoria 

    printf("Datos almacenados en %s correctamente.\n", archivo);    
    
	return 0;
}