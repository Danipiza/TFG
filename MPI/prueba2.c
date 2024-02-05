#include <stdio.h>
#include <stdlib.h>
#include "mpi.h"

int rank, numProcesos, resultado, num;
int main (int argc, char* argv[] ) {
    int i;
    int *numbers, *square;

    MPI_Status status;
    MPI_Init( &argc, &argv );
    MPI_Comm_size( MPI_COMM_WORLD, &numProcesos);
    MPI_Comm_rank( MPI_COMM_WORLD, &rank);
    square=(int*)malloc((numProcesos-1)*sizeof(int));

    if (rank == 0){
        for (i=2; i<=numProcesos; i++){
            MPI_Send(&i, 1, MPI_INTEGER, i-1, 1, MPI_COMM_WORLD);
        }
        for (i=1; i<numProcesos; i++){
            MPI_Recv(&(square[i-1]), 1, MPI_INTEGER, MPI_ANY_SOURCE, 1, MPI_COMM_WORLD, &status);
            printf("Recibido de %d\n", status.MPI_SOURCE);
        }
        for (i=1; i<numProcesos; i++){
            resultado += square[i-1];
        }
        printf ("El resultado es: %d\n", resultado);
    }
    else{
        MPI_Recv( &num, 1, MPI_INTEGER, 0, 1, MPI_COMM_WORLD, &status);
        num = num*num;
        printf("ANTES HIJO, %d. Enviado: %d\n",rank,num);
        MPI_Send(&num, 1, MPI_INTEGER, 0, 1, MPI_COMM_WORLD);
        printf("HIJO, %d. Enviado: %d\n",rank,num);
    }
    MPI_Finalize();
}