/*
 * test.c
 */

unsigned int * sigptr = (unsigned int *)0xffffffc0;
unsigned int i = 0;
unsigned int j = 0;
int cumuloops = 0;

int main() {
    register int a = 0;
    for (i=0; i<10; i++) {
        for (j=0; j<4; j++) {
            a ++;
        }
        *sigptr = i;
        cumuloops ++;
    }
    return cumuloops + a;
}


