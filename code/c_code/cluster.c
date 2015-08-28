#include <stdio.h>
#include <stdlib.h>
#include "cluster.h"


cluster *make_cluster(int identity){
  cluster *c = malloc(sizeof(cluster));
  if(c == NULL){
    printf("couldn't allocate for the cluster\n");
    exit(1);
  }
  c->identity = identity;
  c->num_internal_vertices = 0;
  c->area = 0;
  c->perimeter = 0;
  return c;
}

void destroy_cluster(cluster *c){
  free(c);
}
