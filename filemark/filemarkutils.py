from typing import List
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
	help="Bookmark the specific folder"
)
_parser.add_argument(
	"-v"                , 
	"--version"         ,
	action="store_true" ,
	help="Display the version information of filemark."
)
_parser.add_argument(
	"-s"                ,
	"--show"            ,
	action="store_true" ,
	help="Smart 'show' option, shows the results if asked to search else throws entire list on screen."
)
_parser.add_argument(
	"--show-only"       ,
	action="store_true" ,
	help="Show the details of some specific bookarked item."
)
_parser.add_argument(
	"--show-all"        ,
	action="store_true" ,
	help="Show the entire list of currently bookmarked items."
)
_parser.add_argument(
	"--detailed"        ,
	action="store_true" ,
	help="Show extra detailed output "
)




# Collect Arguments and count ITEMS
args	= _parser.parse_args()
argc	= len(args.ITEM)

if not any((args.add, args.show, args.version, args.show_only, args.show_all)):
	args.add = True
elif args.show:
	if any((args.version, args.show_only, args.show_all, args.add)):
		raise Exception("incompatible options")
	elif argc > 0:
		args.show = False
		args.show_only = True
	elif argc == 0:
		args.show = False
		args.show_all = True

# CHECK ERRORS
_WMESG = []

# for debugging
# print(args)

try:
	if args.add:
		if any((args.version, args.show_only, args.show, args.detailed, args.show_all)):
			raise Exception("incompatible options")
		elif argc < 1:
			raise Exception("--add requires a file/folder as an argumet to bookmark")
		elif argc > 1:
			_WMESG.append("Too many Items in --add. using ONLY the first argument.")

	elif args.version:
		if any((args.add, args.show_only, args.show, args.show_all)):
			raise Exception("incompatible options")
		elif argc > 0:
			raise Exception("--version takes no arguments")
	

	elif args.show_only:
		if any((args.version, args.add, args.show, args.show_all)):
			raise Exception("incompatible options.")
		elif argc < 1:
			raise Exception("--show-only requires atleast \n\t\t one argument to show the details of. \n\n Did you mean --show-all ?")
	
	elif args.show_all:
		if any((args.version, args.add, args.show, args.show_only)):
			raise Exception("incompatible options.")
		elif argc > 1:
			raise Exception("--show-all takes no arguments.\n\n Did you mean --show-only ?")
	
	else:
		print("UNREACHABLE FROM CODE. FATAL")
		exit(1)


except Exception as e:
	_parser.error("<FATAL> " + str(e) + "\n\nFor additional help type filemark -h") 



#display all the warning messages
for msg in _WMESG:
	print("<WARNING> :",msg)




def _getPath(fileName:str = None) -> any:
	if _isValid(fileName):
		return _abspath(fileName)
	else:
		return None


# Accessible from external Files



def quitTerminal():
    input("This is Cool !! Press Enter to Exit ...")
    _os_kill(_os_getppid(), _SIGHUP)



def bookmarkEntry(fileName:str = None) -> any:
	if fileName is None:
		raise Exception("fileName cannot be None")
	
	filePath = _getPath(fileName)

	return "\n" + fileName + "|" + filePath



def getBookmarks(selector:str=None) -> any:
	'''
	Show the bookmarks stored over time by the user.
	'''
	with open(".bookmarks") as bm_file:
		table = []
		for row in bm_file.readlines():
			row = row.replace('"', '')
			row = row.strip().split('|')
			if len(row) == 2:
				bm_name, bm_path = row
				bm_path = bm_path.split('/')
				if len(bm_path)>4 and not args.detailed:
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
						no, bm_name, bm_path = no,table[no][0],table[no][1]
						small_table.append([no, bm_name, bm_path])
				else:
					for i, row in enumerate(table):
						bm_name, bm_path = row
						if search_item in bm_name:
							small_table.append([i+1, bm_name, bm_path])
			return small_table
		
		elif isinstance(selector, str):
			for index, bm_path, bm_name in enumerate(table):
				if bm_name == selector:
					selector = index
					break
			else:
				return table
					
			return [table[selector]]
		else:
			return table
		


def saveBookmark(fileName:str = None) -> bool:
	'''
	Store a new bookmark

	param:
		`fileName`: Name of the file/folder to bookmark
	'''

	if fileName is None:
		raise TypeError("fileName cannot be None")

	if not _isValid(fileName):
		raise FileNotFoundError(fileName+" Not found.")
		
	with open(".bookmarks", 'a') as bm_file:
		bm_file.write(bookmarkEntry(fileName))
