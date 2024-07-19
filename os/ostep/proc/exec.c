#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

int main() {
  printf("parent (pid: %d)\n", (int) getpid());
  int rc = fork();
  if (rc < 0) {
    fprintf(stderr, "fork failed\n");
    exit(1);
  } else if (rc == 0) {
    printf("child (pid: %d)\n", (int) getpid());
    char *p_args[3];
    p_args[0] = strdup("wc");
    p_args[1] = strdup("exec.c");
    p_args[2] = NULL;
    execvp(p_args[0], p_args);
    printf("this shouldn't print out\n");
  } else {
    int rc_wait = wait(NULL);
    printf("parent of %d (pid: %d)\n", rc_wait, (int) getpid());
  }
}