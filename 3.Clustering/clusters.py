from math import sqrt


def readfile(filename):
	'''
	reads the file of the data
	the first row contains the words used in the clustering
	the rest of the rows contain the counts of the words
	the first column contains the titles of the blogs
	the rest of the columns contain the counts of the words
	'''
	lines = [line for line in file(filename)]

	colnames = lines[0].strip().split('\t')[1:]

	rownames = []
	wordcounts = []

	for line in lines[1:]:
		p = line.strip().split('\t')
		rownames.append(p[0])
		wordcounts.append([float(x) for x in p[1:]])

	return rownames, colnames, wordcounts


def pearson(v1, v2):
	'''
	finds the similarity using pearson coeficient
	this will correct the cases where some blogs have more words occurence than
	others as it tests how compared data fit on a straught line
	'''
	n = len(v1)

	sum1 = sum(v1)
	sum2 = sum(v2)

	sum1Sq = sum([pow(value, 2) for value in v1])
	sum2Sq = sum([pow(value, 2) for value in v2])

	sumProd = sum([v1[index] * v2[index] for index in range(n)])


	# calculating the score
	# num/denom is a value between -1 and 1
	# +ve value indicates positive correlation and vice versa
	num = sumProd - sum1 * sum2 / n
	denom = sqrt(abs((sum1Sq - pow(sum1, 2)/n) * (sum2Sq - pow(sum2, 2)/n)))

	if denom == 0:
		return 0

	return 1.0 - num / denom  # for similar items the return value will be small


# modeling the cluster
# a node is either a point in the dataset(a blog in this case)
# or a point in the tree with 2 branches
class bicluster():
	def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
		self.vec = vec
		self.left = left
		self.right = right
		self.distance = distance
		self.id = id


def hcluster(rows, distance=pearson):
	'''
	Hierachical clustering function
	'''
	distances = {}
	currentclustid = -1  # clusters with branches will have -ve ids

	# initially the clusters are just the rows
	clusters = [bicluster(rows[i], id=i) for i in range(len(rows))]

	while len(clusters) > 1:
		closest = (0, 1)
		lowest_distance = distance(clusters[0].vec, clusters[1].vec)

		for i in range(len(clusters)):
			for j in range(i+1, len(clusters)):
				if (clusters[i].id, clusters[j].id) not in distances:
					distances[(clusters[i].id, clusters[j].id)] = distance(clusters[i].vec, clusters[j].vec)

				d = distances[(clusters[i].id, clusters[j].id)]
				if d < lowest_distance:
					lowest_distance = d
					closest = (i, j)

		# merging the closest vectors
		# the merged vector will be the mean of the closest vectors
		mergevec = [(clusters[closest[0]].vec[i] + clusters[closest[1]].vec[i]) / 2.0 for x in range(len(clusters[0].vec))]

		new_cluster = bicluster(mergevec, left=clusters[closest[0]], right=clusters[closest[1]], id=currentclustid, distance=lowest_distance)

		currentclustid -= 1
		del clusters[closest[1]]
		del clusters[closest[0]]
		clusters.append(new_cluster)

	return clusters[0]