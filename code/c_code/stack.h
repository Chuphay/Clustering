#ifndef _stack_h
#define _stack_h

//compile:
//gcc -Wall -O3 -c -o stack.o stack.c

typedef struct stack{
  int key;
  int count;
  struct stack *next;
} stack;

void destroy_stack(stack *root);

void push_stack(int key, stack **root);

void peek_stack(int *key, int *count, stack **root);

void pop_stack(int *key, int *count, stack **root);

int search_stack(int key, int *count, stack *root);

int get_stack(int *key, int *count, int n, stack *root);

int del_key_from_stack(int key, stack **root);

void print_stack(stack *root);

#endif
