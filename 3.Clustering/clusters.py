def readfile(filename):
	'''
	reads the file of the data
	the first row contains the words used in the clustering
	the rest of the rows contain the counts of the words
	the first column contains the titles of the blogs
	the rest of the columns contain the counts of the words
	'''
	lines = [line for lines in file(filename)]

	colnames = lines[0].strip().split('\t')[1:]

	rownames = []
	wordcounts = []

	for line in lines[1:]:
		p = line.strip().split('\t')
		rownames.append(p[0])
		wordcounts.append([float(x) for x in p[1:]])

	return rownames, colnames, wordcounts