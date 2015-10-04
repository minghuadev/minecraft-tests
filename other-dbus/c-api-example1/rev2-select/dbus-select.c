/*
 * Example low-level D-Bus code.
 * Written by Matthew Johnson <dbus@matthew.ath.cx>
 *
 * This code has been released into the Public Domain.
 * You may do whatever you like with it.
 *
 * Subsequent tweaks by Will Ware <wware@alum.mit.edu>
 * Still in the public domain.
 */

#define _GNU_SOURCE /* for unistd.h for pipe2 */

#include <dbus/dbus.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* for profiling */
#include <sys/time.h> /* for gettimeofday */
static unsigned int usdiff(struct timeval *x, struct timeval *y) 
{
    unsigned int tmx = x->tv_sec % 1000;
    unsigned int tmy = y->tv_sec % 1000;
    if ( tmy < tmx ) tmy += 1000;
    return (tmy*1000000+y->tv_usec) - (tmx*1000000+x->tv_usec);
}
#define TMNMAX (100000)
static unsigned int tmnmax=20;
static unsigned int tmnlist[TMNMAX] = {0};
static unsigned int tmnlistcnt = 0;

/**
 * Connect to the DBUS bus and send a broadcast signal
 */
void sendsignal(char* sigvalue)
{
   DBusMessage* msg;
   DBusMessageIter args;
   DBusConnection* conn;
   DBusError err;
   int ret;
   dbus_uint32_t serial = 0;

   printf("Sending signal with value %s\n", sigvalue);

   // initialise the error value
   dbus_error_init(&err);

   // connect to the DBUS system bus, and check for errors
   conn = dbus_bus_get(DBUS_BUS_SESSION, &err);
   if (dbus_error_is_set(&err)) { 
      fprintf(stderr, "Connection Error (%s)\n", err.message); 
      dbus_error_free(&err); 
   }
   if (NULL == conn) { 
      exit(1); 
   }

   // register our name on the bus, and check for errors
   ret = dbus_bus_request_name(conn, "test.signal.source", DBUS_NAME_FLAG_REPLACE_EXISTING , &err);
   if (dbus_error_is_set(&err)) { 
      fprintf(stderr, "Name Error (%s)\n", err.message); 
      dbus_error_free(&err); 
   }
   if (DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER != ret) { 
      exit(1);
   }

   // create a signal & check for errors 
   msg = dbus_message_new_signal("/test/signal/Object", // object name of the signal
                                 "test.signal.Type", // interface name of the signal
                                 "Test"); // name of the signal
   if (NULL == msg) 
   { 
      fprintf(stderr, "Message Null\n"); 
      exit(1); 
   }

   // append arguments onto signal
   dbus_message_iter_init_append(msg, &args);
   if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_STRING, &sigvalue)) {
      fprintf(stderr, "Out Of Memory!\n"); 
      exit(1);
   }

   // send the message and flush the connection
   if (!dbus_connection_send(conn, msg, &serial)) {
      fprintf(stderr, "Out Of Memory!\n"); 
      exit(1);
   }
   dbus_connection_flush(conn);
   
   printf("Signal Sent\n");
   
   // free the message
   dbus_message_unref(msg);
}

/**
 * Call a method on a remote object
 */
void query(char* param , int altdest, int repeatmode)
{
   DBusMessage* msg;
   DBusMessageIter args;
   DBusConnection* conn;
   DBusError err;
   DBusPendingCall* pending;
   int ret;
   dbus_bool_t stat;
   dbus_uint32_t level;
    const char * dbname = "test.method.caller";
    int nrepeats = 0;
    int ii = 0;

   printf("Calling remote method with %s\n", param);

   // initialiset the errors
   dbus_error_init(&err);

   // connect to the system bus and check for errors
   conn = dbus_bus_get(DBUS_BUS_SESSION, &err);
   if (dbus_error_is_set(&err)) { 
      fprintf(stderr, "Connection Error (%s)\n", err.message); 
      dbus_error_free(&err);
   }
   if (NULL == conn) { 
      fprintf(stderr, "Connection null\n"); 
      exit(1); 
   }

   // request our name on the bus
   ret = dbus_bus_request_name(conn, dbname, DBUS_NAME_FLAG_REPLACE_EXISTING , &err);
   if (dbus_error_is_set(&err)) { 
      fprintf(stderr, "Name Error (%s)\n", err.message); 
      dbus_error_free(&err);
   }
   if (DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER != ret) { 
      fprintf(stderr, "Name not primary\n"); 
      exit(1);
   }
 if ( repeatmode == 2 ) nrepeats = tmnmax;
 for ( ii=0; ii<=nrepeats; ii++ ) {
   // create a new method call and check for errors
    struct timeval tmn1 = {0,0}; gettimeofday(&tmn1,NULL);
    printf("time before sending    %lu.%lu\n", tmn1.tv_sec, tmn1.tv_usec);
    if ( altdest == 0 ) {
   msg = dbus_message_new_method_call("test.method.server", // target for the method call
                                      "/test/method/Object", // object to call on
                                      "test.method.Type", // interface to call on
                                      "Method"); // method name
    } else {
        msg = dbus_message_new_method_call(
                                      "test.selector.server", // target for the method call
                                      "/test/method/Object", // object to call on
                                      "test.method.Type", // interface to call on
                                      "Method"); // method name
    }

   if (NULL == msg) { 
      fprintf(stderr, "Message Null\n");
      exit(1);
   }

   // append arguments
   dbus_message_iter_init_append(msg, &args);
   if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_STRING, &param)) {
      fprintf(stderr, "Out Of Memory!\n"); 
      exit(1);
   }
   
    struct timeval tmn2 = {0,0}; gettimeofday(&tmn2,NULL);
    printf("time before sending    %lu.%lu\n", tmn2.tv_sec, tmn2.tv_usec);
   // send message and get a handle for a reply
   if (!dbus_connection_send_with_reply (conn, msg, &pending, -1)) { // -1 is default timeout
      fprintf(stderr, "Out Of Memory!\n"); 
      exit(1);
   }
   if (NULL == pending) { 
      fprintf(stderr, "Pending Call Null\n"); 
      exit(1); 
   }
   dbus_connection_flush(conn);
   
   printf("Request Sent\n");
    struct timeval tmn3 = {0,0}; gettimeofday(&tmn3,NULL);
    printf("time after sending     %9lu.%06lu\n", tmn3.tv_sec, tmn3.tv_usec);
   
   // free message
   dbus_message_unref(msg);
   
   // block until we recieve a reply
   dbus_pending_call_block(pending);
    if ( ! dbus_pending_call_get_completed(pending) ) {
        dbus_pending_call_unref(pending);
        fprintf(stderr, " error Reply incomplete\n");
        exit(1);
    }
    /* timeout notes:
     *   it always reaches here, _completed() always return true.
     *   if destination name does not exist, it consumes 0 time and returns
     *           a string indicating the possible error.
     *   if destination replies late, it consumes full timeout duration and
     *           returns a string about the possible error.
     */
    struct timeval tmn4 = {0,0}; gettimeofday(&tmn4,NULL);
    printf("time after receiving   %lu.%lu\n", tmn4.tv_sec, tmn4.tv_usec);


   // get the reply message
   msg = dbus_pending_call_steal_reply(pending);
   if (NULL == msg) {
      fprintf(stderr, "Reply Null\n"); 
      exit(1); 
   }
   // free the pending message handle
   dbus_pending_call_unref(pending);

    /* */
    int validerror = 0;
    { int mtype = dbus_message_get_type(msg);
        if ( mtype == DBUS_MESSAGE_TYPE_ERROR ) {
            fprintf(stderr, " error Reply with a valid error detected!\n");
            validerror = 1;
        } else if ( mtype != DBUS_MESSAGE_TYPE_METHOD_RETURN ) {
            fprintf(stderr, " error Reply not a valid return type!"
                    " received message type %d\n", mtype);
        }
    }

   // read the parameters
   if (!dbus_message_iter_init(msg, &args))
      fprintf(stderr, "Message has no arguments!\n"); 
   else if (DBUS_TYPE_BOOLEAN != dbus_message_iter_get_arg_type(&args)) 
    {
      fprintf(stderr, "Argument is not boolean!\n"); 
        if (DBUS_TYPE_STRING == dbus_message_iter_get_arg_type(&args) ) {
            fprintf(stderr, "Argument 1 is string!\n");
            if ( validerror ) {
                char * strval = (char*)"<init-unknown>";
                dbus_message_iter_get_basic(&args, &strval);
                if ( strval != NULL && strnlen(strval, 160) < 160 ) {
                    printf("RPC reply arg 0 is c%u %s\n", 160, strval);
                } else {
                    printf("RPC reply arg 0 error \n");
                }
            }
        } else if (DBUS_TYPE_UINT32 == dbus_message_iter_get_arg_type(&args) ) {
            fprintf(stderr, "Argument 1 is uint32!\n");
        } else {
            fprintf(stderr, "Argument 1 is not recognized!\n");
        }
    }
   else
      dbus_message_iter_get_basic(&args, &stat);

   if (!dbus_message_iter_next(&args))
      fprintf(stderr, "Message has too few arguments!\n"); 
   else if (DBUS_TYPE_UINT32 != dbus_message_iter_get_arg_type(&args)) 
      fprintf(stderr, "Argument is not int!\n"); 
   else
      dbus_message_iter_get_basic(&args, &level);

   printf("Got Reply: %d, %d\n", stat, level);
   
   // free reply
   dbus_message_unref(msg);   

    struct timeval tmn9 = {0,0}; gettimeofday(&tmn9,NULL);
    printf("time after receiving   %lu.%lu\n", tmn9.tv_sec, tmn9.tv_usec);
    unsigned int tmncost = usdiff(&tmn1, &tmn9);
    printf("time consumed           %19s.%06u\n", "", tmncost);

    if ( tmnlistcnt < tmnmax ) {
        tmnlist[tmnlistcnt] = tmncost;
        tmnlistcnt ++;
    } else if ( tmnlistcnt == tmnmax ) {
        unsigned int tmnavg = 0;
        unsigned int i;
        for (i=0; i<tmnmax; i++) {
            tmnavg += tmnlist[i];
        }
        tmnavg /= tmnmax;
        tmnlistcnt ++;
        printf("time consumed           %9s.%06u\n", "", tmncost);
        printf("time consumed avg       %30s.%06u tmnmax %u\n", 
               "", tmnavg, tmnmax);
    }
 } /* for ii */

    dbus_bus_release_name(conn, dbname, &err);
    dbus_connection_unref(conn);
}

void reply_to_method_call(DBusMessage* msg, DBusConnection* conn)
{
   DBusMessage* reply;
   DBusMessageIter args;
   dbus_bool_t stat = TRUE;
   dbus_uint32_t level = 21614;
   dbus_uint32_t serial = 0;
   char* param = "";

   // read the arguments
   if (!dbus_message_iter_init(msg, &args))
      fprintf(stderr, "Message has no arguments!\n"); 
   else if (DBUS_TYPE_STRING != dbus_message_iter_get_arg_type(&args)) 
      fprintf(stderr, "Argument is not string!\n"); 
   else 
      dbus_message_iter_get_basic(&args, &param);

   //struct timeval tmn={0,0}; gettimeofday(&tmn,NULL);
   //printf("Method called with %s  %lu.%06lu\n", param, tmn.tv_sec, tmn.tv_usec);
   printf("Method called with %s\n", param);

   // create a reply from the message
   reply = dbus_message_new_method_return(msg);

   // add the arguments to the reply
   dbus_message_iter_init_append(reply, &args);
   if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_BOOLEAN, &stat)) { 
      fprintf(stderr, "Out Of Memory!\n"); 
      exit(1);
   }
   if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_UINT32, &level)) { 
      fprintf(stderr, "Out Of Memory!\n"); 
      exit(1);
   }

   // send the reply && flush the connection
   if (!dbus_connection_send(conn, reply, &serial)) {
      fprintf(stderr, "Out Of Memory!\n"); 
      exit(1);
   }
   dbus_connection_flush(conn);

   // free the reply
   dbus_message_unref(reply);
}

/**
 * Server that exposes a method call and waits for it to be called
 */
void listen() 
{
   DBusMessage* msg;
   DBusConnection* conn;
   DBusError err;
   int ret;

   printf("Listening for method calls\n");

   // initialise the error
   dbus_error_init(&err);
   
   // connect to the bus and check for errors
   conn = dbus_bus_get(DBUS_BUS_SESSION, &err);
   if (dbus_error_is_set(&err)) { 
      fprintf(stderr, "Connection Error (%s)\n", err.message); 
      dbus_error_free(&err); 
   }
   if (NULL == conn) {
      fprintf(stderr, "Connection Null\n"); 
      exit(1); 
   }
   
   // request our name on the bus and check for errors
   ret = dbus_bus_request_name(conn, "test.method.server", DBUS_NAME_FLAG_REPLACE_EXISTING , &err);
   if (dbus_error_is_set(&err)) { 
      fprintf(stderr, "Name Error (%s)\n", err.message); 
      dbus_error_free(&err);
   }
   if (DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER != ret) { 
      fprintf(stderr, "Not Primary Owner (%d)\n", ret);
      exit(1); 
   }

   // loop, testing for new messages
   while (1) {
      // non blocking read of the next available message
      dbus_connection_read_write(conn, 100);
      msg = dbus_connection_pop_message(conn);

      // loop again if we haven't got a message
      if (NULL == msg) { 
         usleep(100);
         continue; 
      }
      
      // check this is a method call for the right interface & method
      if (dbus_message_is_method_call(msg, "test.method.Type", "Method")) 
         reply_to_method_call(msg, conn);

      // free the message
      dbus_message_unref(msg);
   }

}

/**
 * Listens for signals on the bus
 */
void receive()
{
   DBusMessage* msg;
   DBusMessageIter args;
   DBusConnection* conn;
   DBusError err;
   int ret;
   char* sigvalue;

   printf("Listening for signals\n");

   // initialise the errors
   dbus_error_init(&err);
   
   // connect to the bus and check for errors
   conn = dbus_bus_get(DBUS_BUS_SESSION, &err);
   if (dbus_error_is_set(&err)) { 
      fprintf(stderr, "Connection Error (%s)\n", err.message);
      dbus_error_free(&err); 
   }
   if (NULL == conn) { 
      exit(1);
   }
   
   // request our name on the bus and check for errors
   ret = dbus_bus_request_name(conn, "test.signal.sink", DBUS_NAME_FLAG_REPLACE_EXISTING , &err);
   if (dbus_error_is_set(&err)) { 
      fprintf(stderr, "Name Error (%s)\n", err.message);
      dbus_error_free(&err); 
   }
   if (DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER != ret) {
      exit(1);
   }

   // add a rule for which messages we want to see
   dbus_bus_add_match(conn, "type='signal',interface='test.signal.Type'", &err); // see signals from the given interface
   dbus_connection_flush(conn);
   if (dbus_error_is_set(&err)) { 
      fprintf(stderr, "Match Error (%s)\n", err.message);
      exit(1); 
   }
   printf("Match rule sent\n");

   // loop listening for signals being emmitted
   while (1) {

      // non blocking read of the next available message
      dbus_connection_read_write(conn, 0);
      msg = dbus_connection_pop_message(conn);

      // loop again if we haven't read a message
      if (NULL == msg) { 
         usleep(10000);
         continue;
      }

      // check if the message is a signal from the correct interface and with the correct name
      if (dbus_message_is_signal(msg, "test.signal.Type", "Test")) {
         
         // read the parameters
         if (!dbus_message_iter_init(msg, &args))
            fprintf(stderr, "Message Has No Parameters\n");
         else if (DBUS_TYPE_STRING != dbus_message_iter_get_arg_type(&args)) 
            fprintf(stderr, "Argument is not string!\n"); 
         else
            dbus_message_iter_get_basic(&args, &sigvalue);
         
         printf("Got Signal with value %s\n", sigvalue);
      }

      // free the message
      dbus_message_unref(msg);
   }
}

/* ------------------------------------------------------------ */

/* chgevt: 
 * when watch/timeout changes, pass a chgevt via a pipe to 
 *  **the selector loop**  so the loop will return from select() and 
 * react to the dbus change quickly. only need this when new watch/timeout 
 * is added or enabled. when a watch/timeout is removed or disabled, 
 * quick response is not needed. 
 * 
 * when running in single thread because those changes happen only 
 * in stage 2 of the selector loop, this chgevt path is not necessary. 
 * if running in multiple threads, e.g. calling dbus sending from 
 * another thread, then the path would be essential. 
 */
#include <unistd.h> /* for pipe */
#include <errno.h>
#include <fcntl.h> /* for O_NONBLOCK */
#define CHGEVT_ADD_WATCH   (1)
#define CHGEVT_ADD_TIMEOUT (2)
static int watched_chgevt_fds[2] = {0,0}; /* [0] read, [1] write */
static void watched_chgevt_setup() {
    int rc = pipe2(watched_chgevt_fds, O_NONBLOCK);
    if ( rc != 0 ) watched_chgevt_fds[0] = watched_chgevt_fds[1] = 0;
}
static void watched_chgevt_send(int evt) {
    if ( watched_chgevt_fds[1] ) write(watched_chgevt_fds[1], &evt, 1); 
}
static int watched_chgevt_get() { 
    int rc = 0;
    if ( watched_chgevt_fds[0] ) { 
        if ( (rc = read(watched_chgevt_fds[0], &rc, 1)) < 0 ) {
            if ( errno != EAGAIN ) {
                perror("watched_chgevt_fds pipe failed");
                watched_chgevt_fds[0] = watched_chgevt_fds[1] = 0;
            }
            rc = 0;
        }
    }
    return rc;
}

/* watch */
static DBusWatch * watched_watch = NULL;
static int watched_rd_fd = 0;
static int watched_wr_fd = 0;

static dbus_bool_t add_watch(DBusWatch *w, void *data)
{
    if (!dbus_watch_get_enabled(w))
        return TRUE;

    int fd = dbus_watch_get_unix_fd(w);
    unsigned int flags = dbus_watch_get_flags(w);
    int old_rd_fd = watched_rd_fd;
    int old_wr_fd = watched_wr_fd;
    if (flags & DBUS_WATCH_READABLE)
        watched_rd_fd = fd;
    if (flags & DBUS_WATCH_WRITABLE)
        watched_wr_fd = fd;
    watched_watch = w;

    printf(" WATCH:    add dbus watch fd=%d watch=%p rd_fd=%d/%d wr_fd=%d/%d\n", 
           fd, w, watched_rd_fd, old_rd_fd, watched_wr_fd, old_wr_fd);
    watched_chgevt_send( CHGEVT_ADD_WATCH ); 
    return TRUE;
}
static void remove_watch(DBusWatch *w, void *data)
{
    watched_watch = NULL;
    watched_rd_fd = 0;
    watched_wr_fd = 0;
    printf(" WATCH:    remove dbus watch watch=%p\n", w);
}

static void toggle_watch(DBusWatch *w, void *data)
{
    printf(" WATCH:    toggle dbus watch watch=%p\n", w);
    if (dbus_watch_get_enabled(w))
        add_watch(w, data);
    else
        remove_watch(w, data);
}

/* timeout */
#include <limits.h> /* for INT_MAX */
#include <sys/time.h> /* for gettimeofday() */

static DBusTimeout * watched_timeout = NULL;
static struct timeval watched_timeout_start_tv = { 0, 0 };
static unsigned int watched_timeout_setv = 0;
static unsigned int watched_timeout_lastv = 0;

#define TIMEOUT_MAX_MS ( 1000 * 1000 ) /* 1000 sec */
#define TIMEOUT_MOD_MS ( 8 * TIMEOUT_MAX_MS ) /* 8000 sec */
               /* note: last_time is 0 to 7999 sec. 
                *       next_timeout is 0 to 8999 sec.
                */
#define TIME_TV_TO_MS(x) \
               ( (x.tv_sec%(TIMEOUT_MOD_MS/1000))*1000 + \
                 x.tv_usec/1000 )

static dbus_bool_t add_timeout(DBusTimeout *t, void *data)
{
    if (!dbus_timeout_get_enabled(t))
        return TRUE;

    int ms = dbus_timeout_get_interval(t);
    if ( ms < 0 || ms > TIMEOUT_MAX_MS ) {
        ms = TIMEOUT_MAX_MS;
        if ( ms < 0 || ms > INT_MAX/2-1 ) {
            ms = INT_MAX/2-1;
        }
    }
    if ( ms < 1 ) {
        ms = 1; 
    }

    struct timeval tnow = {0,0};
    gettimeofday(&tnow, NULL);
    unsigned int tnowms = TIME_TV_TO_MS(tnow);

    printf(" TIMEOUT: add dbus timeout %p value %u ms\n", t, ms);

    watched_timeout_start_tv = tnow;
    watched_timeout_setv = ms;
    watched_timeout_lastv = tnowms;
    watched_timeout = t;

    watched_chgevt_send( CHGEVT_ADD_TIMEOUT ); 
    return TRUE;
}
static void remove_timeout(DBusTimeout *t, void *data)
{
    printf(" TIMEOUT: remove timeout %p\n", t);
    watched_timeout = NULL;
    struct timeval tv = { .tv_sec = 0, .tv_usec = 0, };
    watched_timeout_start_tv = tv;
    watched_timeout_setv = 0;
    watched_timeout_lastv = 0;
}

static void toggle_timeout(DBusTimeout *t, void *data)
{
    printf(" TIMEOUT: toggle timeout %p\n", t);
    if (dbus_timeout_get_enabled(t))
        add_timeout(t, data);
    else
        remove_timeout(t, data);
}

/* the new selector function */
 /* receive */
static int dbus_selector_process_recv(DBusConnection* conn, int iswaiting_rpcreply,
                                      DBusPendingCall** pendingargptr);

 /* send rpc request */
static int dbus_selector_process_post_send( DBusConnection* conn, char * param,
                                            DBusPendingCall** pendingargptr);
 /* receive rpc reply, called by process_recv() */
static int dbus_selector_process_post_reply( DBusConnection* conn,
                                             DBusPendingCall** pendingargptr );
/* selector */
#include <sys/select.h>
#include <time.h>
static unsigned int lastregtime = 0;
static struct timeval tmn0 = {0,0};

int dbus_selector(char *param, int altsel )
{
   DBusConnection* conn;
   DBusError err;
   int ret = 1; /* default fail */

    watched_chgevt_setup();


        char * destarray[4] = { "test.selector.server", "test.selector.client",
                                "test.unknown.user1", "test.unknown.user2" };
        char * deststr = destarray[0];
        if ( altsel != 0 ) {
            deststr = destarray[1];
            lastregtime = time(NULL);
        }

   printf("Accepting method calls and signals\n");

   // initialise the error
   dbus_error_init(&err);
  
   // connect to the bus and check for errors
   conn = dbus_bus_get(DBUS_BUS_SESSION, &err);
   if (dbus_error_is_set(&err)) {
      fprintf(stderr, "Connection Error (%s)\n", err.message);
      dbus_error_free(&err);
   }
   if (NULL == conn) {
      fprintf(stderr, "Connection Null\n");
      return ret; /* ret=1 fail */
   }

   // request our name on the bus and check for errors
   ret = dbus_bus_request_name(conn, deststr /* "test.selector.server" */, 
                               DBUS_NAME_FLAG_REPLACE_EXISTING , &err);
   if (dbus_error_is_set(&err)) {
      fprintf(stderr, "Name Error (%s)\n", err.message);
      dbus_error_free(&err);
   }
   if (DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER != ret) {
      fprintf(stderr, "Not Primary Owner (%d)\n", ret);
      return ret; /* ret=1 fail */
   }

   // add a rule for which messages we want to see
   dbus_bus_add_match(conn, "type='signal',interface='test.signal.Type'", &err); 
                                           // see signals from the given interface
   dbus_connection_flush(conn); /* Note: this would block */
   if (dbus_error_is_set(&err)) {
      fprintf(stderr, "Match Error (%s)\n", err.message);
      return ret; /* ret=1 fail */
   }
   printf("Match signal rule sent\n");

    /* setup watch and timeout */
    if (!dbus_connection_set_watch_functions(conn, add_watch, remove_watch,
                                             toggle_watch, NULL, NULL)) {
        printf(" ERROR dbus_connection_set_watch_functions() failed\n");
        return ret; /* ret=1 fail */
    }
    if (!dbus_connection_set_timeout_functions(conn, add_timeout,
                                               remove_timeout, toggle_timeout,
                                               NULL, NULL)) {
        printf(" ERROR dbus_connection_set_timeout_functions() failed\n");
        return ret; /* ret=1 fail */
    }

    /* the selector loop */
    ret = 0; /* default success */
    struct timeval local_to_startv = {0,0}; /* timeout saved locally */
    DBusPendingCall* pending = NULL; /* keep track of the outstanding rpc call */
    while(ret == 0) {

        /* the selector loop stage 1, setup for select() call. 
         * in this stage no dbus watch/timeout change should happen 
         */

        #define DEFAULT_SELECT_LOOP_MS (5500)
        int modified_timeout = 0; /* yes or no */

        fd_set rfds, wfds, efds;
        struct timeval timeoutval = {
                           DEFAULT_SELECT_LOOP_MS/1000, 
                           (DEFAULT_SELECT_LOOP_MS%1000)*1000 };
        int nfds = 1;
        int rc = 0;

        printf("\n");
        FD_ZERO(&rfds); FD_ZERO(&wfds); FD_ZERO(&efds);
        if ( watched_watch != NULL ) {
            if ( watched_rd_fd ) { 
                FD_SET(watched_rd_fd, &rfds);
                FD_SET(watched_rd_fd, &efds);
                if ( nfds <= watched_rd_fd ) { nfds = watched_rd_fd + 1; } 
                printf(" SELECT nfds %d  rdfd %d\n", nfds, watched_rd_fd);
            }
            if ( watched_wr_fd ) { 
                FD_SET(watched_wr_fd, &wfds);
                FD_SET(watched_wr_fd, &efds);
                if ( nfds <= watched_wr_fd ) { nfds = watched_wr_fd + 1; } 
                printf(" SELECT nfds %d  wrfd %d\n", nfds, watched_wr_fd);
            }
        }
        if ( watched_chgevt_fds[0] != 0 ) {
            FD_SET(watched_chgevt_fds[0], &rfds);
            FD_SET(watched_chgevt_fds[0], &efds);
        }

        if ( watched_timeout != NULL ) {
            struct timeval startv = watched_timeout_start_tv;
            unsigned int setv = watched_timeout_setv;
            unsigned int lastv = watched_timeout_lastv;

            struct timeval tnow = {0,0};
            unsigned int tnowms = 0;
            unsigned int toms = 0;
            unsigned int tdiff = 0;

            gettimeofday(&tnow, NULL);
            tnowms = TIME_TV_TO_MS(tnow);

            if ( startv.tv_sec != local_to_startv.tv_sec || 
                 startv.tv_usec != local_to_startv.tv_sec   ) 
            { /* new timeout */
                local_to_startv = startv;
            }
            if ( lastv > tnowms ) {
                tnowms += TIMEOUT_MOD_MS;
            }
            toms = lastv + setv + 1;
                             /* add 1 to make up for rounding loss */
            if ( toms > tnowms ) {
                tdiff = toms - tnowms; /* ms till timeout */
            }
            if ( tdiff < DEFAULT_SELECT_LOOP_MS ) {
                /* revise timeout value */
                timeoutval.tv_sec = tdiff/1000;
                timeoutval.tv_usec = (tdiff%1000)*1000;
                modified_timeout = 1; /* yes */
            }
        }

        if ( modified_timeout ) {
            printf(" SELECT with nfds %d ... new tiemout %lu.%03lu\n", 
                         nfds, timeoutval.tv_sec, timeoutval.tv_usec/1000);
        } else {
            printf(" SELECT with nfds %d...\n", nfds);
        }

        rc = select(nfds, &rfds, &wfds, &efds, &timeoutval);
        if ( rc < 0 ) {
            printf(" SELECT returned error %d\n", rc);
            break;
        }

        /* the selector loop stage 2, dbus operation. 
         * in this stage dbus watch/timeout could change.
         */

        /* check timeout */
        if ( watched_timeout != NULL ) {
            struct timeval startv = watched_timeout_start_tv;
            unsigned int setv = watched_timeout_setv;
            unsigned int lastv = watched_timeout_lastv;
            struct timeval tnow = {0,0}; unsigned int tnowms = 0, toms = 0;

            gettimeofday(&tnow, NULL);
            tnowms = TIME_TV_TO_MS(tnow);

            if ( startv.tv_sec == local_to_startv.tv_sec && 
                 startv.tv_usec == local_to_startv.tv_sec   ) 
            { /* same timeout */
                if ( lastv > tnowms ) {
                    tnowms += TIMEOUT_MOD_MS;
                }
                toms = lastv + setv + 1;
                             /* add 1 to make up for rounding loss */
                if ( toms >= tnowms ) {
                    watched_timeout_lastv = tnowms%TIMEOUT_MOD_MS;
                    printf(" HANDLING dbus handle timeout %p\n", 
                           watched_timeout);
                    dbus_timeout_handle(watched_timeout);
                    printf(" HANDLING dbus handle timeout %p done\n", 
                           watched_timeout);
                }
            } /* else if not the same timeout as before select() skip for now */
        }

        /* self initiated rpc call */
        if ( altsel ) {
            unsigned int tmnow = time(NULL);
            unsigned int tmdiff = tmnow - lastregtime;
            if ( tmdiff > 10 ) { /* send a rpc evey 10 seconds */

                struct timeval tmn = {0,0}; gettimeofday(&tmn,NULL);
                printf(" RPC call time  %lu.%06lu\n", tmn.tv_sec, tmn.tv_usec);
                tmn0 = tmn;

                dbus_selector_process_post_send(conn, param, &pending);
                lastregtime = tmnow;
            }
        }

        /* select() returned no event */
        if ( rc == 0 ) {
            printf(" SELECT returned rc 0 \n");
            continue;
        }

        /* some event happened according to select() */
        printf(" SELECT returned rc %d \n", rc);
        if ( watched_watch != NULL ) {
            if ( watched_rd_fd ) { 
                if ( FD_ISSET(watched_rd_fd, &rfds) ) {
                    printf(" HANDLING calls watch_handle\n");
                    dbus_watch_handle(watched_watch, DBUS_WATCH_READABLE);
                    printf(" HANDLING calls process_recv\n");
                    dbus_selector_process_recv(conn, pending==NULL?0:1,
                                                     &pending);
                    printf(" HANDLING done process_recv\n");
                }
                if ( FD_ISSET(watched_rd_fd, &efds) ) {
                    printf(" HANDLING EXCEPTION with rd fd %d \n",
                           watched_rd_fd);
                }
            }
            if ( watched_wr_fd ) { 
                if ( FD_ISSET(watched_wr_fd, &wfds) ) {
                    dbus_watch_handle(watched_watch, DBUS_WATCH_WRITABLE);
                }
                if ( FD_ISSET(watched_wr_fd, &efds) ) {
                    printf(" HANDLING EXCEPTION with wr fd %d \n",
                           watched_wr_fd);
                }
            }
        }

        /* chgevt pipe */
        if ( watched_chgevt_fds[0] != 0 && FD_ISSET(watched_chgevt_fds[0], &rfds) ) {
            int chgevt = watched_chgevt_get();
            switch (chgevt) {
            case CHGEVT_ADD_WATCH: 
                printf(" HANDLING chgevt 1 consumed \n"); break;
            case CHGEVT_ADD_TIMEOUT: 
                printf(" HANDLING chgevt 2 consumed \n"); break;
            default: 
                printf(" HANDLING chgevt n=%d consumed \n", chgevt); break;
            }
        }
    }
   return ret;
}

static int dbus_selector_process_recv(DBusConnection* conn, int iswaiting_rpcreply,
                                      DBusPendingCall** pendingargptr)
{
    int ret = 1; /* default fail */

    /* remove this call that consumes .1ms because dbus is already read 
     * by dbus_watch_handle():
     * dbus_connection_read_write(conn, 0);
     * 
     * according to dbus_connection_dispatch(): The incoming data buffer 
     * is filled when the connection reads from its underlying transport 
     * (such as a socket). Reading usually happens in dbus_watch_handle() 
     * or dbus_connection_read_write().
     */
    DBusDispatchStatus dispatch_rc = dbus_connection_get_dispatch_status(conn);
    if ( DBUS_DISPATCH_DATA_REMAINS != dispatch_rc ) {
        printf(" ERROR recv no message in queue \n");
    }
    while( DBUS_DISPATCH_DATA_REMAINS == dispatch_rc ) {
        DBusMessage* msg = dbus_connection_borrow_message(conn);
        if ( msg == NULL ) {
            printf(" ERROR recv pending check FAILED: remains but "
                            "no message borrowed. \n");
            break;
        }
        int mtype = dbus_message_get_type(msg);
        if ( iswaiting_rpcreply &&  
             ( mtype == DBUS_MESSAGE_TYPE_METHOD_RETURN ||
               mtype == DBUS_MESSAGE_TYPE_ERROR           ) ) {
            printf(" RPC REPLY pending check SUCCESS: received rpc reply \n");
            dbus_connection_return_message(conn, msg);
            dbus_connection_dispatch(conn);
                                  /* dispatch so the received message at the 
                                   * head of queue is passed to the pendingcall
                                   */
            dbus_selector_process_post_reply( conn, pendingargptr );
                struct timeval tmn = {0,0}; gettimeofday(&tmn,NULL);
                printf(" RPC returned time  %lu.%06lu\n", tmn.tv_sec, tmn.tv_usec);

                unsigned int tmncost = usdiff(&tmn0, &tmn);
                printf(" RPC cost time      %19s.%06u\n", "", tmncost);

                if ( tmnlistcnt < tmnmax ) {
                    tmnlist[tmnlistcnt] = tmncost;
                    tmnlistcnt ++;
                } else if ( tmnlistcnt == tmnmax ) {
                    unsigned int tmnavg = 0;
                    unsigned int i;
                    for (i=0; i<tmnmax; i++) {
                        tmnavg += tmnlist[i];
                    }
                    tmnavg /= tmnmax;
                    tmnlistcnt ++;
                    printf("time consumed           %9s.%06u\n", "", tmncost);
                    printf("time consumed avg       %30s.%06u tmnmax %u\n", 
                           "", tmnavg, tmnmax);
exit(0);
                }

            printf(" RPC REPLY pending check SUCCESS: processed rpc reply \n");
        } else if ( mtype == DBUS_MESSAGE_TYPE_METHOD_RETURN ) {
            printf(" RECV pending check FAILED: received rpc reply \n");
            dbus_connection_steal_borrowed_message(conn, msg);
            dbus_message_unref(msg);
        } else if ( mtype == DBUS_MESSAGE_TYPE_ERROR ) {
            printf(" RECV pending check FAILED: received ERROR \n");
            dbus_connection_steal_borrowed_message(conn, msg);
            dbus_message_unref(msg);
        } else if ( mtype == DBUS_MESSAGE_TYPE_SIGNAL ) {
            printf(" SIGNAL pending check SUCCESS: received and drop \n");
            dbus_connection_steal_borrowed_message(conn, msg);
            dbus_message_unref(msg);
        } else if ( mtype == DBUS_MESSAGE_TYPE_METHOD_CALL ) {
            printf(" RPC RECV check SUCCESS: received rpc call. \n");
            dbus_connection_steal_borrowed_message(conn, msg);
            DBusMessage* reply = NULL;
            do {
                /* craft a reply message */
                DBusMessageIter args;
                dbus_uint32_t serial = 111;
                dbus_bool_t   stat    = TRUE;
                dbus_uint32_t retval1 = 555;
                const char *strval    = "good";
                reply = dbus_message_new_method_return(msg);
                dbus_message_iter_init_append(reply, &args);
                if ( !dbus_message_iter_append_basic(
                                       &args, DBUS_TYPE_BOOLEAN, &stat) ) {
                    printf(" error rpc reply Out Of Memory!\n");
                    break;
                }
                if ( !dbus_message_iter_append_basic(
                                       &args, DBUS_TYPE_UINT32, &retval1) ) {
                    printf(" error rpc reply Out Of Memory!\n");
                    break;
                }
                if ( !dbus_message_iter_append_basic(
                                       &args, DBUS_TYPE_STRING, &strval) ) {
                    printf(" error rpc reply Out Of Memory!\n");
                    break;
                }
                if ( !dbus_connection_send(conn, reply, &serial)) {
                    printf(" error rpc reply Out Of Memory!\n");
                    break;
                }
                dbus_connection_flush(conn);
            } while(0);
            if ( reply != NULL ) { dbus_message_unref(reply); }
            if ( msg != NULL ) { /* msg not consumed */
                //dbus_connection_return_message(conn, msg);
                dbus_message_unref(msg);
            }
            ret = 0; /* success */
        } else {
            printf(" error unknown msg type %d \n", mtype);
        }
        dispatch_rc = dbus_connection_get_dispatch_status(conn);
    }
    return ret;
}
static int dbus_selector_process_post_send( DBusConnection* conn, char * param,
                                            DBusPendingCall** pendingargptr)
{ /* mostly a copy of query() */
   DBusMessage* msg = NULL;
   DBusMessageIter args = {0};
   DBusError err = {0};
   DBusPendingCall* pending = NULL;
   int ret = 0;

   * pendingargptr = NULL;

   printf("Calling remote method with %s\n", param);

   // initialiset the errors
   dbus_error_init(&err);

    msg = dbus_message_new_method_call(
                                      "test.selector.server", // target for the method call
                                      "/test/method/Object", // object to call on
                                      "test.method.Type", // interface to call on
                                      "Method"); // method name
   if (NULL == msg) {
      fprintf(stderr, "Message Null\n");
      exit(1);
   }

   // append arguments
   dbus_message_iter_init_append(msg, &args);
   if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_STRING, &param)) {
      fprintf(stderr, "Out Of Memory!\n");
      exit(1);
   }

   // send message and get a handle for a reply
   if (!dbus_connection_send_with_reply (conn, msg, &pending, 300)) { // -1 is default timeout
      fprintf(stderr, "Out Of Memory!\n");
      exit(1);
   }
   if (NULL == pending) {
      fprintf(stderr, "Pending Call Null\n");
      exit(1);
   }
   printf("Request Sent\n");

   dbus_connection_flush(conn); /* Note: block until write finishes */
   printf("Request flushed\n");

   // free message
   dbus_message_unref(msg);
   * pendingargptr = pending;
    return ret;
}

static int dbus_selector_process_post_reply( DBusConnection* conn,
                                             DBusPendingCall** pendingargptr )
{
   DBusMessage* msg = NULL;
   DBusMessageIter args = {0};
   dbus_bool_t stat = FALSE;
   dbus_uint32_t level = 0;
   DBusPendingCall* pending = *pendingargptr;

   // block until we recieve a reply
   /* dbus_pending_call_block(pending); Note: this would block. use dispatch. */
    if ( ! dbus_pending_call_get_completed(pending) ) {
        dbus_pending_call_unref(pending);
        *pendingargptr = NULL;
        fprintf(stderr, " error Reply incomplete\n");
        exit(1);
    }
    /* timeout notes:
     *   it always reaches here, _completed() always return true.
     *   if destination name does not exist, it consumes 0 time and returns
     *           a string indicating the possible error.
     *   if destination replies late, it consumes full timeout duration and
     *           returns a string about the possible error.
     */

    /* can use cancel at top level. still safe to call cancel here: 
    dbus_pending_call_cancel(pending);
     */

   // get the reply message
   msg = dbus_pending_call_steal_reply(pending);
   if (NULL == msg) {
      fprintf(stderr, "Reply Null\n");
      exit(1);
   }
   // free the pending message handle
   dbus_pending_call_unref(pending);
    *pendingargptr = NULL;

    /* */
    int validerror = 0;
    { int mtype = dbus_message_get_type(msg);
        if ( mtype == DBUS_MESSAGE_TYPE_ERROR ) {
            fprintf(stderr, " error Reply with a valid error detected!\n");
            validerror = 1;
        } else if ( mtype != DBUS_MESSAGE_TYPE_METHOD_RETURN ) {
            fprintf(stderr, " error Reply not a valid return type!"
                    " received message type %d\n", mtype);
        }
    }

   // read the parameters
   if (!dbus_message_iter_init(msg, &args))
      fprintf(stderr, "Message has no arguments!\n");
   else if (DBUS_TYPE_BOOLEAN != dbus_message_iter_get_arg_type(&args))
    {
      fprintf(stderr, "Argument is not boolean!\n");
        if (DBUS_TYPE_STRING == dbus_message_iter_get_arg_type(&args) ) {
            fprintf(stderr, "Argument 1 is string!\n");
            if ( validerror ) {
                char * strval = (char*)"<init-unknown>";
                dbus_message_iter_get_basic(&args, &strval);
                if ( strval != NULL && strnlen(strval, 160) < 160 ) {
                    printf("RPC reply arg 0 is c%u %s\n", 160, strval);
                } else {
                    printf("RPC reply arg 0 error \n");
                }
            }
        } else if (DBUS_TYPE_UINT32 == dbus_message_iter_get_arg_type(&args) ) {
            fprintf(stderr, "Argument 1 is uint32!\n");
        } else {
            fprintf(stderr, "Argument 1 is not recognized!\n");
        }
    }
   else
      dbus_message_iter_get_basic(&args, &stat);

   if (!dbus_message_iter_next(&args))
      fprintf(stderr, "Message has too few arguments!\n");
   else if (DBUS_TYPE_UINT32 != dbus_message_iter_get_arg_type(&args))
      fprintf(stderr, "Argument is not int!\n");
   else
      dbus_message_iter_get_basic(&args, &level);

   printf("Got Reply: %d, %d\n", stat, level);

   // free reply
   dbus_message_unref(msg);

   return 0;
}

/* ------------------------------------------------------------ */

int main(int argc, char** argv)
{
   if (2 > argc) {
      printf ("Syntax: dbus-example [send|receive|listen|query] [<param>]\n");
      return 1;
   }
   char* param = "no param";
   int repeatmode = 0;
   if (3 <= argc && NULL != argv[2]) param = argv[2];
    if (4 <= argc && NULL != argv[3]) {
        if ( strncmp(argv[3],"1",2) == 0 ) {
            repeatmode = 1;
        } else if ( strncmp(argv[3],"2",2) == 0 ) {
            repeatmode = 2;
        }
    }
    if (5 <= argc && NULL != argv[4]) {
        long t = atol(argv[4]);
        if ( t > 0 && t < TMNMAX ) {
            tmnmax = (unsigned int)t;
            printf(" repeat max new value %u\n", tmnmax);
        } else {
            printf(" repeat max out of range %ld\n", t);
        }
    }
   if (0 == strcmp(argv[1], "send"))
      sendsignal(param);
   else if (0 == strcmp(argv[1], "receive"))
      receive();
   else if (0 == strcmp(argv[1], "listen"))
      listen();
   else if (0 == strcmp(argv[1], "query"))
    {
        printf(" repeatmode %d \n", repeatmode);
        if ( repeatmode == 0 ) {
      query(param, 0, 0);
        } else if ( repeatmode == 1 ) {
            int i=0;
            query(param, 0, 1);
            for (i=0; i<tmnmax; i++) {
                query(param, 0, 1);
            }
        } else if ( repeatmode == 2 ) {
            query(param, 0, 2);
        }
    }
   else if (0 == strcmp(argv[1], "selector"))
      dbus_selector(param, 0);
   else if (0 == strcmp(argv[1], "seltest"))
      query(param, 1, 0);
   else if (0 == strcmp(argv[1], "selpost"))
      dbus_selector(param, 1);
   else {
      printf ("Syntax: dbus-select [[send|receive|listen|query]|"
                        "[selector|seltest|selpost]] [<param>]\n");
      return 1;
   }
   return 0;
}

