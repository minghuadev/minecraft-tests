/*
 * example2.c
 */

#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit, atoi, malloc, free */
#include <unistd.h> /* read, write, close */
#include <string.h> /* memcpy, memset */
#include <sys/socket.h> /* socket, connect */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */

#include <sys/types.h> /* fstat */
#include <sys/stat.h>  /* fstat */
#include <stdlib.h>    /* malloc */

#define MAX_HTTP_SIZE_TO_POST (10 * 1024 * 1024) /* 10 M including HTTP header */

int main(int argc,char *argv[])
{
    int i, rc;
    rc = 0; /* default success */

    if (argc < 6) { puts("ERROR Parameters: <host> <port> <directory> <file> <seqn>"); exit(1); }
    if ( strnlen(argv[1], 255) < 1 ) { puts("ERROR Argv[1]: <host> "); exit(1);}
    if ( strnlen(argv[2], 255) < 1 ) { puts("ERROR Argv[2]: <port> "); exit(1);}
    if ( strnlen(argv[3], 255) < 1 ) { puts("ERROR Argv[3]: <directory> "); exit(1);}
    if ( strnlen(argv[4], 255) < 1 ) { puts("ERROR Argv[4]: <file> "); exit(1);}
    if ( strnlen(argv[5], 255) < 1 ) { puts("ERROR Argv[5]: <seqn> "); exit(1);}

    /* argv[1]: host */
    char *host = argv[1];

    /* argv[2]: port */
    long arg_port = strtol(argv[2], NULL, 10);
    if ( arg_port > 65535 || arg_port < 1 ) { puts("ERROR <port> out of range "); exit(1);}
    int portno = (int)arg_port;

    /* argv[3,4,5]: directory, file, seqn */
    char arg_url_path[256];
    char arg_file_path[256];

    memset(arg_url_path, 0, sizeof(arg_url_path));
    memset(arg_file_path, 0, sizeof(arg_file_path));

    rc = snprintf(arg_url_path, 255, "/upload/%s/%s", argv[5], argv[4]);
    if ( rc < 0 ) { perror("ERROR /upload/path failed"); exit(1); }
    else if ( rc >= 255 ) { puts("ERROR /upload/path failed truncated"); exit(1); }
    rc = snprintf(arg_file_path, 255, "%s%s", argv[3], argv[4]);
    if ( rc < 0 ) { perror("ERROR file path composition failed"); exit(1); }
    else if ( rc >= 255 ) { puts("ERROR file path composition failed truncated"); exit(1); }

    FILE * ifp = fopen(arg_file_path, "r");
    if (ifp == NULL) { perror("ERROR file path invalid"); exit(1); }

    struct stat fstat_buf;
    memset(&fstat_buf, 0, sizeof(fstat_buf));
    rc = fstat(fileno(ifp), &fstat_buf);
    if ( rc ) { perror("ERROR file stat failed"); fclose(ifp); exit(1); }
    unsigned int buf_size = fstat_buf.st_size;

    char *buffer = malloc(buf_size);
    if ( buffer == NULL ) { perror("ERROR malloc failed for content"); fclose(ifp); exit(1); }
    rc = fread(buffer, 1, buf_size, ifp);
    if ( rc != buf_size ) { perror("ERROR fread failed"); fclose(ifp); free(buffer); exit(1); }
    fclose(ifp);

    /* now data in buffer, of size buffer_size. */

    char *message;
    unsigned int message_size;

    char arg_url_method[] = "POST";

    char arg_cont_len[256];
    memset(arg_cont_len, 0, sizeof(arg_cont_len));
    rc = snprintf(arg_cont_len, 255, "Content-Length: %u\r\n", buf_size);
    if ( rc < 0 ) { perror("ERROR content length composition failed"); free(buffer); exit(1); }
    else if ( rc >= 255 ) { puts("ERROR content length composition failed truncated"); free(buffer); exit(1); }

    char arg_cont_type[256];
    memset(arg_cont_type, 0, sizeof(arg_cont_type));
    rc = snprintf(arg_cont_type, 255, "Content-Type: application/octet-stream\r\n");
    if ( rc < 0 ) { perror("ERROR content type composition failed"); free(buffer); exit(1); }
    else if ( rc >= 255 ) { puts("ERROR content type composition failed truncated"); free(buffer); exit(1); }


    /* How big is the message? */
    message_size = 0;

    message_size += strnlen("%s %s HTTP/1.0\r\n", 255);     /* request line */
    message_size += strnlen(arg_url_method, 255);           /* method         */
    message_size += strnlen(arg_url_path, 255);             /* path           */
    message_size += strnlen(arg_cont_type, 255);            /* content type   */
    message_size += strnlen(arg_cont_len, 255);             /* content length */
    for(i=6;i<argc;i++)                                     /* headers        */
        message_size += strnlen(argv[i], 255) + strnlen("\r\n", 255);
    message_size += strlen("\r\n");                         /* blank line     */

    if ( message_size >= MAX_HTTP_SIZE_TO_POST ||
         buf_size >= MAX_HTTP_SIZE_TO_POST ||
         message_size + buf_size >= MAX_HTTP_SIZE_TO_POST )
    {
        puts("ERROR http data too long"); free(buffer); exit(1);
    }

    message_size += buf_size;
    printf("ok: port %d host %s data %u content %u\n", portno, host, message_size, buf_size);

    /* allocate space for the message */
    message = malloc(message_size);
    if ( message == NULL ) { perror("ERROR malloc failed for data"); free(buffer); exit(1); }
    message[message_size - 1] = 0;

    /* fill in the parameters */
    unsigned int consumed_size = 0;
    int failed = 0;
    do {
        rc = snprintf(message, message_size - 1, "%s %s HTTP/1.0\r\n", arg_url_method, arg_url_path);
                                                            /* method, path   */
        if ( rc < 1 || rc >= message_size - 2 ) { failed = 1; break; }
        consumed_size += rc;
        if ( consumed_size >= message_size - 1 ) { failed = 2; break; }
        for(i=6;i<argc;i++) {                               /* headers        */
            rc = snprintf(message+consumed_size, message_size - consumed_size - 1, "%s\r\n", argv[i]);
            if ( rc < 1 || rc >= message_size - consumed_size - 2 ) { failed = 3; break; }
            consumed_size += rc;
            if ( consumed_size >= message_size - 1 ) { failed = 4; break; }
        }
        if ( failed ) break;
        /* content type */
        rc = snprintf(message+consumed_size, message_size - consumed_size - 1, "%s", arg_cont_type);
        if ( rc < 1 || rc >= message_size - consumed_size - 2 ) { failed = 5; break; }
        consumed_size += rc;
        if ( consumed_size >= message_size - 1 ) { failed = 6; break; }
        /* content length, plus the blank line */
        rc = snprintf(message+consumed_size, message_size - consumed_size - 1, "%s\r\n", arg_cont_len);
        if ( rc < 1 || rc >= message_size - consumed_size - 2 ) { failed = 7; break; }
        consumed_size += rc;
        if ( consumed_size >= message_size - 1 ) { failed = 8; break; }
    }while(0);
    if ( failed ) {
        puts("ERROR http header construction failed"); free(buffer); free(message); exit(1);
    }

    /* What are we going to send? */
    printf("Request header:\n%s\n",message);

    if ( consumed_size + buf_size > message_size ) {
        puts("ERROR http content construction failed truncated"); free(buffer); free(message); exit(1);
    }
    memcpy(message+consumed_size, buffer, buf_size);
    consumed_size += buf_size;
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
    free(buffer);

    /* process response */
    if (failed == 0) {
        printf("Response:\n%s\n",response);
    }

    return 0;
}

