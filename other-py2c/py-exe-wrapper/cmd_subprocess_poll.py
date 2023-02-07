
import subprocess, time, os, fcntl

def subcommand(cmd, timeout=10, debug=False):

    if timeout > 60: timeout = 60
    if timeout < 1: timeout = 1

    if debug:
        print(" cmd ", cmd)

    tm1 = time.time()

    #cmd = ["tail", "-3", '/var/log/messages']
    #cmd = ["/bin/sh", "-c", "date; sleep 1; date"]
    subcmd = ["/bin/sh", "-c", cmd]
    proc = subprocess.Popen(subcmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    poll_cnt = 0
    poll_st = None # init to None
    while True: # loop waiting till cmd finish or timeout
        poll_cnt += 1
        st = proc.poll()
        if debug:
            print(" polling ... ", poll_cnt, st)
        if st is not None:
            poll_st = st
            break # process finished
        tm2 = time.time()
        if tm2 - tm1 >= timeout:
            break
        time.sleep(0.1)
    output = None
    if poll_st is not None:
        output = proc.stdout.read().decode()
    if debug:
        print("Output: \n", output )
    tm2 = time.time()
    if debug:
        print(" cost: %.3f" % (tm2 - tm1))

    return [poll_st, tm2-tm1, output] # poll_st: None,0,non-0


def subcmd_uptime():
    rets, retv = None, 0
    cmd = "uptime"
    result = subcommand(cmd)
    if result[0] is not None:
        rets = result[0]
        lines = result[2].split('\n')
        cmd_out = []
        for i,x in enumerate(lines):
            t = x.strip()
            if type(t) is str and len(t) > 0:
                cmd_out.append( t )
        if len(cmd_out) >= 1:
            retv = cmd_out
        else:
            retv = [""]
    print("rets retv: ", rets, retv) # rets retv:  0 ["13:12:00 "]
    return [rets, retv]


if __name__ == '__main__':
    print(" subcmd_uptime() returned: ", subcmd_uptime() )
    ''' subcmd_uptime() returned:  [0, ["...."]] '''


