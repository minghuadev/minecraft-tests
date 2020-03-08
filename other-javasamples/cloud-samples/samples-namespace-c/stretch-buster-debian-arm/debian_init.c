/*
 * debian_init.c
 * to compile:
 *    arm-<vendor>-linux-gcc -DDS=9$(date +%m%d%H%M) debian_init.c --static
 */

#define EXT_DIR_PATH "/root/extapps"
#define EXT_CONTAINER_PATH "/root/debian_layer"
#define EXT_CONTAINER_PARENT "root-debian-parent" /* under container */

#define _GNU_SOURCE /* for pivot_root and pid namespace */
#include <stdio.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <string.h>

#define ARGONE_SZ (64)
#define ARGS_MAX (9)
#define CMDS_MAX (20)

struct argone_s {
    char arg[ARGONE_SZ];
};

struct args_s {
    int bg;
    int replace;
    struct argone_s argx[ARGS_MAX];
};

struct args_s cmds1[CMDS_MAX] = {
    { 0, 0, {"lib/arm-linux-gnueabihf/ld-2.24.so", "/bin/bash", "-c", "pwd", ""} },
#if 1
    { 0, 1, {"lib/arm-linux-gnueabihf/ld-2.24.so", "/bin/bash", ""} },
#endif

    { 0, 0, {""} }
};

typedef char * argsbuf_t[ARGS_MAX];
#define DEBUG_RUN_CMD (1)

int run_cmd(int replace, int argbg, argsbuf_t *argsbuf) {
    pid_t cpid = 0;
    //replace = 0; /* 0 to force always child exec, no replace */
    if (replace == 0) {
        cpid = fork();
    }
    if (cpid == 0) { /* child, or parent when replace */
#if defined(DEBUG_RUN_CMD) && (DEBUG_RUN_CMD) /* debug */
        int i = 0;
        printf("    child %d or parent-when-replace \n", cpid);
        printf("    child cmd ");
        for (i = 0; i < ARGS_MAX; i++) {
            if ((*argsbuf)[i] == NULL) {
                break;
            }
            int argn = strnlen((*argsbuf)[i], ARGONE_SZ);
            if (argn > 0 && argn < ARGONE_SZ - 1) {
                printf(" %s ", (*argsbuf)[i]);
            }
        }
        printf("  bg=%d replace=%d\n", argbg, replace);
#endif
        char arg0[ARGONE_SZ];
        memset(arg0, 0, sizeof (arg0));
        strncpy(arg0, (*argsbuf)[0], sizeof (arg0) - 1);
        int re = execv(arg0, (*argsbuf));
        if (re != 0) {
            printf("    child execv error %d. cmd %s\n", re, (*argsbuf)[0]);
            exit(1); /* error. ??? how this propagate back ??? */
        } else {
            ;
#if defined(DEBUG_RUN_CMD) && (DEBUG_RUN_CMD) /* debug */
            printf("    child execv ok. cmd %s\n", re, (*argsbuf)[0]);
#endif
        }
        exit(0);
    } else { /* parent */
        int cfg_always_wait = 0; /* set to 1 to force no bg */
        if (argbg == 0 || cfg_always_wait) {
            int status = 0;
            pid_t rw = waitpid(cpid, &status, 0);
#if defined(DEBUG_RUN_CMD) && (DEBUG_RUN_CMD) /* debug */
            printf("    parent returned %d for pid %d\n", rw, cpid);
#endif
            if (rw < 1) {
                return 1; /* error */
            }
        } else {
            ;
#if defined(DEBUG_RUN_CMD) && (DEBUG_RUN_CMD) /* debug */
            printf("    parent left child pid %d\n", cpid);
#endif
        }
    }
    return 0; /* ok */
}

static int run_cmd_list()
{
    int rc;
    int err_found = 0;
    int i;

    for (i = 0; i < CMDS_MAX; i++) {
        if (err_found) {
            break;
        }
#if 1 /* workaround */
        if ( cmds1[i].bg == 2 ) { /* 2: special flag to wait 10ms */
            usleep(10 * 1000);
            continue;
        }
#endif
        if (strnlen(cmds1[i].argx[0].arg, ARGONE_SZ) < 1) {
            break;
        }
        struct args_s cmdbuf;
        argsbuf_t argsbuf_inst;
        memset(&cmdbuf, 0, sizeof (cmdbuf));
        memset(&argsbuf_inst, 0, sizeof (argsbuf_inst));
        int rp1 = snprintf(cmdbuf.argx[0].arg, ARGONE_SZ - 1, 
                                                "%s", cmds1[i].argx[0].arg);
        int rp2 = snprintf(cmdbuf.argx[1].arg, ARGONE_SZ - 1, 
                                                "%s", cmds1[i].argx[1].arg);
        if (rp1 < 0 || rp1 >= ARGONE_SZ - 1 || rp2 < 0 || rp2 >= ARGONE_SZ - 1){
            err_found = 1;
            break;
        }
        argsbuf_inst[0] = cmdbuf.argx[0].arg;
        argsbuf_inst[1] = cmdbuf.argx[1].arg;
        int j;
        int found_ending = 0;
        for (j = 2; j < ARGS_MAX - 1; j++) {
            if (strnlen(cmds1[i].argx[j].arg, ARGONE_SZ) < 1) {
                found_ending = 1;
                break;
            }
            strncpy(cmdbuf.argx[j].arg, cmds1[i].argx[j].arg, ARGONE_SZ);
            argsbuf_inst[j] = cmdbuf.argx[j].arg;
        }
        if (found_ending == 0) {
            err_found = 1;
            break;
        }
        int argbg = cmds1[i].bg;
        int replace = cmds1[i].replace;
        int rp = run_cmd(replace, argbg, &argsbuf_inst);
        if (rp != 0) {
            err_found = 1;
            break;
        }
    }
    
    return rc;
}

extern int run_pivotal(void); /* defined later */
extern int main_ns_clone(void);
int main(int argc, char *argv[]) {
    int cnt = 0;
    struct timeval tv1 = {0, 0};
    int rc = gettimeofday(&tv1, NULL);
#if defined(DS) 
    printf("\nbuild ds %d\n", DS);
#else
    printf("\nbuild ds %s\n", "unknown");
#endif
    printf("\ndebian_init gettimeofday %d %d.%06d\n", tv1.tv_sec, tv1.tv_usec);
    unsigned int tm0 = tv1.tv_sec * 1000 + tv1.tv_usec / 1000;

    pid_t mypid = getpid();
    printf("\ndebian_init mypid %d\n", mypid);

    int err_found = 0;
    int i;

    do {/* scope */
        if (mypid != 1) { 
            break;
        }
    } while(0);
    
    do {/* scope */ 
        int rpvt = run_pivotal();
        if ( rpvt != 0 ) {
            err_found = 1;
            printf("\ndebian_init   pivotal failed\n");
            break;
        }
        printf("\ndebian_init   pivotal succeeded\n");
    } while(0);
    
    struct timeval tv2 = {0, 0};
    gettimeofday(&tv2, NULL);
    printf("\ndebian_init    mounted %d.%06d\n", tv2.tv_sec, tv2.tv_usec);

    /* run commands */
    do {
        int rc_ns = main_ns_clone();
        (void)rc_ns;/*TODO: check rc_ns */
    } while(0);

    struct timeval tv3 = {0, 0};
    unsigned int tm1 = 0;
    if ( argc < 2 ) { /* if any command line argument will not start user app */
        struct args_s cmdbuf;
        argsbuf_t argsbuf_inst;
        int rc = gettimeofday(&tv3, NULL);
        tm1 = tv3.tv_sec * 1000 + tv3.tv_usec / 1000;
        printf("debian_init user app to start    %d.%06d  ms %u\n",
                tv3.tv_sec, tv3.tv_usec, tm1 - tm0);

        memset(&cmdbuf, 0, sizeof (cmdbuf));
        memset(&argsbuf_inst, 0, sizeof (argsbuf_inst));
        int rp1 = snprintf(cmdbuf.argx[0].arg, ARGONE_SZ - 1, 
                                                    EXT_DIR_PATH "/userapp");
        if (rp1 < 0 || rp1 >= ARGONE_SZ - 1) {
            err_found = 1;
        }
        argsbuf_inst[0] = cmdbuf.argx[0].arg;
        argsbuf_inst[1] = NULL;
        int argbg = 1; /* user app /root/extapps/userapp runs in background */
        int replace = 0;
        int rp = run_cmd(replace, /* ??? if pass 1 in, cannot return ??? */
                         argbg, &argsbuf_inst); 
        if (rp != 0) {
            err_found = 1;
        }
    }
    
    /* sleep 1 to allow the user app fully load */
    sleep(1);

#if 0
    /* log file open */
    FILE *logfp = fopen(EXT_DIR_PATH "/logrun_debian_init", "a");
    if (logfp) {
        fprintf(logfp, "debian_init               tv1 %d.%06d\n", 
                tv1.tv_sec, tv1.tv_usec);
        fprintf(logfp, "debian_init           mounted %d.%06d\n", 
                tv2.tv_sec, tv2.tv_usec);
        fprintf(logfp, "debian_init user app to start %d.%06d  ms %u\n", 
                tv3.tv_sec, tv3.tv_usec, tm1 - tm0);
    }

    if (err_found) {
        printf("debian_init err_found %d\n", err_found);
        if (logfp) {
            fprintf(logfp, "debian_init err_found %d\n", err_found);
        }
    }

    /* log file close */
    if (logfp) {
        fclose(logfp);
        logfp = NULL;
    }
    
#if 0
    /* from /etc/inittab: 
     * # Example of how to put a getty on a serial line (for a terminal)
     * ::respawn:/sbin/getty -L ttyS000 115200 vt100 -n root -I "Auto login as root ..."
     */
    if (argc < 2) {
        for (cnt = 0; cnt < 5; cnt++) {
            printf("\ndebian_init   running getty\n");
            run_sh_cmd("/sbin/getty -L ttyS000 115200 vt100 -n root -I \"Auto in..\"");
            printf("\ndebian_init   running getty returned\n");
        }
    }
#endif
#endif
    
    printf("debian_init user app all done\n");
    return 0;
}

/* ######################################################## */
/* pid namespace */

//#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

static char child_stack[1048576];

static int child_fn() {
  printf("PID: %ld\n", (long)getpid());
  printf("Parent PID: %ld\n", (long)getppid());
  int rc_cmd = run_cmd_list();
  return rc_cmd;
}

int main_ns_clone() {
  pid_t child_pid = clone(child_fn, child_stack+1048576, CLONE_NEWPID | SIGCHLD, NULL);
  printf("clone() = %ld\n", (long)child_pid);

  waitpid(child_pid, NULL, 0);
  return 0;
}

/* ######################################################## */
/* pivot_root */

//#define _GNU_SOURCE         /* See feature_test_macros(7) */
#include <unistd.h>
#include <sys/syscall.h>   /* For SYS_xxx definitions */

#define pivot_root(new_root,put_old) syscall(SYS_pivot_root,new_root,put_old)

int run_pivotal()
{
    int rc = 0; /* default success */
    do {
        rc = chdir(EXT_CONTAINER_PATH);
        if ( rc ) {
            perror(" failed chdir ");
            rc = 1;
            break;
        }
        rc = pivot_root(".", EXT_CONTAINER_PARENT);
        if ( rc ) {
            perror(" failed pivot_root ");
            rc = 1;
            break;
        }
    } while(0);
    return rc;
}

/* ######################################################## */


