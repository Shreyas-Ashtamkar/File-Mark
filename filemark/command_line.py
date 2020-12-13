from .filemarkutils import args, quitTerminal
from os.path import exists as _isValid
from tabulate import tabulate

# CASE 1
# Display Version

if args.version:
    print("Version 0.1")
    exit(0)

if args.show_only:
	print("Still Running")
	exit(0)

if args.show:
    with open(".bookmarks") as bm_file:
        table = tabulate([row.split(',') for row in bm_file.readlines()], headers=["S.No", "Name", "Path"], tablefmt="pretty")
        print(table)
    exit(0)
