#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX 16

//gcc make_data.c -lm -o make_data



int length = 0;
double data[MAX] = {};

void fractal_tree(int n, double bottom, double top, int flag){
  double md1 = (top - bottom)/4;
  double md2 = 3*(top - bottom)/4;
  if(n == 0){ 
    if(flag == 1){
      //printf("woh, %f\n",top);
      if(length<MAX){
      data[length] = top;
      length++;
      } else {
	printf("Ran out of memory\n");
      }
    }
  } else {

    fractal_tree(n-1, bottom, bottom + md1,0);
    fractal_tree(n-1, bottom + md2, top, 1);
  }
}

double gaussSim(double x1, double y1, double x2, double y2){
  double sigma = 0.15;
  double eps = 0.001;
  double sqX = (x1 - x2)*(x1 - x2);
  double sqY = (y1 - y2)*(y1 - y2);

  double out = exp(-(sqX+sqY)/sigma);

  if(out< eps)
    return 0;
  else
    return out;
}


int main(){

  //printf("yo %f\n",log(MAX)/log(2));
  fractal_tree(log(MAX)/log(2) + 1,0,1,0);
  int i, j;
  double *coordinates = malloc(2*MAX*MAX*sizeof(double));
  for(i = 0; i<length; i++){
    //printf("%f\n", data[i]);
    for(j = 0; j<length; j++){
      //printf("%d %d %f %f\n", i,j,data[i], data[j]);
      if(j%2 == 0){

	coordinates[i*MAX + j] = data[i];
	coordinates[i*MAX + j + 1] = data[j];
      } else {
	coordinates[MAX*MAX + i*MAX + j-1] = data[i];
	coordinates[MAX*MAX + i*MAX + j] = data[j];
      }

    }
  }

  //printf("length of data: %d\n", length);
  //for(i=0; i <2*MAX*MAX; i = i+2) printf("%f %f\n", coordinates[i], coordinates[i+1]);
  //printf("gaussSim: %f\n",gaussSim(0,0,0.1,0.1));

  double **AdjacencyMatrix = malloc(MAX*MAX*sizeof(double *));
  for(i=0;i<MAX*MAX;i++)
    AdjacencyMatrix[i] = malloc(MAX*MAX*sizeof(double));

  for(i=0;i<2*MAX*MAX;i = i+2){
    for(j=0;j<2*MAX*MAX;j =j+2){
      //printf("i %d j %d\n",i,j);
      if(i<=j){
	
	double temp = gaussSim(coordinates[i],coordinates[i+1],\
			       coordinates[j],coordinates[j+1]);
	//printf("%f %f %f\n", coordinates[j], coordinates[j+1], temp);
	AdjacencyMatrix[i/2][j/2] = temp;
	AdjacencyMatrix[j/2][i/2] = temp;
      }

    }
  }


  FILE *a_m = fopen("adjacencyMatrix.data" ,"w");

  for(i = 0; i< MAX*MAX; i++){ 
    for(j = 0; j< MAX*MAX; j++){
      fprintf(a_m, "%f ",AdjacencyMatrix[i][j] );
    }
    fprintf(a_m,"\n");
  }
  fclose(a_m);

  FILE *coo = fopen("coordinates.data" ,"w");
  for(i=0; i <2*MAX*MAX; i = i+2) fprintf(coo, "%f %f\n", coordinates[i], coordinates[i+1]);
  fclose(coo);


  return 0;
}
