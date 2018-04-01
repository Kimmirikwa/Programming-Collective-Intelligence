# predicting using decision trees. Decision trees are more transparent and therefore easy to understand
# as they appear to be like if and else statements once modeled

from math import log


# example data to be used in the classification
# the data contains user behaviour and the final buying decision for a website
# each value of the outer list if the data for each user, and the inner values
# are the values for a specific user with all values except the last onen being the
# user behaviour. The last one is the buying decision
my_data = [
	['slashdot','USA','yes',18,'None'],
	['google','France','yes',23,'Premium'],
	['digg','USA','yes',24,'Basic'],
	['kiwitobes','France','yes',23,'Basic'],
	['google','UK','no',21,'Premium'],
	['(direct)','New Zealand','no',12,'None'],
	['(direct)','UK','no',21,'Basic'],
	['google','USA','no',24,'Premium'],
	['slashdot','France','yes',19,'None'],
	['digg','USA','no',18,'None'],
	['google','UK','no',18,'None'],
	['kiwitobes','UK','no',19,'None'],
	['digg','New Zealand','yes',12,'Basic'],
	['slashdot','UK','no',21,'None'],
	['google','UK','yes',18,'Basic'],
	['kiwitobes','France','yes',19,'Basic']
]


class decisionnode():
	def __init__(self, col=-1, value = None, tbranch = None, fbranch = None, results = None):
		'''
		col -> is the column index of the criteria to be tested
		value -> the value that the column must match to get a true result
		tbranch -> true branch: None for leaf Nodes
		fbranch -> false branch: None for leaf Nodes
		result -> the final decision: will be None except for the leaf Node
		'''
		self.col = col
		self.value = value
		self.tbranch = tbranch
		self.fbranch = fbranch
		self.results = results


def divideset(rows, column, value):
	'''
	divides the rows on the specified column based on the value
	the value can be numeric or nomal
	'''
	split_function = None  # to be used in splitting the row into 2 sets
	if isinstance(value,int) or isinstance(value,float):
		split_function = lambda row : row[column] >= value
	else:
		split_function = lambda row : row[column] == value

	set1 = [row for row in rows if split_function(row)]  # true values
	set2 = [row for row in rows if not split_function(row)]  # false values

	return set1, set2


def getuniquecounts(rows):
	'''
	gets the number of unique itesm in the rows
	'''
	result_counts = {}

	for row in rows:
		r = row[len(row) - 1]  # the result is in the last column
		result_counts.setdefault(r, 0)
		result_counts[r] += 1

	return result_counts


def giniimpurity(rows):
	'''
	calculates the impurity between the rows
	'''
	total = len(rows)
	counts = getuniquecounts(rows)

	imp = 0
	for k1 in counts:
		p1 = float(counts[k1]) / total
		for k2 in counts:
			if k1 == k2:
				continue
			p2 = float(counts[k2]) / total
			imp += p1 * p2

	return imp # imp will be zero if there is only one unique result in the rows


def entropy(rows):
	# log to base n of x is given by log(x) / log (n)
	log2 = lambda x: log(x) / log(2)

	counts = getuniquecounts(rows)

	entrop = 0.0
	for k in counts.keys():
		p = float(counts[k]) / len(rows)
		entrop -= p * log2(p)

	return entrop # will be 0 if rows have the same result


def buildtree(rows, scoreref = entropy):
	'''
	constructs the tree form the rows of data
	'''
	if len(rows) == 0:
		return decisionnode()

	current_score = scoreref(rows)

	# variables to track the best criteria
	best_gain = 0.0
	best_criteria = None
	best_sets = None

	column_count = len(rows[0]) - 1  # the last column having the result is not included

	for col in range(column_count):
		column_values = {}
		for row in rows:
			column_values[row[col]] = 1

		for value in column_values.keys():
			set1, set2 = divideset(rows, col, value) # dividing based on column col and value val

			p = float(len(set1)) / len(rows)
			gain = current_score - p * scoreref(set1) - (1 - p) * scoreref(set2)

			if gain > best_gain:
				best_gain = gain
				best_criteria = (col, value)
				best_sets = (set1, set2)

		if best_gain > 0:
			truebranch = buildtree(best_sets[0])
			falsebranch = buildtree(best_sets[1])
			return decisionnode(col=best_criteria[0], value=best_criteria[1], fbranch=falsebranch, tbranch=truebranch)

		return decisionnode(results=getuniquecounts(rows))


def classify(observation, tree):
	'''
	classifies the observation using the tree
	'''
	if tree.results != None:  # this is a leaf node
		return tree.results
	v = observation[tree.col]
	if v == None:
		# handling missing data
		# taking both routes and giving each branch a weight equal to the fraction of all the rows
		# in it
		tr, fr = classify(observation, tree.tbranch), classify(observation, tree.fbranch)
		tcount = sum(tr.values())
		fcount = sum(tr.values())
		# the weghts for the truth and false routes
		tw = float(tcount) / (tcount + fcount)
		fw = float(fcount) / (tcount + fcount)
		result = {}
		for k, v in tr.items():
			result[k] = v * tw
		for k, v in tr.items():
			result[k] = v * fw
		return result
	branch = None
	if isinstance(v,int) or isinstance(v,float):
		# for numerical value
		if v >= tree.value:
			branch = tree.tbranch
		else:
			branch = tree.fbranch
	else:
		# for nominal value
		if v == tree.value:
			branch = tree.tbranch
		else:
			branch = tree.fbranch

	return classify(observation, branch)


def prune(tree, mingain):
	'''
	prunes the tree to reduce overfitting
	mingain - if the reduction in entropy is less than this, merge the branches of the tree
	'''
	# prune further the branches if they are not leaves
	if tree.tbranch.results == None:
		prune(tree.tbranch, mingain)
	if tree.fbranch.results == None:
		prune(tree.fbranch, mingain)

	# try to merge the leaves if the information gain is less than the threshold
	if tree.tbranch.results != None and tree.fbranch.results != None:
		# combining the datasets of the branches
		tbranch, fbranch = [], []
		for value, count in tree.tbranch.results.items():
			tbranch += [[value]] * count

		for value, count in tree.fbranch.results.items():
			fbranch += [[value]] * count

		tree_entropy = entropy(fbranch + tbranch)
		branches_entropy = entropy(tbranch) + entropy(tbranch)

		gain = tree_entropy - branches_entropy

		if gain < mingain:
			# merge the branches
			tree.tbranch, tree.fbranch = None, None  # deleting the child Nodes
			tree.results = getuniquecounts(tbranch + fbranch)
