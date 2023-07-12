# coding: utf-8

""" Who Cites Me?
Search SAO/NASA ADS to generate a list of people who cite you the most often
Philip Mocz, 2023 (@PMocz)
"""

__author__ = "Philip Mocz <philip.mocz@gmail.com>"


import ads
from collections import Counter
from tqdm import tqdm
import time


# **********************************************************************
# Change these:
my_name = "Mocz, P"
ads.config.token = 'secret token' # add your ADS secret token here, keep it secret! (obtain from: https://ui.adsabs.harvard.edu/user/settings/token)
exclude_self_citations = True
# **********************************************************************



bibcode_counter = Counter()
author_counter = Counter()


# a function that turns "Lastname, Firstname I." -> "Lastname, F"
prettify_author_name = lambda author: author.split(",")[0] + ", " + author.split(",")[1].strip()[0]


# Search for my papers
my_papers = list(ads.SearchQuery(author=my_name, fl=['id', 'bibcode', 'citation']))
print('Found ', len(my_papers), ' papers for the name: ', my_name)

# Get all the bibcodes that cite my papers (with counts)
for paper in my_papers:
	if(paper.citation):
		for bibcode in paper.citation:
			if(bibcode):
				bibcode_counter[bibcode] += 1

if(exclude_self_citations):
	for paper in my_papers:
		if bibcode_counter[paper.bibcode] > 0:
			del bibcode_counter[paper.bibcode]

print('Found ', len(bibcode_counter), ' papers that cite these.')	
		
# Search for all authors in this bibcode list
print('Creating complete author list of all works that cite me (may take a few minutes) ...')	
articles = []
for idx, bibcode in tqdm(enumerate(bibcode_counter)):
	articles.append(list(ads.SearchQuery(bibcode=bibcode, fl=['id', 'bibcode', 'author']))[0])
	time.sleep(0.1) # to limit query rate
	
print('... author list complete!')

# Tally up the number of times each author cites me
for article in articles:
	for author in article.author:
		author_counter[prettify_author_name(author)] += bibcode_counter[article.bibcode]


# Print list of 30 most common authors that cite me
print('Listing most common authors that cite me:')
most_common = author_counter.most_common(30)	
for idx, pair in enumerate(most_common):
	print('#', idx+1, ': ', pair[0], ' (', pair[1], ')')

