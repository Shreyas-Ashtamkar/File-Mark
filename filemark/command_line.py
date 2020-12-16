from .filemarkutils import args, bookmarkEntry, quitTerminal as _quitTerminal, _isValid, _tabulate, saveBookmark, getBookmarks


# CASE 1 - Display Version
if args.version:
	print("Version 0.1")
	exit(0)


# CASE 2 - Show Only Specific File/Folder
if args.show_only:
	output = getBookmarks(args.ITEM)
	if output == []:
		print(f"None of these found --> {args.ITEM}")
		exit(1)
	else:
		table = _tabulate(
			output, 
			headers=["S.No.","Name", "Path"], 
			tablefmt="pretty", 
		)
		print(table)
		exit(0)


# CASE 3 - Show all the bookmarks
if args.show_all:
	table = _tabulate(
		getBookmarks(), 
		headers=["S.No.","Name", "Path"], 
		tablefmt="pretty", 
		showindex=True
	)
	print(table)
	exit(0)

# CASE 4 - Add a new bookmark to the list, automatically
if args.add:
	fileName = args.ITEM[0]
	saveBookmark(fileName)
