/*
 * ns_t1_pid.c
 *    search linux namespace
 *    https://www.toptal.com/linux/separation-anxiety-isolating-your-system-with-linux-namespaces
 */

#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

static char child_stack[1048576];

static int child_fn() {
  printf("My PID: %ld\n", (long)getpid());
  printf("Parent PID: %ld\n", (long)getppid());
  return 0;
}

int main() {
  pid_t child_pid = clone(child_fn, child_stack+1048576, CLONE_NEWPID | SIGCHLD, NULL);
  printf("clone() = %ld\n", (long)child_pid);

  waitpid(child_pid, NULL, 0);
  return 0;
}



