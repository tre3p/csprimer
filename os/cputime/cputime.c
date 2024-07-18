#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/syscall.h>
#include <sys/time.h>
#include <sys/resource.h>

#define SLEEP_SEC 3
#define NUM_MULS 100000000
#define NUM_MALLOCS 100000
#define MALLOC_SIZE 1000

// TODO define this struct
struct profile_times {
  // PID
  pid_t curr_pid;

  // Real stats
  time_t start_real_time_sec;
  suseconds_t start_real_time_microsec;
  time_t end_real_time_sec;
  suseconds_t end_real_time_microsec;

  // User stats
  time_t start_user_ru_sec;
  suseconds_t start_user_ru_microsec;
  time_t end_user_ru_sec;
  suseconds_t end_user_ru_microsec;

  // Kernel stats
  time_t start_kernel_ru_sec;
  suseconds_t start_kernel_ru_microsec;
  time_t end_kernel_ru_sec;
  suseconds_t end_kernel_ru_microsec;
};

struct timeval *get_current_time() {
  struct timeval *tv = (struct timeval*) malloc(sizeof(struct timeval));
  gettimeofday(tv, NULL);

  return tv;
}

struct rusage *get_current_resource_usage() {
  struct rusage *usg = (struct rusage*) malloc(sizeof(struct rusage));
  getrusage(RUSAGE_SELF, usg);

  return usg;
}

// TODO populate the given struct with starting information
void profile_start(struct profile_times *t) {
  // Logic of retrieving PID
  pid_t current_pid = getpid();
  t->curr_pid = current_pid;


  // Logic of retrieving time
  struct timeval *tv = get_current_time();
  t->start_real_time_sec = tv->tv_sec;
  t->start_real_time_microsec = tv->tv_usec;

  struct rusage *ru = get_current_resource_usage();
  t->start_user_ru_sec = ru->ru_utime.tv_sec;
  t->start_user_ru_microsec = ru->ru_utime.tv_usec;
  t->start_kernel_ru_sec = ru->ru_stime.tv_sec;
  t->start_kernel_ru_microsec = ru->ru_stime.tv_usec;

  free(tv);
  free(ru);
}

// TODO given starting information, compute and log differences to now
void profile_log(struct profile_times *t) {
  struct timeval *tv = get_current_time();
  t->end_real_time_sec = tv->tv_sec;
  t->end_real_time_microsec = tv->tv_usec;

  struct rusage *ru = get_current_resource_usage();
  t->end_user_ru_sec = ru->ru_utime.tv_sec;
  t->end_user_ru_microsec = ru->ru_utime.tv_usec;
  t->end_kernel_ru_sec = ru->ru_stime.tv_sec;
  t->end_kernel_ru_microsec = ru->ru_stime.tv_usec;

  time_t real_seconds_elapsed = t->end_real_time_sec - t->start_real_time_sec;
  suseconds_t real_microsec_elapsed = t->end_real_time_microsec - t->start_real_time_microsec;

  time_t user_seconds_elapsed = t->end_user_ru_sec - t->start_user_ru_sec;
  suseconds_t user_microseconds_elapsed = t->end_user_ru_microsec - t->start_user_ru_microsec;

  time_t kernel_seconds_elapsed = t->end_kernel_ru_sec - t->start_kernel_ru_sec;
  suseconds_t kernes_microseconds_elapsed = t->end_kernel_ru_microsec - t->start_kernel_ru_microsec;

  printf("[pid %d] real: %ld.%lds user: %ld.%lds kernel: %ld.%ld\n", t->curr_pid, real_seconds_elapsed, real_microsec_elapsed, user_seconds_elapsed, user_microseconds_elapsed, kernel_seconds_elapsed, kernes_microseconds_elapsed);
  free(tv);
  free(ru);
}

int main(int argc, char *argv[]) {
  struct profile_times t;

  // TODO profile doing a bunch of floating point muls
  float x = 1.0;
  profile_start(&t);
  for (int i = 0; i < NUM_MULS; i++)
    x *= 1.1;
  profile_log(&t);

  // TODO profile doing a bunch of mallocs
  profile_start(&t);
  void *p;
  for (int i = 0; i < NUM_MALLOCS; i++)
    p = malloc(MALLOC_SIZE);
  profile_log(&t);

  // TODO profile sleeping
  profile_start(&t);
  sleep(SLEEP_SEC);
  profile_log(&t);
}
