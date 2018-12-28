/*
 * test.c
 */

volatile unsigned char * sigptr = (unsigned char *)0xffffffc0;
volatile int cumuloops = 3;

int main() {
    unsigned char v = 0x59;
    cumuloops += v;
    *sigptr = v;
    return cumuloops;
}


