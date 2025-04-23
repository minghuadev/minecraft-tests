#!/usr/bin/env python
#

# env: base python 3.11.9 on windows 10.
#   other venv packages:
#       bottle            0.13.3
#       cffi              1.17.1
#       clr_loader        0.2.7.post0
#       pip               24.0
#       proxy_tools       0.1.0
#       pycparser         2.22
#       pythonnet         3.0.5
#       pywebview         5.4
#       setuptools        65.5.0
#       typing_extensions 4.13.2
# source: github.com/r0x0r/pywebview
# home: https://pywebview.flowrl.com/
# 2025-4-22

import webview
from threading import Thread
import time
from webview.dom import ManipulationMode


_cfg_url1=('pywebview docs', 'https://pywebview.flowrl.com')
_cfg_url_to_show = _cfg_url1


_g_win1inst = None
_g_win1loaded = None
_g_auths = [None, None] # [<access_token>, <access_key>]
_g_win1loc = None

def update_auths(w1inst):
    try:
        # github issue search: localStorage
        # https://github.com/r0x0r/pywebview/issues/668
        #v1 = w1inst.evaluate_js("window.localStorage")
        v11 = w1inst.evaluate_js("window.localStorage.getItem('access_token')")
        v12 = w1inst.evaluate_js("window.localStorage.getItem('access_key')")
        v1 = None
        if type(v11) is str and type(v12) is str:
            if len(v11) > 0 and len(v12) > 0:
                v1 = {"access_token":v11, "access_key":v12}
        if type(v1) is dict:
            v1k = v1.keys()
            if "access_token" in v1k and "access_key" in v1k:
                acc_tok = v1.get("access_token", None)
                acc_exp = v1.get("access_key", None)
                if acc_tok is not None and acc_exp is not None:
                    if acc_tok != _g_auths[0] and acc_exp != _g_auths[1]:
                        _g_auths[0] = acc_tok
                        _g_auths[1] = acc_exp
                        print("DataPoller: v1 token ", repr(acc_tok),
                              " ", repr(acc_exp))
    except Exception as ex:
        print("Exception for localStorage: ", repr(ex))
    except:
        print("Exception for localStorage: <unlnown>")

def update_loc(w1inst):
    try:
        # github issue search: localStorage
        # https://github.com/r0x0r/pywebview/issues/668
        v1 = w1inst.evaluate_js("window.document.location")
        if type(v1) is dict:
            v1k = v1.keys()
            if "hostname" in v1k:
                hn = v1.get("hostname", None)
                global _g_win1loc
                if hn is not None and hn != _g_win1loc:
                    _g_win1loc = hn
                    print("DataPoller: v1 loc ", repr(hn))
    except Exception as ex:
        print("Exception for document.location: ", repr(ex))
    except:
        print("Exception for document.location: <unlnown>")

def show_loc(win1inst, loc): # return True for ok, None for failure
    retv = None
    base_id = 'MyExampleLocElement'
    try:
        base_elem = win1inst.dom.get_element("#" + base_id)  # returns a first matching Element or None
        if base_elem is None:
            #print("Show loc: create new ...")
            new_content = '<div id="%s"><H3>My Example Loc Elelemt</H3></div>' % base_id
            new_elem = win1inst.dom.create_element(new_content)  # insert a new element as body's last child
            element = win1inst.dom.create_element('<p>loc: %s</p>' % str(loc),
                                                  parent = new_elem,
                                                  mode = ManipulationMode.LastChild) # insert a new element
        else:
            #print("Show loc: insert to existing ...")
            element = win1inst.dom.create_element('<p>loc: %s</p>' % str(loc),
                                      parent=base_elem,
                                      mode=ManipulationMode.LastChild)  # insert a new element
        retv = True
    except Exception as ex:
        print("Exception for show loc: ", repr(ex))
    except:
        print("Exception for show loc: <unknown>")
    #print("Show loc: done")
    return retv

class DataPoller(Thread):
    def __init__(self):
        super().__init__()
        self._user_started = None
        self._user_finished = None
        self._stop_requested = None

    def set_stop(self):
        self._stop_requested = True

    def run(self):
        self._user_started = True
        time.sleep(0.1)
        loop_count = 0
        while True:
            loop_count += 1
            if self._stop_requested is not None:
                break
            time.sleep(0.2) # pace 0.2s
            poll_interval_count = 10 # 10: 10 * 0.2s = 2s
            while True: # scope
                if (loop_count % poll_interval_count) != 1: break # scope
                # below runs once every poll interval

                w1inst = _g_win1inst
                w1loaded = _g_win1loaded
                if w1inst is None: break # scope
                if w1loaded is None: break # scope
                # below runs only if the page has been loaded at least once

                update_auths(w1inst)

                prev_loc = _g_win1loc
                update_loc(w1inst)
                if _g_win1loc is not None and _g_win1loc != prev_loc:
                    show_loc(w1inst, _g_win1loc)

                if (loop_count % (poll_interval_count * 10)) != 1: break # scope
                # below runs once every 10 poll intervals
                if _g_win1loc is not None and len(_g_win1loc) > 0:
                    show_loc(w1inst, _g_win1loc)

                break # scope

        self._user_finished = True
        print("DataPoller: finished")

data_poller = DataPoller()
data_poller.start()


webview.settings['REMOTE_DEBUGGING_PORT'] = 13341

# window 1, the user content
window1 = webview.create_window(_cfg_url_to_show[0], _cfg_url_to_show[1])
def window1handler_loaded():
    print("Window 1 location loaded: %s, %s" % (str(window1.original_url),
                                                str(window1.real_url)) )
    global _g_win1inst, _g_win1loaded
    _g_win1inst = window1
    prev_loaded = _g_win1loaded
    _g_win1loaded = True
    if prev_loaded != True:
        show_loc(window1, str(window1.real_url))
window1.events.loaded += window1handler_loaded

# window 2, the info about window 1
show_win2 = False
if show_win2 == True:
    window2content = "<h1>Woah dude!</h1>" + \
            "<p href=\"" + _cfg_url_to_show[1] + "\">" + \
                _cfg_url_to_show[1] + \
            "</p>"
    window2 = webview.create_window("WebViewInfo", html=window2content)
    # window events: closed, closing, loaded, before_load, before_show, shown,
    # minimized, maximized, restored, resized, moved
    def window2handler():
        print("There are %d windows" % len(webview.windows))
        act_win = webview.active_window()
        if act_win is not None:
            print("Active window: %s" % str(act_win.title))
        else:
            print("Active window: <empty>")
    window2.events.shown += window2handler

print("Main: starting...")
webview.start(debug=True)
print("Main: all done.")

