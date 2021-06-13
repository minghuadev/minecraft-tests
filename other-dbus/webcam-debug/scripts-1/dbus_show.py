#!/usr/bin/env python
#

import os, sys, time
import logging
from datetime import date
import subprocess
import shlex

if sys.version_info < (3, 5):
    sys.exit("Error: this script requires Python 3.5 or greater.")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_cmd(cmds_in, dryrun=False):
    if not dryrun:
        logging.debug("Running command:\"{}\"".format(cmds_in))
        result = subprocess.run(shlex.split(cmds_in), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.debug("Command output is: \n{}".format(result.stdout.decode('utf-8')))
        logging.debug("Return code is: {}".format(result.returncode))
        return result.returncode, result.stdout.decode('utf-8')
    else:
        logging.debug("If not dryrun, would run: {}".format(cmds_in))
        return 0, ""

def run_cmd_critical(cmds_in, dryrun=False):
    ret, output = run_cmd(cmds_in, dryrun)
    if ret:
        logging.error("Failure to execute command \"{}\", exiting script".format(cmds_in))
        sys.exit(1)
    return output

def get_process_pid(name_in):
    cmd = "dbus-send --system --type=method_call --print-reply " + \
          "--dest=org.freedesktop.DBus " + \
          "/ org.freedesktop.DBus.GetConnectionUnixProcessID string:" + name_in
    rc, lines = run_cmd(cmd)
    if rc != 0:
        return 0 # special pid 0 for an error
    rc = 0 # default fail
    # grep uint32 | sed -e 's/.*uint32 //' | xargs
    for x in lines.split("\n"):
        x = x.strip()
        leading_s = "uint32 "
        if x.startswith(leading_s):
            pid = int(x[len(leading_s):])
            if pid > 2: # cannot be pid 1 or 2
                rc = pid
                break
            print("Error: found no pid: ", x)
    return rc

def get_dbus_all_names():
    cmd = "dbus-send --system --type=method_call --print-reply " + \
          "--dest=org.freedesktop.DBus " + \
          "/org/freedesktop/DBus org.freedesktop.DBus.ListNames"
    rc, lines = run_cmd(cmd)
    names = []
    if rc != 0:
        return names
    # grep 'string "' | sed -e 's/.*string "//' | sed -e 's/".*//'
    for x in lines.split("\n"):
        x = x.strip()
        leading_s = "string \""
        if x.find(leading_s) == 0:
            name = None
            v = x[len(leading_s):]
            if v[-1] == "\"":
                v = v[:-1]
                name = v
            if name is None:
                print("Error: found no name: ", x)
            else:
                names.append(name)
    return names

def get_names_pids(do_show=False):
    results = dict() # keyed to int pid, and value array of 2: main-name, [bus-names]
    results_msglines = []
    all_names = get_dbus_all_names()
    for x in all_names:
        # check if x == ':1.23' and its length
        if x.startswith(":1."):
            # should be 4 to 6, plus a trailing eol
            pat_len = len(x)
        else:
            pat_len=3 # default ok

        if pat_len > 2 and pat_len <= 7:
            pid = get_process_pid(x)
            if pid > 2:
                msg = " ok name pid: %s %s" % (pid, x)
                rpid = results.get(pid, None)
                short_name = True if x.startswith(":1.") else False
                if rpid is None: # new
                    shortnames = [] if not short_name else [x]
                    results[pid] = [None if short_name else x, shortnames]
                else:
                    if not short_name: # long name
                        if results[pid][0] is None:
                            results[pid][0] = x
                        else:
                            results[pid][0] += " + " + x
                    else:
                        results[pid][1].append(x)
            else:
                msg = " skip name %s  pid %s" % (pid, x)
                results_msglines.append(msg)
        else:
            msg = " skip name %s  " % ( x )
            results_msglines.append(msg)
    if do_show:
        for x in sorted(results.keys()):
            print(" ok ", x, "%32s" % results[x][0], results[x][1])
        for x in sorted(results_msglines):
            print(x)
    return results

def show_names_pids():
    get_names_pids(do_show=True)

if __name__ == '__main__':
    show_names_pids()

