#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define CONTAINER_ROOT "/home/container"

int main(int argc, char**argv) {
  int cp = fork();
  if (cp < 0) {
    fprintf(stderr, "fork failed\n");
    exit(1);
  } else if (cp == 0) {
    if (chroot(CONTAINER_ROOT) != 0) {
      perror("chroot");
      exit(1);
    }

    chdir("/");

    if (execvp(argv[1], argv)) {
      fprintf(stderr, "execvp failed '%m'\n");
      exit(1);
    }
  }

  wait(NULL);
}