#include <stdio.h>
#include <stdlib.h>
#include "stack.h"

//compile:
//gcc -Wall -O3 -c -o stack.o stack.c


void destroy_stack(stack *root){
  if(root != NULL){
    destroy_stack(root->next);
    free(root);
  }
}

void push_stack(int key, stack **root){
  if(*root == NULL){
    //initialize the stack
    *root = (stack *)malloc(sizeof(stack));
    if(root == NULL){
      printf("couldn't initialize the stack. exiting\n");
      exit(1);
    }

    (*root)->key = key;
    (*root)->count = 1;
    (*root)->next = NULL;     
  } else {
    //stack has already been initialized
    //now we need to check if the key is already in the stack
    stack **leaf = root;
    int flag = 0;
    while(*leaf != NULL){
      if((*leaf)->key == key){
	(*leaf)->count++;
	flag = 1;
	break;
      }
      leaf = &(*leaf)->next;
    } 
    if(flag == 0){
      //key is not in the stack
      //therefore we add it to the stack
      //we need to switch the root with the new key value
      //so that it is on top of the stack

      stack *new_root = malloc(sizeof(stack));
      if(new_root == NULL){
	printf("couldn't get enough memory. exiting\n");
	exit(1);
      }
      new_root->key = (*root)->key;
      new_root->count = (*root)->count;
      new_root->next = (*root)->next;
      (*root)->key = key;
      (*root)->count = 1;
      (*root)->next = new_root;
    }
  }
}

void peek_stack(int *key, int *count, stack **root){
  *key = (*root)->key;
  *count = (*root)->count;
}

void pop_stack(int *key, int *count, stack **root){
  if(*root == NULL){
    printf("Nothing in the stack. exiting\n");
    exit(1);
  }

  *key = (*root)->key;
  *count = (*root)->count;

  stack *leaf = (*root)->next;
  if(leaf != NULL){
    (*root)->key = leaf->key;
    (*root)->count = leaf->count;
    (*root)->next = leaf->next;
  } else {
    //popping the only node
    free(*root);
    *root = NULL;
  }

  free(leaf);
}

int search_stack(int key, int *count, stack *root){
  //this one is kind of confusing
  //search for a key
  //I'll place the count in the count variable
  //returns 1 for success
  //and 0 for fail
  int flag = 0;
  while(root != NULL){
    if(root->key == key){
      *count = root->count;
      flag = 1;
      break;
    }
    root = root->next;
  }
  return flag;
}

int get_stack(int *key, int *count, int n, stack *root){
  //here's another confusing one
  //give me two arrays key and count
  //and i'll place stuff in there up to the limit n
  //I'll return how long the list is,
  //if the list is more than n, 
  //I'll abort
  int num = 0;
  while(root != NULL){
    if(num>=n){
      printf("perimeter is bigger than allowed\n");
      break;
    }
    key[num] = root->key;
    count[num] = root->count;
    root = root->next;
    num++;
  }
  return num;
}

int del_key_from_stack(int key, stack **root){
  //returns count for success
  //and -1 for fail
  int out = -1;
  if((*root) == NULL){
    return out;
  } else if((*root)->key == key){
    out = (*root)->count;
    stack *leaf = (*root)->next;
    if(leaf != NULL){
      (*root)->key = leaf->key;
      (*root)->count = leaf->count;
      (*root)->next = leaf->next;
    } else {
      //no leafs, simply deleting the node
      free(*root);
      *root = NULL;
    }
    free(leaf);
    return out;

  } else {
    return del_key_from_stack(key, &((*root)->next));
  }
}



void print_stack(stack *root){
  if(root != NULL){
    printf("key: %d count: %d\n", root->key, root->count);
    print_stack(root->next);
  }
}

/*
int main(){
  stack *root = NULL; //necessary to initialize root to 0
  print_stack(root);
  push_stack(3, &root);
  push_stack(76, &root);
  push_stack(4, &root);
  push_stack(3, &root);
  push_stack(17, &root);
  push_stack(76, &root);
  push_stack(76, &root);
  int key, count;
  peek_stack(&key, &count, &root); 
  printf("Peeking: %d, %d\n", key, count);
  print_stack(root);
  pop_stack(&key, &count, &root);
  printf("popped %d, %d\n", key, count);
  print_stack(root);
  int count2;
  int success = search_stack(78, &count2, root);
  printf("success in finding 78: %d, and count %d\n", success, count2);
  int keys[12];
  int counts[12];
  int tot_count = get_stack(keys, counts, 12, root);
  for(int i=0; i<tot_count; i++)
    printf("tot--key: %d count: %d\n", keys[i], counts[i]);



  int n_count = del_key_from_stack(76, &root);
  printf("deleted and the count was %d\n", n_count);

  destroy_stack(root);
  return 0;
}
*/
