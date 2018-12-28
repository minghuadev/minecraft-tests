/*
 * test.c
 */

volatile unsigned char * sigptr = (unsigned char *)0xffffffc0;
volatile int cumuloops = 3;

int subf();

int main() {
    int k;
    unsigned char v = 0x41;
    for (k=0; k<4; k++) {
      cumuloops += k;
      *sigptr = (unsigned char)(v+k);
    }
    k = subf();
    return cumuloops;
}

int subf() { return 55; }

