/*
 * ns_t32_mount.c
 *    search linux create new mount namespace
 *    https://lwn.net/Articles/689856/ Mount namespaces and shared subtrees
 *            mount -n -o remount,defaults /dev/sda1 /
 *    https://unix.stackexchange.com/questions/464033/understanding-how-mount-namespaces-work-in-linux
 *    https://unix.stackexchange.com/questions/456620/how-to-perform-chroot-with-linux-namespaces
 */

#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>


static char child_stack[1048576];

static int child_fn() {
  printf("New `mount` Namespace:\n");
  system("ls /etc/");
  printf("\n\n");
  /* system("mount -n -o remount,defaults /dev/sda1 /etc"); */
  system("mount --make-rslave /");
  system("mount -n -o bind ./newetc /etc");
  system("ls /etc/");
  printf("\n\n");
  return 0;
}

int main() {
  printf("Original `mount` Namespace:\n");
  system("ls /etc/");
  printf("\n\n");

  pid_t child_pid = clone(child_fn, child_stack+1048576, CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWNS | SIGCHLD, NULL);

  waitpid(child_pid, NULL, 0);
  return 0;
}


