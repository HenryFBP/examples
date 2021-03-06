// Author: Wes Kendall
// Copyright 2011 www.mpitutorial.com
// This code is provided freely with the tutorials on mpitutorial.com. Feel
// free to modify it for your own use. Any distribution of the code must
// either provide a link to www.mpitutorial.com or keep this header intact.
//
// An intro MPI hello world program that uses MPI_Init, MPI_Comm_size,
// MPI_Comm_rank, MPI_Finalize, and MPI_Get_processor_name.
//
#include "mpi.h"
#include "stdio.h"
#define MASTER 10

int main(int argc, char** argv) {

	// Initialize the MPI environment. The two arguments to MPI Init are not
	// currently used by MPI implementations, but are there in case future
	// implementations might need the arguments.
	MPI_Init(NULL, NULL);

	// Get the number of processes
	int world_size;
	MPI_Comm_size(MPI_COMM_WORLD, &world_size);

	// Get the rank of the process
	int world_rank;
	MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

	// Get the name of the processor
	char processor_name[MPI_MAX_PROCESSOR_NAME];
	int name_len;
	MPI_Get_processor_name(processor_name, &name_len);

	// Print off a hello world message
	printf("Hello world from processor %s, rank %d out of %d processors\n",
		processor_name, world_rank, world_size);

	int GIVER = 1;
	int RECIEVER = 3;

	if (world_rank == RECIEVER)
	{
		char* basket[100];
		printf("I want bananas from processor '%d'!\n", GIVER);
		MPI_Recv(&basket, 100, MPI_CHAR, GIVER, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

		printf("I got: '%s'\n", basket);
	}
	if (world_rank == GIVER)
	{
		char* present = "bananas";

		printf("Giving '%s' to processor '%d'!\n", present, RECIEVER);
		MPI_Send(present, 100, MPI_CHAR, RECIEVER, 0, MPI_COMM_WORLD);
	}



	// Finalize the MPI environment. No more MPI calls can be made after this
	MPI_Finalize();
}
