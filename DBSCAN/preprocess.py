"""
@author: Srishti
"""

#It is used to preprocess the data
#It removes the html tags as well as the stop words from the data
import json
from nltk.tokenize import RegexpTokenizer
import re
import nltk

def getJSON(filePathAndName):
	with open(filePathAndName,'r') as fp:
		return json.load(fp)

#removing stopwords
def preprocess(sentence):
	stopwords = set(nltk.corpus.stopwords.words('english'))
	sentence = sentence.lower()
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(sentence)
	words = [word for word in tokens if len(word) > 1]
	words = [word for word in tokens if not word.isnumeric()]
	filtered_words = [w for w in words if not w in stopwords]
	return (filtered_words)

#removing html
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
