/*
 * showvm.cpp : scan system for process memory usage 
 *              verify data access speed
 */

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <fcntl.h>
#include <errno.h>
#include <assert.h>
#include <sys/ioctl.h>
#include <pthread.h>
#include <string>
#include <stdexcept>
#include <vector>

#include <sys/types.h>
#include <dirent.h>


using namespace std;

static int getPidComm(int tpid, char *obuf);
static int getPidHwmRss(int tpid, int sel);
static int getPidPss(int tpid);

static int verify_data_access(void);

int main(int argc, char *argv[])
{
    int mypid = getpid();

    DIR * dirp = opendir("/proc");
    if ( dirp == NULL ) {
        perror("cannot opendir /proc\n");
        return 1;
    }
    
    struct dirent *entp = NULL; 
    int hwmsum = 0, rsssum = 0, psssum = 0;
    
    printf("\n\n");
    printf("  header  %18s   %6s   %6s   %6s   %6s   %6s    %6s %6s\n\n", 
            "comm", "pid", "hwm", "rss", "hwmsum", "rsssum", "pss", "psssum");
                    
    /* all pids */
    do {
        entp = readdir(dirp);
        if ( entp != NULL ) {
            char fname[256], fcomm[256];
            unsigned ftype = DT_UNKNOWN;
            memset(fname,0,256); memset(fcomm,0,256);
            
            memcpy(fname, entp->d_name, 255);
            ftype = entp->d_type;
            
            if ( ftype == DT_DIR && fname[0] >= '0' && fname[0] <= '9' ) {
                int tpid = atol(fname);
                if ( tpid != mypid ) {
                    int hwm = getPidHwmRss(tpid, 0);
                    int rss = getPidHwmRss(tpid, 1);
                    int pss = getPidPss(tpid);
                    hwmsum += hwm;
                    rsssum += rss;
                    psssum += pss;
                    int rc = getPidComm(tpid, fcomm);
                    if ( rc != 0 ) {
                        memset(fcomm,0,256);
                    }
                    printf("  process %18s   %6d   %6d   %6d   %6d   %6d"
                            "    %6d %6d\n", 
                            fcomm, tpid, 
                            hwm/1000, rss/1000, hwmsum/1000, rsssum/1000, 
                            pss/1000, psssum/1000);
                }
            }
            
        }
    } while(entp != NULL);
    closedir(dirp);
    
    /* this pid */
    {
                    int hwm = getPidHwmRss(mypid, 0);
                    int rss = getPidHwmRss(mypid, 1);
                    int pss = getPidPss(mypid);
                    hwmsum += hwm;
                    rsssum += rss;
                    psssum += pss;
                    printf("\n");
                    printf("  myself  %18s   %6d   %6d   %6d   %6d   %6d"
                            "    %6d %6d\n\n", 
                            "showvm", mypid, 
                            hwm/1000, rss/1000, hwmsum/1000, rsssum/1000, 
                            pss/1000, psssum/1000);
    }
    
    if ( argc > 1 ) {
        int stime = atol(argv[1]);
        if ( stime < 0 || stime > 60 ) {
            stime = 10;
        }
        printf("  Sleep %d seconds\n", stime);
        sleep(stime);
    }
    printf("\n");
    verify_data_access();
    printf("\n");
    return 0;
}

static int getPidComm(int tpid, char *obuf)
{
    int rc = 1;
    char pbuf[256], rbuf[256];
    do {
        memset(pbuf, 0, 256);
        snprintf(pbuf,255,"/proc/%d/comm", tpid);
        memset(rbuf, 0, 256);
        snprintf(rbuf,255,"\ncannot open %s for reading\n", pbuf);
        FILE *fp = fopen(pbuf, "r");
        if ( fp == NULL ) {
            perror(rbuf);
            break;
        }
        for (int i=0; i<2; i++) {
            memset(rbuf, 0, 256);
            char * lp = fgets(rbuf, 255, fp);
            if ( lp == NULL ) break;
            if ( lp[0] != 0) {
                memcpy(obuf, rbuf, 255);
                for (int k=0; k<255; k++) {
                    if ( obuf[k] == '\n' || obuf[k] == '\r' ) {
                        obuf[k] = 0;
                        break;
                    }
                }
                rc = 0;
                break;
            } else {
                printf("  look for next line in %s\n", pbuf);
            }
        }
        fclose (fp);
    } while(0);
    return rc;
}

static int getPidHwmRss(int tpid, int sel)
{
    int rc = 0;
    char pbuf[256], rbuf[256];
    do {
        memset(pbuf, 0, 256);
        snprintf(pbuf,255,"/proc/%d/status", tpid);
        memset(rbuf, 0, 256);
        snprintf(rbuf,255,"\ncannot open %s for reading\n", pbuf);
        FILE *fp = fopen(pbuf, "r");
        if ( fp == NULL ) {
            perror(rbuf);
            break;
        }
        for (int i=0; i<200; i++) {
            memset(rbuf, 0, 256);
            char * lp = fgets(rbuf, 255, fp);
            if ( lp == NULL ) break;
            /*  VmHWM:      2536 kB
                VmRSS:      2536 kB
             */
            memset(pbuf,0,256);
            if ( sel == 0 ) snprintf(pbuf,255,"VmHWM:");
            else            snprintf(pbuf,255,"VmRSS:");
            if ( strncmp(rbuf, pbuf , 6) == 0 ) {
                char * tp = strtok(rbuf+6," \t");
                if ( tp == NULL) {
                    perror("\ntok 0 null in getPidHwmRss()\n"); 
                    break; 
                }
                if ( tp[0] < '0' || tp[0] > '9' ) {
                  perror("\ntok 0 not start with a number in getPidHwmRss()\n"); 
                    break; 
                }
                rc = atol(tp); 
                if ( rc ) {
                    tp = strtok(NULL," \t");
                    if ( tp == NULL) {
                        perror("\ntok 1 null in getPidHwmRss()\n"); 
                        break; 
                    }
                    if (strncmp("kB",tp,2) == 0) {
                        rc *= 1000; 
                    } else {
                        perror("\ntok 1 not kB in getPidHwmRss()\n"); 
                        break;
                    }
                }
            }
        }
        fclose (fp);
    } while(0);
    return rc;
}

static int getPidPss(int tpid)
{
    int rc = 0;
    char pbuf[256], rbuf[256];
    do {
        memset(pbuf, 0, 256);
        snprintf(pbuf,255,"/proc/%d/smaps", tpid);
        memset(rbuf, 0, 256);
        snprintf(rbuf,255,"\ncannot open %s for reading\n", pbuf);
        FILE *fp = fopen(pbuf, "r");
        if ( fp == NULL ) {
            perror(rbuf);
            break;
        }
        for (int i=0; i<600; i++) {
            memset(rbuf, 0, 256);
            char * lp = fgets(rbuf, 255, fp);
            if ( lp == NULL ) break;
            /*  Pss:      2536 kB
             */
            memset(pbuf,0,256);
            snprintf(pbuf,255,"Pss:");
            if ( strncmp(rbuf, pbuf , 4) == 0 ) {
                char * tp = strtok(rbuf+4," \t");
                if ( tp == NULL) {
                    perror("\ntok 0 null in getPidPss()\n");
                    continue;
                }
                if ( tp[0] < '0' || tp[0] > '9' ) {
                    perror("\ntok 0 not start with a number in getPidPss()\n"); 
                    break; 
                }
                int pssline = atol(tp); 
                if ( pssline ) {
                    tp = strtok(NULL," \t");
                    if ( tp == NULL) {
                        perror("\ntok 2 null in getPidPss()\n");
                        continue;
                    }
                    if (strncmp("kB",tp,2) == 0) {
                        pssline *= 1000;
                    } else {
                        perror("\ntok 2 not kB in getPidPss()\n");
                        continue;
                    }
                }
                rc += pssline;
            }
        }
        fclose (fp);
    } while(0);
    return rc;
}


/* 
 *  * L1 Instruction and Data Cache of 32KB, 4-way, 16-word line with 
 *    128-bit interface.
 *  * Integrated L2 cache of 256 KB, 8-way, 16 word line, 128 bit interface 
 *     to L1 along with ECC/Parity supporte
 */

/* L1 cache verify */

static const unsigned int L1Words = 16; 

#define TESTSET (3)
#if TESTSET==(1)
  static const unsigned int L1Size = 32768; /* 32k */
  static const unsigned int L1Ways = 4;
  /* result triple-loop triple-trashing: 3ms */
  static const unsigned int L1Blk = L1Size/2; /* copy a block to another block */
#elif TESTSET==(2)
  static const unsigned int L1Size = 256 * 1024 ; /* 256k */
  static const unsigned int L1Ways = 8;
  static const unsigned int L1Blk = L1Size/2; /* copy a block to another block */
  /* result: 54 64 */
#elif TESTSET==(3)
  static const unsigned int L1Size = 512 * 1024 ; /* double L2 size */
  static const unsigned int L1Ways = 16;          /* double ways */
  /* result: 205 725  total 8M blk 256k */
  static const unsigned int L1Blk = L1Size/2; /* copy a block to another block */
  static const unsigned int L1Lines = L1Size / (L1Ways/2) / L1Words;
#elif TESTSET==(4)
  static const unsigned int L1Size = 256 * 1024 ; /* L2 size */
  static const unsigned int L1Ways = 16;          /* double ways */
  /* result: 26 215 */
  static const unsigned int L1Lines = L1Size / (L1Ways/2) / L1Words;
  static const unsigned int L1Blk = L1Lines * L1Words; /* copy a block to another block */
#elif TESTSET==(5)
  static const unsigned int L1Size = 256 * 1024 ; /* L2 size */
  static const unsigned int L1Ways = 8;           /* ways */
  /* result: 13 16  total data 512k */
  static const unsigned int L1Lines = L1Size / (L1Ways) / L1Words;
  static const unsigned int L1Blk = L1Lines * L1Words; /* copy a block to another block */
#elif TESTSET==(6)
  static const unsigned int L1Size = 256 * 1024 ; /* L2 size */
  static const unsigned int L1Ways = 8;           /* ways */
  /* result: 26 32  total data 1024k */
  static const unsigned int L1Lines = L1Size / (L1Ways/2) / L1Words;
  static const unsigned int L1Blk = L1Lines * L1Words; /* copy a block to another block */
#else
  #error unknown test set
#endif


struct data_block_s {
    unsigned char data_src[L1Blk];
    unsigned char data_dest[L1Blk];
};

extern struct data_block_s data[L1Ways];
struct data_block_s data[L1Ways];

#include <sys/time.h>

static int verify_data_access1() {
    /* touch data[0] so it gets into cache */
    memset(&data[0], 0, sizeof(data[0]));
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data);
    
    struct timeval tm1 = {0,0};
    struct timeval tm2 = {0,0};
    
    /* copy block and keep track the time cost */
    gettimeofday(&tm1, NULL);
    memcpy( &(data[0].data_dest[0]), &(data[0].data_src[0]), L1Blk);
    gettimeofday(&tm2, NULL);
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data); 
    
    unsigned int tmcost = 0;
    if ( tm2.tv_sec > tm1.tv_sec ) {
        tmcost = tm2.tv_sec - tm1.tv_sec;
        tmcost *= 1000000; /* us */
    }
    tmcost += tm2.tv_usec;
    tmcost -= tm1.tv_usec;
    printf("\n %s \n", __func__);
    printf("   time cost us : %03u %03u %03u \n\n", 
            tmcost/1000000, (tmcost/1000) % 1000, tmcost% 1000);
    return 0;
}

/* repeat on same data block [0] */
static int verify_data_access2() {
  unsigned int tmcosts[L1Ways] = {0};
  
  for (int k=0; k<L1Ways; k++) {
    /* touch data[0] so it gets into cache */
    memset(&data[0], 0, sizeof(data[0]));
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data);
    
    struct timeval tm1 = {0,0};
    struct timeval tm2 = {0,0};
    
    /* copy block and keep track the time cost */
    gettimeofday(&tm1, NULL);
    memcpy( &(data[0].data_dest[0]), &(data[0].data_src[0]), L1Blk);
    gettimeofday(&tm2, NULL);
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data); 
    
    unsigned int tmcost = 0;
    if ( tm2.tv_sec > tm1.tv_sec ) {
        tmcost = tm2.tv_sec - tm1.tv_sec;
        tmcost *= 1000000; /* us */
    }
    tmcost += tm2.tv_usec;
    tmcost -= tm1.tv_usec;
    tmcosts[k] = tmcost;
  }
    printf("\n %s \n", __func__);
  for (int k=0; k<L1Ways; k++) {
    unsigned int tmcost = tmcosts[k];
    printf("   time cost us : %03u %03u %03u  k %u\n\n", 
            tmcost/1000000, (tmcost/1000) % 1000, tmcost% 1000, k);
  }
    return 0;
}

/* iterate through data block [k] */
static int verify_data_access3() {
  unsigned int tmcosts[L1Ways] = {0};
  
  for (int k=0; k<L1Ways; k++) {
    /* touch data[0] so it gets into cache */
    memset(&data[k], 0, sizeof(data[k]));
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data);
    
    struct timeval tm1 = {0,0};
    struct timeval tm2 = {0,0};
    
    /* copy block and keep track the time cost */
    gettimeofday(&tm1, NULL);
    /* ******** this line is changed from last test ******** */
    memcpy( &(data[k].data_dest[0]), &(data[0].data_src[k]), L1Blk);
    gettimeofday(&tm2, NULL);
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data); 
    
    unsigned int tmcost = 0;
    if ( tm2.tv_sec > tm1.tv_sec ) {
        tmcost = tm2.tv_sec - tm1.tv_sec;
        tmcost *= 1000000; /* us */
    }
    tmcost += tm2.tv_usec;
    tmcost -= tm1.tv_usec;
    tmcosts[k] = tmcost;
  }
    printf("\n %s \n", __func__);
  for (int k=0; k<L1Ways; k++) {
    unsigned int tmcost = tmcosts[k];
    printf("   time cost us : %03u %03u %03u  k %u\n\n", 
            tmcost/1000000, (tmcost/1000) % 1000, tmcost% 1000, k);
  }
    return 0;
}

/* for loop copy byte by byte ... */
static int verify_data_access11() {
  unsigned int tmcosts[L1Ways] = {0};
  
  for (int k=0; k<L1Ways; k++) {
    /* touch data[0] so it gets into cache */
    memset(&data[k], 0, sizeof(data[k]));
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data);
    
    struct timeval tm1 = {0,0};
    struct timeval tm2 = {0,0};
    
    /* copy block and keep track the time cost */
    gettimeofday(&tm1, NULL);
    for (unsigned int b = 0; b<L1Blk; b++) {
        data[k].data_dest[b] = data[k].data_src[b];
    }
    gettimeofday(&tm2, NULL);
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data); 
    
    unsigned int tmcost = 0;
    if ( tm2.tv_sec > tm1.tv_sec ) {
        tmcost = tm2.tv_sec - tm1.tv_sec;
        tmcost *= 1000000; /* us */
    }
    tmcost += tm2.tv_usec;
    tmcost -= tm1.tv_usec;
    tmcosts[k] = tmcost;
  }
    printf("\n %s \n", __func__);
  for (int k=0; k<L1Ways; k++) {
    unsigned int tmcost = tmcosts[k];
    printf("   time cost us : %03u %03u %03u  k %u\n\n", 
            tmcost/1000000, (tmcost/1000) % 1000, tmcost% 1000, k);
  }
    return 0;
}

/* do not touch data block [k] */
static int verify_data_access12() {
  unsigned int tmcosts[L1Ways] = {0};
  
 for (int k=0; k<L1Ways; k++) {
    /* touch data[0] so it gets into cache */
    //memset(&data[k], 0, sizeof(data[k]));
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data);
    
    struct timeval tm1 = {0,0};
    struct timeval tm2 = {0,0};
    
    /* copy block and keep track the time cost */
    gettimeofday(&tm1, NULL);
    for (unsigned int b = 0; b<L1Blk; b++) {
        data[k].data_dest[b] = data[k].data_src[b];
    }
    gettimeofday(&tm2, NULL);
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data); 
    
    unsigned int tmcost = 0;
    if ( tm2.tv_sec > tm1.tv_sec ) {
        tmcost = tm2.tv_sec - tm1.tv_sec;
        tmcost *= 1000000; /* us */
    }
    tmcost += tm2.tv_usec;
    tmcost -= tm1.tv_usec;
    tmcosts[k] = tmcost;
  }
    printf("\n %s \n", __func__);
  for (int k=0; k<L1Ways; k++) {
    unsigned int tmcost = tmcosts[k];
    printf("   time cost us : %03u %03u %03u  k %u\n\n", 
            tmcost/1000000, (tmcost/1000) % 1000, tmcost% 1000, k);
  }
    return 0;
}

/* double loop */
static int verify_data_access21_double_loop() {
    
  unsigned int tmcosts[L1Ways] = {0};
  
  for (int k=0; k<L1Ways; k++) {
    /* touch data[0] so it gets into cache */
    //memset(&data[k], 0, sizeof(data[k]));
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data);
    
    struct timeval tm1 = {0,0};
    struct timeval tm2 = {0,0};
    
    /* copy block and keep track the time cost */
    gettimeofday(&tm1, NULL);
    for (int i=0; i<L1Blk; i+= L1Words) {
     for (int j=0; j<L1Words; j++) {
        int b = i+j;
        data[k].data_dest[b] = data[k].data_src[b];
     }
    }
    gettimeofday(&tm2, NULL);
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data); 
    
    unsigned int tmcost = 0;
    if ( tm2.tv_sec > tm1.tv_sec ) {
        tmcost = tm2.tv_sec - tm1.tv_sec;
        tmcost *= 1000000; /* us */
    }
    tmcost += tm2.tv_usec;
    tmcost -= tm1.tv_usec;
    tmcosts[k] = tmcost;
  }
    printf("\n %s \n", __func__);
    unsigned int costtotal = 0;
  for (int k=0; k<L1Ways; k++) {
    unsigned int tmcost = tmcosts[k];
    costtotal += tmcost;
    printf("   time cost us : %03u %03u %03u  k %u\n\n", 
            tmcost/1000000, (tmcost/1000) % 1000, tmcost% 1000, k);
  }
    printf("   time cost us : %03u %03u %03u  total\n\n", 
            costtotal/1000000, (costtotal/1000) % 1000, costtotal% 1000);
    return 0;
}

/* triple loop */
static int verify_data_access22_triple_loop() {
    
    struct timeval tm1 = {0,0};
    struct timeval tm2 = {0,0};
    
    /* copy block and keep track the time cost */
    gettimeofday(&tm1, NULL);
  for (int k=0; k<L1Ways; k++) {
    for (int i=0; i<L1Blk; i+= L1Words) {
     for (int j=0; j<L1Words; j++) {
        int b = i+j;
        data[k].data_dest[b] = data[k].data_src[b];
     }
    }
  }
    gettimeofday(&tm2, NULL);
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data); 
    
    unsigned int tmcost = 0;
    if ( tm2.tv_sec > tm1.tv_sec ) {
        tmcost = tm2.tv_sec - tm1.tv_sec;
        tmcost *= 1000000; /* us */
    }
    tmcost += tm2.tv_usec;
    tmcost -= tm1.tv_usec;
    printf("\n %s \n", __func__);
    printf("   time cost us : %03u %03u %03u  \n\n", 
            tmcost/1000000, (tmcost/1000) % 1000, tmcost% 1000);
    return 0;
}

/* triple loop trashing */
static int verify_data_access23_triple_trashing() {
    
    struct timeval tm1 = {0,0};
    struct timeval tm2 = {0,0};
    
    /* copy block and keep track the time cost */
    gettimeofday(&tm1, NULL);
    for (int i=0; i<L1Blk; i+= L1Words) {
     for (int j=0; j<L1Words; j++) {
        int b = i+j;
      for (int k=0; k<L1Ways; k++) {
        data[k].data_dest[b] = data[k].data_src[b];
      }
     }
    }
    gettimeofday(&tm2, NULL);
    
    /* pass data to an external function so to hint the compiler that 
     * the data could be changed. this may not work though. 
     */
    printf("\n %p \n", &data); 
    
    unsigned int tmcost = 0;
    if ( tm2.tv_sec > tm1.tv_sec ) {
        tmcost = tm2.tv_sec - tm1.tv_sec;
        tmcost *= 1000000; /* us */
    }
    tmcost += tm2.tv_usec;
    tmcost -= tm1.tv_usec;
    printf("\n %s \n", __func__);
    printf("   time cost us : %03u %03u %03u  \n\n", 
            tmcost/1000000, (tmcost/1000) % 1000, tmcost% 1000);
    return 0;
}

static int verify_data_access() {
    int rc1 = verify_data_access1(); /* data and code cache */
    int rc2 = verify_data_access2(); /* code cache */
    int rc3 = verify_data_access3();
    int rc11 = verify_data_access11();
    int rc12 = verify_data_access12();
    int rc21 = verify_data_access21_double_loop();
    int rc22 = verify_data_access22_triple_loop(); /* code cache */
    int rc23 = verify_data_access23_triple_trashing();
    printf("\n TESTSET %d  data total %u  lines %u  blk %u\n", 
           TESTSET, sizeof(data), L1Lines, L1Blk);
    return rc1 | rc2 | rc3 | rc11 | rc12 | rc21 | rc22 | rc23 ;
}

/* testset 3 result:
 verify_data_access1
   time cost us : 000 001 068

 verify_data_access2
   time cost us : 000 000 976  k 0
   time cost us : 000 001 038  k 1
   time cost us : 000 001 007  k 2
   time cost us : 000 001 007  k 3
   time cost us : 000 000 976  k 4
   time cost us : 000 001 037  k 5
   time cost us : 000 001 068  k 6
   time cost us : 000 001 099  k 7
   time cost us : 000 001 007  k 8
   time cost us : 000 001 130  k 9
   time cost us : 000 001 007  k 10
   time cost us : 000 000 977  k 11
   time cost us : 000 000 976  k 12
   time cost us : 000 001 038  k 13
   time cost us : 000 001 007  k 14
   time cost us : 000 000 976  k 15

 verify_data_access3
   time cost us : 000 000 977  k 0
   time cost us : 000 000 855  k 1
   time cost us : 000 001 007  k 2
   time cost us : 000 000 946  k 3
   time cost us : 000 000 976  k 4
   time cost us : 000 000 977  k 5
   time cost us : 000 000 915  k 6
   time cost us : 000 000 946  k 7
   time cost us : 000 000 946  k 8
   time cost us : 000 000 915  k 9
   time cost us : 000 000 946  k 10
   time cost us : 000 000 946  k 11
   time cost us : 000 001 007  k 12
   time cost us : 000 000 976  k 13
   time cost us : 000 000 946  k 14
   time cost us : 000 000 946  k 15

 verify_data_access11
   time cost us : 000 010 834  k 0
   time cost us : 000 010 956  k 1
   time cost us : 000 010 956  k 2
   time cost us : 000 010 955  k 3
   time cost us : 000 010 925  k 4
   time cost us : 000 010 926  k 5
   time cost us : 000 010 955  k 6
   time cost us : 000 010 956  k 7
   time cost us : 000 010 956  k 8
   time cost us : 000 011 078  k 9
   time cost us : 000 010 956  k 10
   time cost us : 000 010 956  k 11
   time cost us : 000 010 987  k 12
   time cost us : 000 010 956  k 13
   time cost us : 000 010 956  k 14
   time cost us : 000 010 956  k 15

 verify_data_access12
   time cost us : 000 010 926  k 0
   time cost us : 000 010 956  k 1
   time cost us : 000 010 926  k 2
   time cost us : 000 010 987  k 3
   time cost us : 000 010 956  k 4
   time cost us : 000 010 956  k 5
   time cost us : 000 010 925  k 6
   time cost us : 000 010 925  k 7
   time cost us : 000 010 956  k 8
   time cost us : 000 010 956  k 9
   time cost us : 000 010 955  k 10
   time cost us : 000 011 047  k 11
   time cost us : 000 010 986  k 12
   time cost us : 000 011 078  k 13
   time cost us : 000 010 987  k 14
   time cost us : 000 010 986  k 15

 verify_data_access21_double_loop
   time cost us : 000 012 909  k 0
   time cost us : 000 012 909  k 1
   time cost us : 000 012 940  k 2
   time cost us : 000 012 939  k 3
   time cost us : 000 012 909  k 4
   time cost us : 000 012 939  k 5
   time cost us : 000 012 909  k 6
   time cost us : 000 012 940  k 7
   time cost us : 000 012 939  k 8
   time cost us : 000 012 909  k 9
   time cost us : 000 013 001  k 10
   time cost us : 000 012 940  k 11
   time cost us : 000 012 970  k 12
   time cost us : 000 013 001  k 13
   time cost us : 000 012 970  k 14
   time cost us : 000 012 970  k 15
                                           time cost us : 000 207 094  total

 verify_data_access22_triple_loop          time cost us : 000 205 566
 verify_data_access23_triple_trashing      time cost us : 000 655 731

 TESTSET 3
 
 */


