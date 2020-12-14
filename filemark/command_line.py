from .filemarkutils import args, bookmarkEntry, quitTerminal as _quitTerminal, _isValid, _tabulate


# CASE 1 - Display Version
if args.version:
    print("Version 0.1")
    exit(0)


# CASE 2 - Show Only Specific File/Folder
if args.show_only:
	print("Still Running")
	exit(0)


if args.show:
    with open(".bookmarks") as bm_file:
        table = _tabulate([row.split('|') for row in bm_file.readlines()], headers=["S.No.","Name", "Path"], tablefmt="pretty", showindex=True)
        print(table)
    exit(0)

print("\n\n\n", args.add)

if args.add:
    with open(".bookmarks", 'a') as bm_file:
        bm_file.write(bookmarkEntry(args.ITEM[0]))
    exit(0)
