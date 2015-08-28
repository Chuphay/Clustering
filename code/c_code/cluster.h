#ifndef _cluster_h
#define _cluster_h

typedef struct cluster{
  int identity;
  // int *internal_vertices;
  int num_internal_vertices;
  int area;
  int perimeter;
} cluster;

cluster *make_cluster(int identity);

void destroy_cluster(cluster *c);

#endif
