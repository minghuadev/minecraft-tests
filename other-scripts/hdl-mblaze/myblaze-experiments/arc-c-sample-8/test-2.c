/*
 * test.c
 */

unsigned int * sigptr = 0;
int main() {
    int cumuloops = 0;
    unsigned int i;
    sigptr = (unsigned int *)0xffffffc0;
    for (i=0; i<10; i++) {
        unsigned int j;
        for (j=0; j<10; j++) {
            cumuloops ++;
        }
        *sigptr = i;
    }
    return cumuloops;
}


