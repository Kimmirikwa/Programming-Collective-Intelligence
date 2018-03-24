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

		words = getWords(e.title + summary)
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