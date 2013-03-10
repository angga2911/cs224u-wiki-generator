def combine_rc():
	rpath = 'relatedness.txt'
	if not os.path.isfile(rpath):
		print "no r file"
		return
	rfile = open(rpath, 'r')
	save = rfile.read()
	temp = 'r =' + save
	exec temp
	
	cpath = '../jason_files/commonness.txt'
	if not os.path.isfile(cpath):
		print "no c file"
		return
	cfile = open(cpath, 'r')
	save = cfile.read()
	temp = 'c =' + save
	exec temp
	
	# Now r is a list in this structure [