import feedparser
import re

def getwordcounts(url):
	'''
	gets the title and word counts in a blog
	'''
	wc = {}

	d = feedparser.parse(url)

	for e in d.entries:
		if 'summary' in e:
			summary = e.summary
		else:
			summary = e.description

		words = getwords(e.title + summary)
		for word in words:
			wc.setdefault(word, 0)
			wc[word] += 1
	return d.feed.title, wc

def getwords(html):
	'''
	removes html tags and splits the words using non-alpha characters
	'''

	txt = re.compile(r'<[^>]+>').sub('', html)

	words = re.compile(r'[^A-Z^a-z]+').split(txt)

	return [word.lower() for word in words if word != ' ']


apcount = {}
wordcount = {}

path = '/home/mirikwa/projects/ml/Programming-Collective-Intelligence/3.Clustering/data'

for feedurl in file(path + '/feedlist.txt'):
	title, wc = getwordcounts(feedurl)
	wordcount[title] = wc
	for word, count in wc.items():
		apcount.setdefault(word, 0)
		if count <= 1:
			continue
		apcount[word] += 1


# gettingn the wors that will actually be used in clustering
# dropping words that are too common or very strange and thus appear in very few blogs
wordlist = []
feedlist = open(path + '/feedlist.txt').readlines()
for word, count in apcount.items():
	frac = float(count) / len(feedlist)
	if frac > 0.1 and frac < 0.5:
		wordlist.append(word)

out = file(path + '/blogdata.txt', 'w')
out.write('Blog')
for word in wordlist:
	out.write('\t{}'.format(word))
for word, count in wordcount.items():
	if word in wordlist:
		out.write('\t{}'.format(count))
	else:
		out.write('\t0')
	out.write('\n')