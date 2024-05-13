#!/usr/bin/env python
# python-sys-stdout-redirect.py

import sys
import threading


class SysTeeCapturePrints(object):
    def __init__(self, file_hdl, file_lock, old_std_out, old_out_prefix):
        self._out_file = file_hdl
        self._out_file_lock = file_lock
        self._old_std_out = old_std_out
        self._old_out_prefix = old_out_prefix
        self._buffer = None

    def write(self, msg):
        if len(msg) < 1:
            return

        self._out_file_lock.acquire()

        do_write = False
        if msg.endswith("\n"):
            if self._buffer is None:
                out_msg = self._old_out_prefix + " " + msg
            else:
                out_msg = self._old_out_prefix + " " + self._buffer + msg
                self._buffer = None

            do_write = True
        else:
            if self._buffer is None:
                self._buffer = msg
            else:
                self._buffer += msg

        if do_write:
            self._out_file.write(out_msg)
            self._out_file.flush()
            self._old_std_out.write(out_msg)
            self._old_std_out.flush()

        self._out_file_lock.release()


class SysTeeScreenPrints(object):
    def __init__(self, log_file_name):
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        self._out_f_lock = threading.Lock()
        self._out_file = None
        try:
            tmp_fh = open(log_file_name, "w")
            self._out_file = tmp_fh
        except Exception as ex:
            print("Error in SysTeeScreenPrints. Exception: ", repr(ex))
        except:
            print("Error in SysTeeScreenPrints. Exception: unknown")
        if self._out_file is None:
            return
        self._stdout_redirect = SysTeeCapturePrints(
            self._out_file, self._out_f_lock, self._old_stdout, "STDOUT")
        self._stderr_redirect = SysTeeCapturePrints(
            self._out_file, self._out_f_lock, self._old_stdout, "STDERR")
        sys.stdout = self._stdout_redirect
        sys.stderr = self._stderr_redirect

    def close(self):
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr
        if self._out_file is not None:
            self._out_file.close()
            self._out_file = None


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == '__main__':

    print("line before redirect")
    eprint("error before redirect")

    tee_instance = SysTeeScreenPrints("log-screen-output")

    print("line 1")
    eprint("error 1")

    print("line 2")
    eprint("error 2")

    tee_instance.close()

    print("line beyond redirect")
    eprint("error beyong redirect")

