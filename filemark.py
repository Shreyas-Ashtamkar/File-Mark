import os
import signal

input("This is Cool !! Press Enter to Exit ...")

os.kill(os.getppid(), signal.SIGHUP)
