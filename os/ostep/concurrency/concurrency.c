#include <pthread.h>
#include <stdio.h>

static int counter = 0;
pthread_mutex_t counter_lock = PTHREAD_MUTEX_INITIALIZER;

void *print() {
  for (int i = 0; i < 1e7; i++) {
    pthread_mutex_lock(&counter_lock);
    counter++;
    pthread_mutex_unlock(&counter_lock);
  }

  return NULL;
}

int main() {
  printf("main: creating threads\n");
  pthread_t p1, p2;
  pthread_create(&p1, NULL, print, NULL);
  pthread_create(&p2, NULL, print, NULL);

  printf("main: waiting for threads\n");
  pthread_join(p1, NULL);
  pthread_join(p2, NULL);

  printf("main: value of counter: %d\n", counter);
  return 0;
}