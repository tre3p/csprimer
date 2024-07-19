#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
  printf("hello (pid: %d)\n", (int) getpid());
  int rc = fork();
  if (rc < 0) {
    fprintf(stderr, "fork failed\n");
    exit(1);
  } else if (rc == 0) {
    printf("child (pid: %d)\n", (int) getpid());
  } else {
    int rc_wait = wait(NULL);
    printf("parent of %d (rc_wait: %d) (pid: %d)\n", rc, rc_wait, (int) getpid());
  }

  return 0;
}