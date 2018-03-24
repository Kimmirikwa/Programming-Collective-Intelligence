from math import sqrt

# A dictionary of item critics and their ratings of a small
# set of items
critics = {
	'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
	'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
	'The Night Listener': 3.0},
	'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
	'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
	'You, Me and Dupree': 3.5},
	'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
	'Superman Returns': 3.5, 'The Night Listener': 4.0},
	'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
	'The Night Listener': 4.5, 'Superman Returns': 4.0,
	'You, Me and Dupree': 2.5},
	'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
	'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
	'You, Me and Dupree': 2.0},
	'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
	'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
	'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}
}

def sim_distance(critics, person1, person2):
	'''
	Finds the Euclidean distance between person1 and person2
	items ratings
	'''
	similar_items = [item for item in critics[person1] if item in critics[person2]]

	if len(similar_items) == 0:
		return 0

	# the sums will be big if the user ratings are very different
	sum_squared_diffs = sum([pow(critics[person1][item] - critics[person2][item], 2) for item in similar_items])

	# the returned value will be between 0 and 1
	# the value will be higher for very similar critics
	return 1.0 / (1 + sqrt(sum_squared_diffs))


def sim_pearson(critics, person1, person2):
	'''
	Finds the pearson correlation between person1 and person 2 item ratings
	corrects for grade inflation while euclidean distance will only conclude 
	that items are similar if their values are exactly the same
	returned value will be between -1 and 1, with positive values indicating
	positive similarity and vice versa
	'''
	similar_items = [item for item in critics[person1] if item in critics[person2]]

	n = len(similar_items)
	if n == 0:
		return 0

	# the sums of the item ratings
	sum1 = sum([critics[person1][item] for item in similar_items])
	sum2 = sum([critics[person2][item] for item in similar_items])

	# the sums of the squares of the ratings
	sum1Sq = sum([pow(critics[person1][item], 2) for item in similar_items])
	sum2Sq = sum([pow(critics[person2][item], 2) for item in similar_items])

	# the sums of the products
	sumProd = sum([critics[person1][item] * critics[person2][item] for item in similar_items])

	numerator = sumProd - sum1 * sum2 / n
	denomenator = sqrt((sum1Sq - sum1 * sum1 / n) * (sum2Sq - sum2 * sum2 / n))

	if denomenator == 0:
		return 0

	return numerator / denomenator  # value will be between -1 and 1, being high with high simlilarity


def sim_tanimoto(prefs, person1, person2):
	'''
	suited for finding similarity between binary data
	finds the intersection / union of the data sets
	'''
	intersection = [item for item in prefs[person1] if prefs[person2].get(item) == prefs[person1][item]]
	return len(intersection) / (len(prefs[person1]) + len(prefs[person2]) - intersection)


def topMatches(critics, person, n=5, similarity=sim_pearson):
	'''
	return n critics who are most similar to person in a sorted order
	'''
	matches = [(similarity(critics, person, other), other) for other in critics if other != person]

	# sorts and reverses the matches in place and returns n most similar critics
	matches.sort()
	matches.reverse()
	return matches[0:n]


def getRecommendations(prefs, person, similarity=sim_pearson):
	'''
	gets the recommendations for a person
	'''
	sim_sums = {} # will hold the sums of the similarities
	product_sums = {}  # will hold the sums of the products of the similarites and item ratings

	for other in prefs:
		if other == person:  # a person can't recomment him/herself
			continue

		sim = similarity(prefs, person, other)

		if sim <= 0:
			continue

		for item in prefs[other]:
			if prefs[person].get(item):
				continue
			sim_sums.setdefault(item, 0)
			sim_sums[item] += sim

			product_sums.setdefault(item,0)
			product_sums[item] += prefs[other][item] * sim

	recoms = [(sum_item / sim_sums[item], item) for item, sum_item in product_sums.items()]

	recoms.sort()
	recoms.reverse()
	return recoms


def transformPrefs(prefs):
	results = {}
	for critic in prefs:
		for item in prefs[critic]:
			results.setdefault(item, {})
			results[item][critic] = prefs[critic][item]

	return results


def calculateSimilarItems(prefs, n=10):
	'''
	gets the similarities between items
	this does not need to run very often as item similarities may not change a lot after a new rating comes in
	for instance, the calculation can be done during low traffic hours or in another computer that if off network
	'''
	itemPrefs = transformPrefs(prefs)
	results = {}

	c = 0

	for item in itemPrefs:
		c += 1
		if c % 100 == 0:
			print "%d / %d" % (c,len(itemPrefs))
		scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
		results[item] = scores

	return results # each item will have its 10 most similar items


def calculateSimilarUsers(prefs, n=5):
	'''
	precomputes similar users
	'''
	results = {}

	c = 0

	for user in prefs:
		c += 1
		if c % 100 == 0:
			print "%d / %d" % (c,len(itemPrefs))
		results[user] = topMatches(prefs, user, n=n, similarity=sim_distance)

	return results  # returns users with their n most similar users

def getRecommendedItems(prefs, itemsMatch, user):
	'''
	gets recommendations for a user using item based filtering
	it uses the similarities between items the user has rated and the items the user
	has not yet rated.
	item based filtering is more efficient than user based filetering for a sparce
	data but their perfomance on dense data data is almost the same.
	'''
	userRatings = prefs[user]

	scores = {}
	totalSim = {}

	for (item, rating) in userRatings.items():
		for (similarity, item2) in itemsMatch[item]:
			if item2 in userRatings:  # should not recommend an item already rated by the user
				continue

			totalSim.setdefault(item2, 0)
			totalSim[item2] += similarity

			scores.setdefault(item2, 0)
			scores[item2] += similarity * rating

	recoms = [(score/totalSim[item], item) for item, score in scores.items()]

	recoms.sort()
	recoms.reverse()
	return recoms


def loadMovieLens(path="/home/mirikwa/projects/ml/Programming-Collective-Intelligence/2.Recommendations/data"):
	'''
	loads the movies data and composes the preferences
	''' 

	# get the movie titles from u.item
	# an example line is as below
	# 1|Toy Story (1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)|0|0|0|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0|0
	# values are separated by |, from the line above 1 is the id and Toy Story (1995) is the title
	movies = {}
	for line in open(path+'/u.item'):
		movie_id, title = line.split('|')[0:2]
		movies[movie_id] = title

	# composing the preferences
	# an example line from u.data
	# 196	242	3	881250949
	# in the above line 196 is the user id, 242 the movie id, 3 is the rating and 881250949 is the timestamp
	# prefs will be a nested dict of users and their ratings for different movies
	prefs = {}
	for line in open(path+'/u.data'):
		user, movie_id, rating, ts = line.split('\t')
		prefs.setdefault(user, {})
		prefs[user][movies[movie_id]] = float(rating)
	return prefs