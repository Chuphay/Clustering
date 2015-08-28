#ifndef _graph_h
#define _graph_h

//compile:
//gcc -std=c99 -Wall -O3 -c -o graph.o graph.c


typedef struct vertex{
  int identity;
  int *edges;
  int num_edges;
  int cluster;
  int edges_pointing_to_me;
  int my_cluster;
} vertex;

vertex **make_graph(int *N, int *K,char *name);

void destroy_graph(int N, vertex **graph);

void print_graph(int N, vertex **graph);

void print_clusters(int N, vertex **graph);


#endif
