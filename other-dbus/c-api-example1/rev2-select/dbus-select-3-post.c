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
#include <dbus/dbus.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

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
void query(char* param , int altdest)
{
   DBusMessage* msg;
   DBusMessageIter args;
   DBusConnection* conn;
   DBusError err;
   DBusPendingCall* pending;
   int ret;
   dbus_bool_t stat;
   dbus_uint32_t level;

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
      exit(1); 
   }

   // request our name on the bus
   ret = dbus_bus_request_name(conn, "test.method.caller", DBUS_NAME_FLAG_REPLACE_EXISTING , &err);
   if (dbus_error_is_set(&err)) { 
      fprintf(stderr, "Name Error (%s)\n", err.message); 
      dbus_error_free(&err);
   }
   if (DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER != ret) { 
      exit(1);
   }

   // create a new method call and check for errors
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
   DBusMessage* reply;
   DBusMessageIter args;
   DBusConnection* conn;
   DBusError err;
   int ret;
   char* param;

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
      dbus_connection_read_write(conn, 0);
      msg = dbus_connection_pop_message(conn);

      // loop again if we haven't got a message
      if (NULL == msg) { 
         usleep(10000);
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

#define LOG_DEBUG " debug "
#define LOG_ERROR " error "

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
    printf(LOG_DEBUG " added dbus watch fd=%d watch=%p rd_fd=%d/%d wr_fd=%d/%d\n", 
           fd, w, watched_rd_fd, old_rd_fd, watched_wr_fd, old_wr_fd);
    return TRUE;
}

static void remove_watch(DBusWatch *w, void *data)
{
    watched_watch = NULL;
    watched_rd_fd = 0;
    watched_wr_fd = 0;
    printf(LOG_DEBUG " removed dbus watch watch=%p\n", w);
}

static void toggle_watch(DBusWatch *w, void *data)
{
    printf(LOG_DEBUG " toggling dbus watch watch=%p\n", w);
    if (dbus_watch_get_enabled(w))
        add_watch(w, data);
    else
        remove_watch(w, data);
}

static DBusTimeout * watched_timeout = NULL;
static struct timeval watched_timeout_tv = { 0, 0 };

static dbus_bool_t add_timeout(DBusTimeout *t, void *data)
{
    if (!dbus_timeout_get_enabled(t))
        return TRUE;

    int ms = dbus_timeout_get_interval(t);
    struct timeval tv = {
        .tv_sec = ms / 1000,
        .tv_usec = (ms % 1000) * 1000,
    };

    printf(LOG_DEBUG " adding timeout %p val %u\n", t, ms);
    watched_timeout_tv = tv;
    watched_timeout = t;

    return TRUE;
}
static void remove_timeout(DBusTimeout *t, void *data)
{
    printf(LOG_DEBUG " removing timeout %p\n", t);
    watched_timeout = NULL;
    struct timeval tv = {
        .tv_sec = 0,
        .tv_usec = 0,
    };
    watched_timeout_tv = tv;
}

static void toggle_timeout(DBusTimeout *t, void *data)
{
    printf(LOG_DEBUG " toggling timeout %p\n", t);
    if (dbus_timeout_get_enabled(t))
        add_timeout(t, data);
    else
        remove_timeout(t, data);
}

/* the new selector function */
static int dbus_selector_process_recv(DBusConnection* conn, int iswaiting_rpcreply,
                                      DBusPendingCall** pendingargptr);
#include <sys/select.h>

static int dbus_selector_process_post(DBusConnection* conn, char * param,
                                      DBusPendingCall** pendingargptr);
static int dbus_selector_process_post_reply( DBusConnection* conn,
                                             DBusPendingCall** pendingargptr );
#include <time.h>
static unsigned int lastregtime = 0;

int dbus_selector(char *param, int altsel )
{
   DBusConnection* conn;
   DBusError err;
   int ret = 1; /* default fail */

        DBusPendingCall* pending = NULL;

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
   dbus_connection_flush(conn);
   if (dbus_error_is_set(&err)) {
      fprintf(stderr, "Match Error (%s)\n", err.message);
      return ret; /* ret=1 fail */
   }
   printf("Match signal rule sent\n");


    if (!dbus_connection_set_watch_functions(conn, add_watch, remove_watch,
                                             toggle_watch, NULL, NULL)) {
        printf(LOG_ERROR " dbus_connection_set_watch_functions() failed\n");
        return ret; /* ret=1 fail */
    }
    if (!dbus_connection_set_timeout_functions(conn, add_timeout,
                                               remove_timeout, toggle_timeout,
                                               NULL, NULL)) {
        printf(LOG_ERROR " dbus_connection_set_timeout_functions() failed\n");
        return ret; /* ret=1 fail */
    }

    ret = 0; /* default success */
    while(ret == 0) {

        fd_set rfds, wfds, efds;
        struct timeval timeoutval = {5, 500 * 1000};
        int nfds = 1;
        int rc = 0;
        FD_ZERO(&rfds); FD_ZERO(&wfds); FD_ZERO(&efds);
        if ( watched_watch != NULL ) {
            if ( watched_rd_fd ) { 
                FD_SET(watched_rd_fd, &rfds);
                FD_SET(watched_rd_fd, &efds);
                if ( nfds <= watched_rd_fd ) { nfds = watched_rd_fd + 1; } 
                printf(" select nfds %d  rdfd %d\n", nfds, watched_rd_fd);
            }
            if ( watched_wr_fd ) { 
                FD_SET(watched_wr_fd, &wfds);
                FD_SET(watched_wr_fd, &efds);
                if ( nfds <= watched_wr_fd ) { nfds = watched_wr_fd + 1; } 
                printf(" select nfds %d  wrfd %d\n", nfds, watched_wr_fd);
            }
        }
        printf(" select nfds %d\n", nfds);
        rc = select(nfds, &rfds, &wfds, &efds, &timeoutval);
        if ( rc < 0 ) {
            printf(" select returned error %d\n", rc);
            break;
        }

        /* self initiated rpc call */
        if ( altsel ) {
            unsigned int tmnow = time(NULL);
            unsigned int tmdiff = tmnow - lastregtime;
            if ( tmdiff > 10 ) {
                dbus_selector_process_post(conn, param, &pending);
                lastregtime = tmnow;
            }
        }

        if ( rc == 0 ) {
            printf(" select returned rc 0 \n");
            continue;
        }
        /* some event happened */
        printf(" select returned rc %d \n", rc);
        if ( watched_watch != NULL ) {
            if ( watched_rd_fd ) { 
                if ( FD_ISSET(watched_rd_fd, &rfds) ) {
                    printf(" select returned calls watch_handle\n");
                    dbus_watch_handle(watched_watch, DBUS_WATCH_READABLE);
                    printf(" select returned calls process_recv\n");
                    dbus_selector_process_recv(conn, pending==NULL?0:1,
                                                     &pending);
                    printf(" select returned done process_recv\n");
                }
                if ( FD_ISSET(watched_rd_fd, &efds) ) {
                    printf(" select returned exception with rd fd %d \n",
                           watched_rd_fd);
                }
            }
            if ( watched_wr_fd ) { 
                if ( FD_ISSET(watched_wr_fd, &wfds) ) {
                    dbus_watch_handle(watched_watch, DBUS_WATCH_WRITABLE);
                }
                if ( FD_ISSET(watched_wr_fd, &efds) ) {
                    printf(" select returned exception with wr fd %d \n",
                           watched_wr_fd);
                }
            }
        }

    }
   return ret;
}

static int dbus_selector_process_recv(DBusConnection* conn, int iswaiting_rpcreply,
                                      DBusPendingCall** pendingargptr)
{
    int ret = 1; /* default fail */

    dbus_connection_read_write(conn, 2);
    DBusDispatchStatus dispatch_rc = dbus_connection_get_dispatch_status(conn);
    if ( DBUS_DISPATCH_DATA_REMAINS != dispatch_rc ) {
            printf(" error no message pending \n");
    }
    while( DBUS_DISPATCH_DATA_REMAINS == dispatch_rc ) {
        DBusMessage* msg = dbus_connection_borrow_message(conn);
        if ( msg == NULL ) {
            printf(" error pending check FAILED: remains but "
                            "no message borrowed. \n");
            break;
        }
        int mtype = dbus_message_get_type(msg);
        if ( mtype == DBUS_MESSAGE_TYPE_METHOD_RETURN ) {
            if ( iswaiting_rpcreply ) {
                printf(" rpc pending check SUCCESS: received rpc reply \n");
                dbus_connection_return_message(conn, msg);
                msg = NULL;
                dbus_selector_process_post_reply( conn, pendingargptr );
                printf(" rpc pending check SUCCESS: processed rpc reply \n");

            } else {
                printf(" rpc pending check FAILED: received rpc reply \n");
            }
        } else if ( mtype == DBUS_MESSAGE_TYPE_ERROR ) {
            if ( iswaiting_rpcreply ) {
                printf(" rpc pending check SUCCESS: received rpc ERROR \n");
            } else {
                printf(" rpc pending check FAILED: received rpc ERROR \n");
            }
        } else if ( mtype == DBUS_MESSAGE_TYPE_SIGNAL ) {
                printf(" signal pending check SUCCESS: received and drop \n");
                dbus_connection_steal_borrowed_message(conn, msg);
                dbus_message_unref(msg);
        } else if ( mtype == DBUS_MESSAGE_TYPE_METHOD_CALL ) {
                printf(" rpc pending check SUCCESS: received rpc call. \n");
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
static int dbus_selector_process_post(DBusConnection* conn, char * param,
                                      DBusPendingCall** pendingargptr)
{ /* mostly a copy of query() */
   DBusMessage* msg = NULL;
   DBusMessageIter args = {0};
   DBusError err = {0};
   DBusPendingCall* pending = NULL;
   int ret = 0;
   dbus_bool_t stat = FALSE;
   dbus_uint32_t level = 0;

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

   dbus_connection_flush(conn);
   printf("Request flushed\n");

   // free message
   dbus_message_unref(msg);
   * pendingargptr = pending;
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
   if (3 >= argc && NULL != argv[2]) param = argv[2];
   if (0 == strcmp(argv[1], "send"))
      sendsignal(param);
   else if (0 == strcmp(argv[1], "receive"))
      receive();
   else if (0 == strcmp(argv[1], "listen"))
      listen();
   else if (0 == strcmp(argv[1], "query"))
      query(param, 0);
   else if (0 == strcmp(argv[1], "selector"))
      dbus_selector(param, 0);
   else if (0 == strcmp(argv[1], "seltest"))
      query(param, 1);
   else if (0 == strcmp(argv[1], "selpost"))
      dbus_selector(param, 1);
   else {
      printf ("Syntax: dbus-select [[send|receive|listen|query]|"
                        "[selector|seltest|selpost]] [<param>]\n");
      return 1;
   }
   return 0;
}

