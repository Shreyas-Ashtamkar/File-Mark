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



if args.open:
	bm_list = getBookmarks(args.ITEM)
	bm_count = len(bm_list)
	table = _tabulate(
		getBookmarks(args.ITEM),
		headers=["S.No.", "Name", "Path"],
		tablefmt="pretty",
		showindex=True
	)

	if bm_count == 1:
		print("opening : ", bm_list[0][2])
	elif bm_count > 1:
		print(f"Error : The Argument Suites Multiple Answers. ")
		print("\n\nPlease Choose the exact number. ")
		print(table)
	else:
		print(f"Error : Not Found {bm_list}")
		print("\n\nAvailable options: ")
		print(table)

		
