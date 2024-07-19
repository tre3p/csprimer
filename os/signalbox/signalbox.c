#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>

void window_size_changed_handler(int sig) {
  if (sig == SIGWINCH) {
    struct winsize ws;
    ioctl(0, TIOCGWINSZ, &ws);
    printf("Terminal size: %d rows, %d cols\n", ws.ws_row, ws.ws_col);
  }
}

int main() {
  signal(SIGWINCH, window_size_changed_handler);
  while (1);
}