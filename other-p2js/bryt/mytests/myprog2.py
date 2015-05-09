
    import sys
    import traceback

    from browser import document
    from browser import alert
    import time

    def write(data):
        document['code'].value += data
    sys.stdout.write = sys.stderr.write = write

    def echo(event):
                N = 10000
                a = 0
                tm0 = time.time()
                for i in range(0,N):
                    a += 1
                tms = time.time() - tm0

                ostr = " == %s  %s  %s == " % (document["zone"].value, tm0, tms)
                #print "abcd"
                #print "ostr", ostr
                #print
                sys.stdout.write(ostr)
                alert(ostr)
                assert 0, "hhhhhhhhhhhhhh errrrrrrrr %s " % tms


    document['mybutton'].bind('click', echo)


    #console.html:
    #    <input id="zone"></input><button id="mybutton">click !</button>

