#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define ASCII_LOWERCASE_LOWER_BOUND 97
#define ASCII_LOWERCASE_UPPER_BOUND 122
#define ASCII_UPPERCASE_LOWER_BOUND 65
#define ASCII_UPPERCASE_UPPER_BOUND 90
#define ASCII_UPPERCASE_TO_LOWERCASE_MASK 0x20
#define ASCII_LETTERS_COUNT 26

bool ispangram(char *s) {
  char seen_letters[ASCII_LETTERS_COUNT];
  memset(seen_letters, 0, ASCII_LETTERS_COUNT); // fill array with zeros
  char *str_ptr = s;

  char c;
  while ((c = *str_ptr) != '\0') {
      if (c >= ASCII_LOWERCASE_LOWER_BOUND && c <= ASCII_LOWERCASE_UPPER_BOUND) {
          seen_letters[c - ASCII_LOWERCASE_LOWER_BOUND] = 1;
      } else if (c >= ASCII_UPPERCASE_LOWER_BOUND && c <= ASCII_UPPERCASE_UPPER_BOUND) {
          seen_letters[(c | ASCII_UPPERCASE_TO_LOWERCASE_MASK) - ASCII_LOWERCASE_LOWER_BOUND] = 1;
      }

      str_ptr++;
  }

  for (char i = 0; i < ASCII_LETTERS_COUNT; i++) {
      if (seen_letters[i] != 1) {
          return false;
      }
  }

  return true;
}

#define BS_MASK 0x3FFFFFF

bool is_pangram_fast(char *s) {
    unsigned int bs = 0;

    char c;
    while ((c = *s) != '\0') {
        if (isalpha(c)) {
            char lower = c | ASCII_UPPERCASE_TO_LOWERCASE_MASK;
            bs |= 1 << (lower - 'a');
        }

        s++;
    }

    return bs == BS_MASK;
}

int main() {
  size_t len;
  ssize_t read;
  char *line = NULL;
  while ((read = getline(&line, &len, stdin)) != -1) {
    if (is_pangram_fast(line))
      printf("%s", line);
  }

  if (ferror(stdin))
    fprintf(stderr, "Error reading from stdin");

  free(line);
  fprintf(stderr, "ok\n");
}
