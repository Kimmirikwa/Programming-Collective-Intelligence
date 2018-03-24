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
	sum2 = sum([critics[person2][item] for item] in similar_items)

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


def topMatches(critics, person, n=5, similarity=sim_pearson):
	'''
	return n critics who are most similar to person in a sorted order
	'''
	matches = [(similarity(critics, person, other), other) for other in critics if other != person]

	# sorts and reverses the matches in place and returns n most similar critics
	matches.sort()
	matches.reverse()
	return matches[0:n]


def getRecommendations(critics, person, similarity=sim_pearson):
	'''
	gets the recommendations for a person
	'''
	sim_sums = {} # will hold the sums of the similarities
	product_sums = {}  # will hold the sums of the products of the similarites and item ratings

	for critic in critics:
		if critic == person:  # a person can't recomment him/herself
			continue

		sim = similarity(critics, person, critic)

		for watched_item in person:
			for item in critic:
				if item == watched_item:  # should not recomment a item watched
					continue

				sim_sums.setdefault(item, 0)
				sim_sums[item] += sim

				product_sums.setdefault(item, 0)
				product_sums[item] += sim * critics[critic][item]

	recoms = [(sum_item / sim_sums(item), item) for item, sum_item in product_sums.items()]

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


def calculateSimilarities(prefs, n=10):
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