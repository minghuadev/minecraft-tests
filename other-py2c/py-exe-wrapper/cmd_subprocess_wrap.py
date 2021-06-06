#!/usr/bin/env python
# cmd_subprocess_wrap.py

import sys, os, copy, time, threading, subprocess, traceback

_cfg_version = "cmd_wrap version 0.0.1 win32"

_cfg_usage_txt = '''cmd_wrap program
'''

_g_local_env = os.environ.copy()
_cfg_run_sub_py_source = False
_cfg_sub_site_path = None

_g_logfile = None


def logmsg(logfile, *args, **kwargs):
    if _g_logfile is not None:
        p1 = str(repr(args))
        p2 = str(repr(kwargs))
        #print(" type p1: ", type(p1), len(p1))
        #print(" type p2: ", type(p2), len(p2))
        p3 = " args  %s  kwargs  %s \n" % (p1, p2)
        #print(" type p3: ", type(p3), len(p3))
        _g_logfile.write( p3.encode() )
        _g_logfile.flush()


class ProcMonitor(threading.Thread):
    def __init__(self, proc, timeout=0):
        super().__init__()
        self._proc = proc
        self._timeout = timeout
        self._timeout_happened = False
        self._set_stop_requested = False

    def run(self):
        tm1 = time.time()
        while True:
            if self._timeout <= 0:
                break
            time.sleep(0.2)
            tm2 = time.time()
            tdif = tm2 - tm1
            if self._set_stop_requested:
                break
            if tdif > self._timeout:
                try:
                    self._proc.terminate()
                    self._timeout_happened = True
                except:
                    pass
                break

    def set_stop(self):
        self._set_stop_requested = True

    def get_timeouted(self):
        return self._timeout_happened


class SubCmd(object):

    def subcmd(self, cmdstr, timeout=0, logfile=None):
        logmsg(logfile, "subcmd run: %.3f  %s" % ( timeout, cmdstr ))
        tm1 = time.time()
        subenv = None
        if sys.platform == "win32": #
            cmd_raw = cmdstr
            # shlex does not work well with windows path.sep \ so we have to do it manually:
            cmd_segs = [x.strip() for x in cmd_raw.split()]
            cmd_segs = [x for x in cmd_segs if len(x) > 0] # remove blank elements
            if len(cmd_segs) < 1:
                raise RuntimeError("Error, composing win32 command subprocess cmds_arg")
            cmds_arg = cmd_segs
            # also add the special venv dependency path to the env copy:
            if _cfg_run_sub_py_source == True:
                if _cfg_sub_site_path is not None:
                    subenv = _g_local_env.copy()
                    python_path = subenv.get('PYTHONPATH', None)
                    if python_path is None:
                        python_path = _cfg_sub_site_path
                    else:
                        python_path = _cfg_sub_site_path + os.pathsep + python_path
                    subenv['PYTHONPATH'] = python_path
                else:
                    raise RuntimeError("site package path not configured properly")
        else:
            raise RuntimeError("non-win32 platform not supported")

        proc_ok = None
        out_lines = []
        mon = None
        try:
            proc = subprocess.Popen(cmds_arg,
                                    env=subenv,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            proc_pid = proc.pid
            logmsg(logfile, "subcmd pid: %s" % ( str(proc_pid) ))
            tmp_mon = ProcMonitor(proc, timeout=timeout)
            tmp_mon.start()
            mon = tmp_mon
            while True:
                line = proc.stdout.readline()
                if not line:
                    mon.set_stop()
                    break
                line = line.decode()
                out_lines.append(line)
                #print("subcmd-print: " + line.rstrip())
                short_line = line.rstrip('\r\n')
                print(short_line)
            proc_ok = True
        except Exception as e:
            lmsg = " Exception: %s" % str(e)
            #traceback.print_exception( sys.exc_info() )
            logmsg(logfile, lmsg)
            #print(lmsg)
        except:
            lmsg = " Exception: unknown"
            logmsg(logfile, lmsg)
            #print(lmsg)

        tm3 = time.time()
        tdif = tm3 - tm1
        logmsg(logfile, "subcmd cost: %.3f ,  output lines %d" % ( tdif, len(out_lines) ))
        if mon is not None:
            mon.set_stop()
            mon.join(0.3)

        proc_ret_code = None
        if proc_ok:
            proc.terminate() # just blindly call it to make sure it terminates
            try:
                r_wait = proc.wait(0.1) # need to call or the process go defunct
                logmsg(logfile, "subcmd proc wait: %s" % ( str(r_wait) ))
                proc_ret_code = proc.returncode
            except:
                logmsg(logfile, "subcmd proc wait: exception")
        else:
            logmsg(logfile, "subcmd proc wait: no action due to no proc_ok")
        logmsg(logfile, "subcmd proc returncode", proc_ret_code)

        mon_err_terminate = None
        mon_err_timeout = None
        if mon is not None:
            mon_err_terminate = mon.is_alive()
            mon_err_timeout = mon.get_timeouted()
        logmsg(logfile, "subcmd timeouted terminate: %s %s" % (
                    mon_err_timeout, mon_err_terminate))
        errs = None
        if mon_err_timeout or mon_err_terminate:
            errs = [mon_err_timeout, mon_err_terminate]
            logmsg(logfile, "Error: subcmd errs: %s" % errs)
            if mon_err_terminate:
                logmsg(logfile, "Critical error: subcmd proc error!")
        if timeout > 0 and timeout < 0.1:
            raise RuntimeError("timout too small")
        logmsg(logfile, "subcmd done")
        return [errs, out_lines, tdif, timeout, proc_ret_code]


def package_main(logfile=None):
    logmsg(logfile, "\ncmd_wrap version %s" % _cfg_version)
    rc = 0 # default ok

    argc = len(sys.argv)
    if argc >= 1:
        cmd_arg0 = copy.deepcopy(sys.argv[0])
        wk_dir = os.path.abspath(os.path.dirname(cmd_arg0))
        cur_dir = os.getcwd()
        wk_dir = os.path.relpath(wk_dir, cur_dir)
        logmsg(logfile, "cmd_wrap  cur_dir %s  wk_dir %s" % (cur_dir, wk_dir))
        #os.chdir(wk_dir)
        the_cmd = wk_dir + os.path.sep + "cmd_orig.exe"

        arg0 = copy.deepcopy(sys.argv[0])
        logmsg(logfile, "cmd_wrap  arg0", str(arg0))
        del(sys.argv[0])
        for x in sys.argv:
            the_cmd += " " + x
        logmsg(logfile, "")

        errs, out_lines, tdif, touted, pret_c = SubCmd().subcmd(the_cmd, timeout=30)

        logmsg(logfile, "")
        logmsg(logfile, "cmd_wrap subcmd errs       ", errs)
        logmsg(logfile, "cmd_wrap subcmd out_lines  ", len(out_lines))
        logmsg(logfile, "cmd_wrap subcmd tdif       ", "%.3f" % tdif)
        logmsg(logfile, "cmd_wrap subcmd timeouted  ", touted)
        logmsg(logfile, "cmd_wrap subcmd proc rc    ", pret_c)

        if errs is not None or pret_c != 0:
            logmsg(logfile, "cmd_wrap failed due to errs is not None or proc rc not 0")
            rc = 1

        cur_dir2 = os.getcwd()
        logmsg(logfile, "cmd_wrap  cur_dir %s" % (cur_dir2))
        os.chdir(cur_dir)
    else:
        logmsg(logfile, "cmd_wrap argc < 1")
        logmsg(logfile, "cmd_wrap argc < 1 - done")
        rc = 1
    return rc


if __name__ == '__main__':

    cur_dir = os.getcwd()
    base_path = getattr(sys, '_MEIPASS', cur_dir)
    #print("base_path", base_path)
    cmd_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    #print("cmd_dir", cmd_dir)

    #logfilename = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + "cmd_wrap_log.txt"
    logfilename = cmd_dir + os.path.sep + "cmd_wrap_log.txt"
    #print("logfilename", logfilename)
    with open(logfilename, "ab") as logfile:
        _g_logfile = logfile
        rc = package_main(logfile=logfile)
        logmsg(logfile, "cmd_wrap __main__ rc: ", rc)
        _g_logfile = None
        logfile.close()


    ''' use the bash script in cygwin to create a pyinstaller bat file for win32
        verified with auto-py-to-exe 2.9.0 pyinstaller 4.3
        
#!/bin/bash
# rel-gen-cmd-wrap.bash

cat << EOF2 > rel_bat_cmd_wrap.bat
pyinstaller --noconfirm --onefile --console \
    "cmd_subprocess_wrap.py"
EOF2
    '''

