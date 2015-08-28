#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "graph.h"


vertex **make_graph(int *N, int *K,char *name){
  /*graph needs to be preallocated memory
name is the name of the file you need opened
returns the number of lines in the file
and hence in the data,
but otherwise it messes with data in place
 */

  char s[100];
  FILE *fp =fopen(name,"r");
  if (fp == NULL) {
    printf("Couldn't open %s for reading\n",name);
    exit(1);
  }
  vertex **graph;
  *N=0, *K=0;
  int c;
  int j = 0; //place in the line
  int k = 0; //num of line
  int l = 0; //element in the line i.e "2 13 434" has only 3 elements
  int flag = 0; //checking for double spaces, probably not necessary


  //deal with the first line of text
  //which has all the important info
  while((c=fgetc(fp)) != '\n'){
    s[j]=c;
    j++;
    if (isspace(c)){
      *N= atoi(s);
      l++;

      for(int i = 0; i<j;i++){
	//this here to clear s of all data
	s[i] = 0;
      }
      j = 0; 
    }
    l=0;
  }
  *K = atoi(s);

  //initialize the graph
  graph = (vertex **) malloc(*N*sizeof(vertex *));
  for(int i = 0; i< *N; i++){
    graph[i] = malloc(sizeof(vertex));
    if(graph[i] == NULL){
      printf("couldn't allocate enough memory\n");
      exit(1);
    }
    graph[i]->edges = malloc(*K*sizeof(int));
    if(graph[i]->edges == NULL){
      printf("couldn't allocate enough memory for edges\n");
      exit(1);
    }
  }
  l = 0;
  for(int i = 0; i<j;i++){
    //this here to clear s of all data
    s[i] = 0;
  }
  j = 0; 

  while((c=fgetc(fp)) != EOF){
    //printf("%c",(char)c);
    if((char)c != '\n'){
      flag = 0; 
      s[j]=c;
      j++;
    }
    if((char)c == '\n'){

      graph[k]->edges[l-1] = atoi(s); //minus one, because the first element goes to the identity
      graph[k]->num_edges = l;
      graph[k]->cluster = 0;  
      //printf("l = %d\n", l);
      k++;
      l = 0;
      for(int i = 0; i<j;i++){
	//this here to clear s of all data
	s[i] = 0;
      }
      j = 0; 
    } else if (isspace(c)){
      if(flag){
	printf("2 spaces.. exiting  %d \n", k);
	exit(1);      
      }
      flag = 1;
      //printf("l = %d\n", l);
      if(l==0){
	graph[k]->identity = atoi(s);
      } else {
	graph[k]->edges[l-1] = atoi(s);
      }
      l++;
      for(int i = 0; i<j;i++){
	//this here to clear s of all data
	s[i] = 0;
      }
      j = 0; 
    }
  }

  fclose(fp);
  if(k != *N){
    printf("woh... mismatch between N and num_lines\n");
    exit(1);
  }

  if(graph == NULL){
    printf("ooppss... didn't initialize the graph correctly\n");
    exit(1);
  }
  return graph;
}

void destroy_graph(int N, vertex **graph){

 for(int i = 0; i< N; i++){
    free(graph[i]->edges);
    free(graph[i]);
  }
  free(graph);
}

void print_graph(int N, vertex **graph){
  for(int i =0; i<N; i++){
    printf("i = %d, identity = %d, num_edges = %d\n", i, graph[i]->identity, graph[i]->num_edges);
    printf("edges ");
    for(int j =0; j< graph[i]->num_edges; j++){
      printf("%d ", (graph[i]->edges)[j]);
    }
    printf("\n");
  }
}

void print_clusters(int N, vertex **graph){
  FILE *clusters = fopen("clusters.data" ,"w");

  for(int i = 0; i< N; i++){ 
    fprintf(clusters, "%d\n", graph[i]->cluster);
  }
  fclose(clusters);
}
