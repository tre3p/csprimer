#include <dirent.h>
#include <stdio.h>
#include <assert.h>
#include <sys/stat.h>

int main() {
  DIR *d = opendir(".");
  assert(d != NULL);

  struct dirent *dir_entry;
  struct stat f_stat;

  while ((dir_entry = readdir(d)) != NULL) {
    stat(dir_entry->d_name, &f_stat);
    printf("%lld %s\n", f_stat.st_size, dir_entry->d_name);
  }

  closedir(d);
}