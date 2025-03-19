#
#https://github.com/supernifty/port-forwarder/blob/master/forward-tcp.py

import socket
import time
import threading

# listening on ip address and port
listen_host = "192.168.1.11"
listen_port = 8080

# forwarding to local port
target_host = "127.0.0.1"
target_port = 18080


_g_tm00 = time.time()


def main():
    global _g_tm00
    _g_tm00 = time.time()

    the_server_thread = TheServer()
    the_server_thread.start()


class TheServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._clients = {}

        self._timeout = 70

    def run(self):

        while True:
            dock_socket = None
            try:
                tmp_dock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dock_socket = tmp_dock
                dock_socket.bind((listen_host, listen_port)) # listen
                dock_socket.listen(5)

                t_now = time.time()
                age = t_now - _g_tm00

                print("*** %.3f listening on %s:%i" % ( age, listen_host, listen_port ))

                while True:
                    try:
                        client_socket, client_address = dock_socket.accept()
                        client_ip = client_address[0]
                        client_port = client_address[1]
                        client_desc = "%s:%d" % (client_ip, client_port)
                        server_desc = "%i" % listen_port

                        client_socket.settimeout(self._timeout)

                        t_now = time.time()
                        age = t_now - _g_tm00

                        print("*** %.3f from %s:%s to %s:%i" % (age,
                                                               client_desc, server_desc,
                                                               target_host, target_port ))
                        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server_socket.connect((target_host, target_port))

                        self._lock.acquire()
                        self._lock.release()

                        the_2rmt_desc = "server %s -> remote %s" % (server_desc, client_desc)
                        the_2local_desc = "remote %s -> server %s" % (client_desc, server_desc)

                        thread1 = TheForwarder(client_socket, server_socket, the_2rmt_desc, self)
                        thread2 = TheForwarder(server_socket, client_socket, the_2local_desc, self)
                        thread1.start()
                        thread2.start()
                    finally:
                        pass
            finally:
                if dock_socket is not None:
                    break


class TheForwarder(threading.Thread):
    def __init__(self, rx_sock, tx_sock, description, the_parent):
        super().__init__()
        self._rx_sock = rx_sock
        self._tx_sock = tx_sock
        self._description = description
        self._the_parent = the_parent
        self._started_ok = None
        self._finished_ok = None

    def run(self):
        self._started_ok = True
        while True:
            try:
                data = self._rx_sock.recv(1024)

                t_now = time.time()
                age = t_now - _g_tm00

                print("*** %.3f %s: data: %s" % (age, self._description,
                                                 #repr(data) ) )
                                                 str(len(data))))

                if data:
                    self._tx_sock.sendall(data)
                else:
                    break
            except:
                break
        try:
            t_now = time.time()
            age = t_now - _g_tm00

            print("*** %.3f %s: shutdown" % (age, self._description))
            self._rx_sock.shutdown(socket.SHUT_RD)
            self._tx_sock.shutdown(socket.SHUT_WR)
            #self._rx_sock.close()
            #self._tx_sock.close()
        except:
            pass

        self._finished_ok = True


if __name__ == '__main__':
    main()

