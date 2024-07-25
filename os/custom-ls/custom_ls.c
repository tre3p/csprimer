#include <dirent.h>
#include <stdio.h>
#include <assert.h>
#include <sys/stat.h>
#include <string.h>

void list_dir(char *current_path, int print_indent) {
  DIR *d = opendir(current_path);
  assert(d != NULL);

  struct dirent *dir_entry;
  struct stat f_stat;

  while ((dir_entry = readdir(d)) != NULL) {
    stat(dir_entry->d_name, &f_stat);
    char *file_name = dir_entry->d_name;
    off_t file_size_b = f_stat.st_size;

    printf("%*s %lld - %s\n", print_indent, " ", file_size_b, file_name);

    if (dir_entry->d_type == 4 && strcmp(file_name, ".") != 0 && strcmp(file_name, "..") != 0)  {
      char buf[2048];
      sprintf(buf, "%s/%s", current_path, file_name);
      list_dir(buf, print_indent + 4);
    }
  }

  closedir(d);
}

int main() {
  list_dir(".", 0);
}