from os import kill as _os_kill
from os import getcwd as _pwd
from os import system as _run
from posix import listdir
from subprocess import Popen as _fork_run
from os import listdir as _ls
from os import environ as env
from os import getppid as _os_getppid
from os.path import exists as _isValid
from os.path import isdir as _isDir
from os.path import isfile as _isFile
from os.path import abspath as _abspath
from tabulate import tabulate as _tabulate
import argparse as _argparse

from signal import SIGHUP as _SIGHUP

# GLOBAL_CONSTANTS
SMART_CONTROLS = {
    "ide": {
            "alg" : ["code", "subl", "atom", "gedit","xdg-open"],
            "web" : ["sensible-browser"],
            "med" : ["xdg-open"],
        },
    "ext": {
            "alg" : ["py", "py3", "cpp", "java", "js", "php", "c", "html", "md"],
            "web" : ["html"],
            "med" : ["jpg", "jpeg", "png", "svg", "webp", "mp4", "mp3", "gif", "mov", "mkv", "flv", "avi", "webm"]
        },
    "url": "https://localhost:8000/"
}

BOOKMARK_STOREAGE = env["HOME"]+"/.bookmarks"
if not _isFile(BOOKMARK_STOREAGE):
    _run("touch "+BOOKMARK_STOREAGE)

_parser = _argparse.ArgumentParser()
_mutulal_exlusion_parser = _parser.add_mutually_exclusive_group()

# Actual Arguments
_parser.add_argument(
    "ITEM",
    nargs="*",
    help="The Folder/File to Bookmark"
)

# Argument Operations
_mutulal_exlusion_parser.add_argument(
    "-v",
    "--version",
    action="store_true",
    help="Display the version information of filemark."
)
_mutulal_exlusion_parser.add_argument(
    "-a",
    "--add",
    action="store_true",
    help="Bookmark the specific folder"
)
_mutulal_exlusion_parser.add_argument(
    "-s",
    "--show",
    action="store_true",
    help="Show the stored bookmarks."
)
_mutulal_exlusion_parser.add_argument(
    "--show-only",
    action="store_true",
    help="Show the details of some specific bookarked item."
)
_mutulal_exlusion_parser.add_argument(
    "--show-all",
    action="store_true",
    help="Show the entire list of currently bookmarked items."
)
_mutulal_exlusion_parser.add_argument(
    "-o",
    "--open",
    action="store_true",
    help="Open A Bookmarked File",
)
_mutulal_exlusion_parser.add_argument(
    "--delete",
    action="store_true",
    help="Delete a bookmark's entry."
)

# Extra Flags
_parser.add_argument(
    "--full-path",
    action="store_true",
    help="Show the entire path"
)
_parser.add_argument(
    "--not-smart",
    action="store_true",
    default=False,
    help="Open A Bookmark only in Terminal",
)


# Collect Arguments and count ITEMS
args = _parser.parse_args()
argc = 0
itmc = len(args.ITEM)
extra_flags = any((args.full_path, args.not_smart))

for arg in args.__dict__:
    if args.__dict__[arg]:
        argc += 1

argc -= int(itmc > 0) + int(extra_flags)

# Custom Exceptions
class CompatibilityError(Exception):
    def __str__(self) -> str:
        return "Incompatible options"

class FilemarkError(Exception):
    pass

# when nothing is given as input
if argc < 1:
    # when items supplied consider that it has to add 
    if itmc > 0:
        args.add = True
    # when no items supplied consider show
    else:
        args.show = True
        args.show_all = True

if args.show:
    if args.not_smart:
        raise CompatibilityError()
    elif itmc > 0:
        args.show_only = True
    else:
        args.show_all = True

# CHECK ERRORS
_WMESG = []

try:
    if args.add:
        if extra_flags:
            raise CompatibilityError()
        elif itmc < 1:
            raise FilemarkError("--add requires a file/folder as an argumet to bookmark")
        elif itmc > 1:
            _WMESG.append("Too many Items in --add. using ONLY the first argument.")

    elif args.version:
        if extra_flags:
            raise CompatibilityError()
        elif itmc > 0:
            raise FilemarkError("--version takes no arguments")

    elif args.delete:
        if extra_flags:
            raise CompatibilityError()
        elif itmc != 1:
            raise FilemarkError("--delete needs exactly one argument of bookmark number or name.")

    elif args.show_only:
        if itmc < 1:
            raise FilemarkError("--show-only requires atleast \n\t\t one argument. \n\n Did you mean --show-all ?")

    elif args.show_all:
        if itmc > 1:
            raise FilemarkError("--show-all takes no arguments.\n\n Did you mean --show-only ?")

    elif args.open:
        if itmc != 1:
            raise FilemarkError("--open needs exactly one argument of bookmark number or name.")
        # We need the argument full-path at any cost
        args.full_path = True

    else:
        raise Exception("UNREACHABLE FROM CODE.")

    # Display all the warning messages
    for msg in _WMESG:
        print("<WARNING> :", msg)

    def _getPath(fileName: str = None) -> any:
        if _isValid(fileName):
            filePath = _abspath(fileName)
            args.full_path = True

            for bms in getBookmarks():
                if bms[1] == filePath:
                    raise Exception(bms[0] +" Already Bookmarked")
            
            return filePath

        else:
            raise FileNotFoundError()

    # Accessible from external Files

    def quitTerminal():
        input("This is Cool !! Press Enter to Exit ...")
        _os_kill(_os_getppid(), _SIGHUP)

    def bookmarkEntry(fileName: str = None) -> any:
        if fileName is None:
            raise Exception("fileName cannot be None")

        filePath = _getPath(fileName)

        if fileName in (".", ".."):
            fileName = filePath.split('/')[-1]

        return "\n" + fileName + "|" + filePath

    def getBookmarks(selector: str = None) -> any:
        '''
        Show the bookmarks stored over time by the user.
        '''
        
        with open(BOOKMARK_STOREAGE) as bm_file:
            table = []
            for row in bm_file.readlines():
                row = row.replace('"', '')
                row = row.strip().split('|')
                if len(row) == 2:
                    bm_name, bm_path = row
                    bm_path = bm_path.split('/')
                    if len(bm_path) > 4 and not args.full_path:
                        bm_path = '.../' + '/'.join(bm_path[-2:])
                    else:
                        bm_path = '/'.join(bm_path)
                    table.append((bm_name, bm_path))

            if selector in (None, ""):
                return table

            elif isinstance(selector, list):
                small_table = []
                for search_item in selector:
                    if search_item.isdigit():
                        no = int(search_item)
                        if no < len(table):
                            no, bm_name, bm_path = no, table[no][0], table[no][1]
                            small_table.append([no, bm_name, bm_path])
                    else:
                        for i, row in enumerate(table):
                            bm_name, bm_path = row
                            if search_item in bm_name:
                                small_table.append([i+1, bm_name, bm_path])
                return small_table

            elif isinstance(selector, str):
                for index, row in enumerate(table):
                    bm_path, bm_name = row
                    if bm_name == selector:
                        selector = index
                        break
                else:
                    return table

                return [table[selector]]
            else:
                return table

    def saveBookmark(fileName: str = None) -> bool:
        '''
        Store a new bookmark

        param:
            `fileName`: Name of the file/folder to bookmark
        '''

        if fileName is None:
            raise TypeError("fileName cannot be None")

        if not _isValid(fileName):
            raise FileNotFoundError(fileName + " Not found.")

        with open(BOOKMARK_STOREAGE, 'a') as bm_file:
            bm_file.write(bookmarkEntry(fileName))

    def openBookmark(bookmarkPath):
        if _isValid(bookmarkPath):
            entirePath = bookmarkPath.split("/")
            endOfPath  = entirePath[-1]

            if _isFile(bookmarkPath):
                folderPath = "/".join(entirePath[:-1])
                ext = [endOfPath.split(".")[-1].lower()]
            else:
                folderPath = bookmarkPath
                ext        = []
                for file in _ls(folderPath):
                    if _isFile(file):
                        ext.append(file.split(".")[-1].lower())
            
            #Terminal_Open
            if _run("command -v gnome-terminal")==0:
                    _fork_run(["gnome-terminal","working-directory=\"" + folderPath + "\""])
            else:
                _fork_run(["x-terminal-emulator","workdir \"" + folderPath + "\""])
            
            open_EXT = set()
            #SMART_FUNCTIONALITY
            if not args.not_smart:
                for fileType in ext:
                    #set open_EXT
                    for e in SMART_CONTROLS['ext']:
                        if fileType in e:
                            open_EXT.add(fileType)

                #Now Actully open every sensibe thing needed for that 
                # e.g. html needs code as well as 
                for e in open_EXT:
                    for i in SMART_CONTROLS['ide'][e]:
                        if _run("command -v " + i) == 0:
                            if e != "med":
                                _fork_run(i+" "+bookmarkPath)
                            else:
                                _fork_run(i+" "+folderPath)

        else:
            raise FileNotFoundError(bookmarkPath + " Not found.")


            #SMART_CONTROLS
            # print("Opening smartly, the folder.")

    def makeTable(items):
        if not items:
            items = []

        return _tabulate(
            items,
            headers=["S.No.", "Name", "Path"],
            tablefmt="pretty",
            showindex=True
        )

except Exception as e:
    _parser.error("<FATAL> " + str(e) +
                  "\n\nFor additional help type filemark -h")
