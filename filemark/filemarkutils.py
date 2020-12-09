from signal import SIGHUP as _SIGHUP
from os import kill as _os_kill, getppid as _os_getppid

def quitTerminal():
    input("This is Cool !! Press Enter to Exit ...")
    _os_kill(_os_getppid(), _SIGHUP)
