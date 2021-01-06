from .filemarkutils import BOOKMARK_STOREAGE, args, bookmarkEntry, openBookmark, quitTerminal as _quitTerminal, _isValid, makeTable, saveBookmark, getBookmarks

def main():

	# CASE 1 - Display Version
	if args.version:
		print("Version 0.1.2")
		exit(0)


	# CASE 2 - Show Only Specific File/Folder
	if args.show_only:
		output = getBookmarks(args.ITEM)
		if output == []:
			print(f"None of these found --> {args.ITEM}")
			exit(1)
		else:
			table = makeTable(output)
			print(table)
			exit(0)


	# CASE 3 - Show all the bookmarks
	if args.show_all:
		table = makeTable(getBookmarks())
		print(table)
		exit(0)

	# CASE 4 - Add a new bookmark
	if args.add:
		fileName = args.ITEM[0]
		saveBookmark(fileName)
		exit(0)

	# CASE 5 - Open the bookmarked location
	if args.open:
		bm_list = getBookmarks(args.ITEM)
		bm_count = len(bm_list)
		table = makeTable(getBookmarks(args.ITEM))

		if bm_count == 1:
			bm_path = bm_list[0][2]
			print("opening :", bm_path, "in terminal", "only." if args.not_smart else "also.")
			openBookmark(bm_path)
			
		elif bm_count > 1:
			print(f"Error : The Argument Suites Multiple Answers. ")
			print("\n\nPlease Choose the exact number. ")
			print(table)
		else:
			print(f"Error : Not Found {bm_list}")
			print("\n\nAvailable options: ")
			print(table)
		exit(0)

	# CASE 6 - Delete a bookmark entry.
	if args.delete:
		print("Delete is still unimplemented. \n\nMANUAL : Head over to the file at ->", BOOKMARK_STOREAGE, "and remove the specific line, (for now)")
		exit(0)



if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)
		
