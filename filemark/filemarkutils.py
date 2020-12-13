from .              import filemarkutils    as _utils
from os             import kill             as _os_kill, 
from os             import getppid          as _os_getppid
from os.path        import exists           as _isValid
from tabulate       import tabulate         as _tabulate
import argparse                             as _argparse

from signal         import SIGHUP           as _SIGHUP

_parser = _argparse.ArgumentParser()

_parser.add_argument(
	"ITEM"              ,
	nargs = "*"         ,
	help="The Folder/File to Bookmark"
)
_parser.add_argument(
	"-a"                ,
	"--add"             ,
	action="store_true" ,
	default=True		,
	help="Bookmark the specific folder"
)
_parser.add_argument(
	"-v"                , 
	"--version"         ,
	action="store_true" , 
	help="Display the version information of filemark."
)
_parser.add_argument(
	"--show-only"       ,
	action="store_true" ,
	help="Show the details of some specific bookarked item."
)
_parser.add_argument(
	"-s"                ,
	"--show"            ,
	"--show-all"        ,
	action="store_true" ,
	help="Show the list of currently bookmarked items."
)

args = _parser.parse_args()

def quitTerminal():
    input("This is Cool !! Press Enter to Exit ...")
    _os_kill(_os_getppid(), _SIGHUP)
