# predicting using decision trees. Decision trees are more transparent and therefore easy to understand
# as they appear to be like if and else statements once modeled

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
	def __init__(self, col=-1, value, tbranch, fbranch, result):
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
		self.result = result