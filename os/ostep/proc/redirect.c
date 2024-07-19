#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/wait.h>

int main() {
  int rc = fork();
  if (rc < 0) {
    fprintf(stderr, "fork failed\n");
  } else if (rc == 0) {
    close(STDOUT_FILENO);
    open("./redirect.output", O_CREAT|O_WRONLY|O_TRUNC, S_IRWXU);
    char *args[3] = {
        strdup("wc"),
        strdup("redirect.c"),
        NULL
    };
    execvp(args[0], args);
  } else {
    int rc_wait = wait(NULL);
  }

  return 0;
}