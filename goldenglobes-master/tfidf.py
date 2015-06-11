import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
import math
 
 
stopwords = nltk.corpus.stopwords.words('english')
tokenizer = RegexpTokenizer("[\w']+", flags=re.UNICODE)
 
 
def freq(word, doc):
	return doc.count(word)
 
 
def word_count(doc):
	return len(doc)
 
 
def tf(word, doc):
	return (freq(word, doc) / float(word_count(doc)))
 
 
def num_docs_containing(word, list_of_docs):
	count = 0
	for document in list_of_docs:
		if freq(word, document) > 0:
			count += 1
	return 1 + count
 
 
def idf(word, list_of_docs):
	return math.log(len(list_of_docs) /float(num_docs_containing(word, list_of_docs)))
 
 
def tf_idf(word, doc, list_of_docs):
	return (tf(word, doc) * idf(word, list_of_docs))
