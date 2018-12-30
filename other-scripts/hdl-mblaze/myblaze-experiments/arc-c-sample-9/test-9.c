/*
 * test.c
 */

volatile unsigned char * uart_tx_send_ptr = (unsigned char *)0xffffffc0; /* send char to uart */
volatile unsigned int  * uart_tx_busy_ptr = (unsigned int  *)0xffffffa0; /* read status back */

unsigned int uart_tx_busy = 1;
unsigned int uart_tx_done = 1;
int cumuloops = 3;

int main() {
    int k, w;
    unsigned char v = 0x41; /* 'A' */
    for (k=0; k<4; k++) {
      cumuloops += k;
      *uart_tx_send_ptr = (unsigned char)(v+k);
      uart_tx_done = 0;
      for (w=0; w<20; w++) { /* wait up to 20 loops */
          uart_tx_busy = *uart_tx_busy_ptr;
          if ((uart_tx_busy & 1) == 0) {
              uart_tx_done = 1;
              break;
          }
      }
    }
    return cumuloops;
}


