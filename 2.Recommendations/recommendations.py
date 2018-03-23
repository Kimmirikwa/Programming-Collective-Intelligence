from math import sqrt

# A dictionary of movie critics and their ratings of a small
# set of movies
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
	movies ratings
	'''
	similar_movies = [movie for movie in critics[person1] if movie in critics[person2]]

	if len(similar_movies) == 0:
		return 0

	# the sums will be big if the user ratings are very different
	sum_squared_diffs = sum([pow(critics[person1][movie] - critics[person2][movie], 2) for movie in similar_movies])

	# the returned value will be between 0 and 1
	# the value will be higher for very similar critics
	return 1.0 / (1 + sqrt(sum_squared_diffs))
