#include <stdio.h>
#include <stdlib.h>
#include "graph.h"
#include "cluster.h"

#define MAX_CLUSTERS 100

int N, K;
int *cluster_id;
int *num_edges;
double alpha;
FILE *perimeter_file; 


int find_next_vertex(int seed, vertex **graph, cluster *cluster){
  //returns the number of the next cluster to add
  //if there is a good one
  //otherwise returns -1
  //We will only look at edges that the seed node contains


  double old_ratio = alpha*(cluster->area)/((double)cluster->perimeter + 0.00001); //avoid divide by zero
  double new_ratio;

  int out = -1;

  int new_node;
  for(int i=0; i< graph[seed]->num_edges; i++){

    new_node = graph[seed]->edges[i];
    if(cluster_id[new_node] == 0){
 
      int num_new_edges = 0;
      for(int j=0; j<graph[new_node]->num_edges; j++){
	if(num_edges[graph[new_node]->edges[j]] != cluster->identity)
	  num_new_edges++;
      }

      double new_perimeter = cluster->perimeter + graph[new_node]->num_edges - 2*num_edges[new_node];
      double new_area = cluster->area + num_edges[new_node];

      new_ratio = new_area/(new_perimeter + 0.00001);
      //do our stopping condition
      if(new_ratio >= old_ratio){
	old_ratio = new_ratio;
	out = new_node;
      }
    }
  }

  return out;
}

void add_vertex(int v, vertex **graph, cluster *cluster){

  int c_identity = cluster->identity;
  graph[v]->cluster = c_identity;
  cluster->num_internal_vertices++;
  cluster_id[v] = c_identity;

  int num_edges_pointing_to_cluster = 0; //just for bookkeeping purposes
  int new_node;
  for(int i=0; i< graph[v]->num_edges; i++){
    //looking at the nodes that the vertex points to
    new_node = graph[v]->edges[i]; 
    if(graph[new_node]->cluster == 0){
      //new_node really is a new node

      num_edges[new_node]++;
      cluster->perimeter++;
    } else if(graph[new_node]->cluster == c_identity){
      //this means that this edge already points to the cluster
      num_edges_pointing_to_cluster++;

    } else {
      //this means it points to some other cluster
      cluster->perimeter++;
      //printf("%d is already in a cluster...\n", graph[new_node]->identity);

    }
  }
  //how many edges point to this vertex?
  if(cluster->num_internal_vertices != 1){
    //above if to check this is not the first node

    int n_count = num_edges[v]; 
    if(num_edges_pointing_to_cluster != n_count){

      printf("yikes.... aborting\n");
      printf("seed: %d num_edges: %d n_count: %d\n",v, num_edges_pointing_to_cluster, n_count);
      exit(1);
    }
    //take that number away from the perimeter
    cluster->perimeter -= n_count;

    //and add that number to the area
    cluster->area += n_count;

    num_edges[v] = 0;

    if(n_count == -1){
      printf("woh... count of edges is negative?\n");
      exit(1);
    }
  }
}

void recursively_make_cluster(int seed, vertex **graph, cluster *c){
  fprintf(perimeter_file, "%d\n", c->perimeter);

  add_vertex(seed, graph, c);

  int next_vertex = find_next_vertex(seed, graph, c);
  while(next_vertex != -1){
    recursively_make_cluster(next_vertex, graph, c);
    next_vertex = find_next_vertex(next_vertex, graph, c);
  }
}



int main(int argc, char **argv){

  if(argc>1){
    alpha = atof(argv[1]);
    printf("setting alpha to %f\n", alpha);
  } else {
    alpha = 1.0;
    printf("setting alpha to 1\n");
  }

  perimeter_file = (FILE *)fopen("perimeter.data","w"); 
 

  vertex **graph = make_graph(&N, &K,"test.data");
  printf("N = %d, K = %d\n",N,K);
  cluster_id = malloc(N*sizeof(int));
  num_edges = malloc(N*sizeof(int));
  for(int i = 0; i<N; i++){
    num_edges[i] = 0;
    cluster_id[i] = 0;
  }



  cluster **clusters = malloc(MAX_CLUSTERS*sizeof(cluster *));
  int num_clusters = 0;
  for(int i = 0; i<N; i++){
    if(graph[i]->cluster == 0){
      for(int j = 0; j<N; j++)
	num_edges[j] = 0;

      //printf("making a new cluster, with seed %d and identity %d\n", i, num_clusters+1);
      clusters[num_clusters] = make_cluster(num_clusters+1);
      recursively_make_cluster(i, graph, clusters[num_clusters]);
      num_clusters++;
      if(num_clusters>=MAX_CLUSTERS-1){
	//minus to be on the safe side 
	printf("ukk... too many clusters\n");
	exit(1);
      }
    }
  }


  printf("num_of_clusters %d\n", num_clusters);
  for(int i = 0; i<num_clusters; i++)
    printf("cluster %d has %d elements\n", i+1, clusters[i]->num_internal_vertices);
  print_clusters(N, graph);


  //free all the memory
  for(int i = 0; i<num_clusters; i++)
    destroy_cluster(clusters[i]);
  free(clusters);

  destroy_graph(N, graph);

  free(cluster_id);
  free(num_edges);

  return 0;
}
