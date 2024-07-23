#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/mman.h>

int main () {
  int stat;
  srand(time(NULL));

  void* int_mem = mmap(NULL, sizeof(int), PROT_READ|PROT_WRITE, MAP_ANON|MAP_SHARED, -1, 0);

  if (fork() == 0) {
    // as the child, write a random number to shared memory (TODO!)
    *((int*) int_mem) = rand();
    printf("Child has written %d to address %p\n", *((int*) int_mem), int_mem);
    exit(0);
  } else {
    // as the parent, wait for the child and read out its number
    wait(&stat);
    printf("Parent reads %d from address %p\n", *((int*) int_mem), int_mem);
  }
}
