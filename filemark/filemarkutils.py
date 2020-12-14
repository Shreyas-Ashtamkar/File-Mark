from .              import filemarkutils    as _utils
from os             import kill             as _os_kill
from os             import getcwd           as _pwd
from os             import getppid          as _os_getppid
from os.path        import exists           as _isValid
from os.path        import abspath          as _abspath
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


def _getPath(fileName:str = None) -> any:
	if _isValid(fileName):
		return _abspath(fileName)
	else:
		return None





# Collect Arguments and count ITEMS
args	= _parser.parse_args()
argc	= len(args.ITEM)


# CHECK ERRORS
_ERROR = False
_EMESG = "Other Error"


if any((args.add, args.show_only)) and argc < 1:
	_ERROR = True
	_EMESG = "\n<FATAL> File / Folder not supplied"

if not args.add and argc > 1:
	_EMESG = "\n<WARNING> Only using the first supplied Folder/File to bookmark."


if _ERROR:
	_parser.error(_EMESG + "\n\n for help type filemark -h")









# Accessible from external Files

def quitTerminal():
    input("This is Cool !! Press Enter to Exit ...")
    _os_kill(_os_getppid(), _SIGHUP)

def bookmarkEntry(fileName:str = None) -> any:
	if fileName is None:
		raise Exception("fileName cannot be None")
	
	filePath = _getPath(fileName)

	return filePath + "|" + fileName
	
