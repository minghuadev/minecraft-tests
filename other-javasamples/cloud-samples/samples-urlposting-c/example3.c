/*
 * example3.c
 */

#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit, atoi, malloc, free */
#include <unistd.h> /* read, write, close */
#include <string.h> /* memcpy, memset */
#include <sys/socket.h> /* socket, connect */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */

#include <stdlib.h>    /* malloc */

int main(int argc,char *argv[])
{
    int i, rc;
    rc = 0; /* default success */

    if (argc < 4) { puts("ERROR Parameters: <host> <port> <seqn>"); exit(1); }
    if ( strnlen(argv[1], 255) < 1 ) { puts("ERROR Argv[1]: <host> "); exit(1);}
    if ( strnlen(argv[2], 255) < 1 ) { puts("ERROR Argv[2]: <port> "); exit(1);}
    if ( strnlen(argv[3], 255) < 1 ) { puts("ERROR Argv[3]: <seqn> "); exit(1);}

    /* argv[1]: host */
    char *host = argv[1];

    /* argv[2]: port */
    long arg_port = strtol(argv[2], NULL, 10);
    if ( arg_port > 65535 || arg_port < 1 ) { puts("ERROR <port> out of range "); exit(1);}
    int portno = (int)arg_port;

    /* argv[3]: seqn */
    char arg_url_path[256];

    memset(arg_url_path, 0, sizeof(arg_url_path));

    rc = snprintf(arg_url_path, 255, "/upload/%s", argv[3]);
    if ( rc < 0 ) { perror("ERROR /upload/path failed"); exit(1); }
    else if ( rc >= 255 ) { puts("ERROR /upload/path failed truncated"); exit(1); }

    char *message;
    unsigned int message_size;

    char arg_url_method[] = "GET";

    /* How big is the message? */
    message_size = 0;

    message_size += strnlen("%s %s HTTP/1.0\r\n", 255);     /* request line */
    message_size += strnlen(arg_url_method, 255);           /* method         */
    message_size += strnlen(arg_url_path, 255);             /* path           */
    message_size += strlen("\r\n");                         /* blank line     */

    printf("ok: port %d host %s data %u\n", portno, host, message_size);

    /* allocate space for the message */
    message = malloc(message_size);
    if ( message == NULL ) { perror("ERROR malloc failed for data"); exit(1); }
    message[message_size - 1] = 0;

    /* fill in the parameters */
    unsigned int consumed_size = 0;
    int failed = 0;
    do {
        rc = snprintf(message, message_size - 1, "%s %s HTTP/1.0\r\n\r\n", arg_url_method, arg_url_path);
                                                            /* method, path   */
        if ( rc < 1 || rc >= message_size - 2 ) { failed = 1; break; }
        consumed_size += rc;
        if ( consumed_size >= message_size - 1 ) { failed = 2; break; }
        if ( failed ) break;
    }while(0);
    if ( failed ) {
        puts("ERROR http header construction failed"); free(message); exit(1);
    }

    /* What are we going to send? */
    printf("Request header:\n%s\n",message);

    if ( consumed_size > message_size ) {
        puts("ERROR http content construction failed truncated"); free(message); exit(1);
    }
    printf("Request data size %u\n", consumed_size);

    struct hostent *server;
    struct sockaddr_in serv_addr;
    int sockfd;
    char response[4096];
    do {
        /* create the socket */
        sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if (sockfd < 0) { perror("ERROR opening socket"); sockfd = 0; failed = 1; break; }

        /* lookup the ip address */
        server = gethostbyname(host);
        if (server == NULL) { perror("ERROR, no such host"); failed = 1; break; }

        /* fill in the structure */
        memset(&serv_addr,0,sizeof(serv_addr));
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(portno);
        memcpy(&serv_addr.sin_addr.s_addr,server->h_addr,server->h_length);

        /* connect the socket */
        if (connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr)) < 0) {
            perror("ERROR connecting"); failed = 1; break;
        }

        /* send the request */
        unsigned int total = consumed_size;
        unsigned int sent = 0;
        do {
            int bytes = write(sockfd,message+sent,total-sent);
            if (bytes < 0) {
                perror("ERROR writing message to socket"); failed = 1; break;
            }
            if (bytes == 0)
                break;
            sent+=bytes;
        } while (sent < total);

        /* receive the response */
        memset(response, 0, sizeof(response));
        total = sizeof(response)-1;
        unsigned int received = 0;
        do {
            int bytes = read(sockfd,response+received, total-received);
            if (bytes < 0) {
                perror("ERROR reading response from socket"); failed = 1; break;
            }
            if (bytes == 0)
                break;
            received += bytes;
        } while (received < total);

        if (received == total) {
            perror("ERROR storing complete response from socket"); failed = 1; break;
        }
        printf("Response received size %u\n", received);
    }while(0);

    /* close the socket */
    if ( sockfd > 0 ) {
        close(sockfd);
    }
    free(message);

    /* process response */
    if (failed == 0) {
        printf("Response:\n%s\n",response);
    }

    return 0;
}

