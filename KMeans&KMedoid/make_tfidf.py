"""
@author: Srishti 
"""

#get the tfidf of each question/answer id beforehand and store it in a file in a dictionary 
from qdet import list2
from qdet import list3
import json
from nltk.tokenize import RegexpTokenizer
import re
import math
from collections import OrderedDict
from preprocess import*

#loading all the json files in variables to ease the usage
idf_A=getJSON('wordDocumentCount.json')
allWords_A=getJSON('allWords.json')
wordList_A=getJSON('wordFrequencyCount.json')
data_A=getJSON("android_questions.json")
proc_ans=getJSON("preprocessed_questions.json")

tfidf_A={}                                                 #it will save the tfidf values of each question
totalAnswers=len(list3)                                    #get total no. of answers

#computing the value of tfidf
def calculateTFIDFB(aid,word):
	#check if word is present in aid
	if word in wordList_A[aid]:
		#cal tf. take freq from wordList_A
		val_tf = 1 + math.log(wordList_A[aid][word])
		#cal idf. take no. of documents containing the word from idf_A dictionary	
		val_idf = (math.log(totalAnswers/(len(idf_A[word])+1)))
		#return (1+math.log(wordList_A[aid][word])*math.log(totalAnswers/(len(idf_A[word])+1)))
		return (val_tf*val_idf)
	else:
		return 0

#to calculate the tfidf value
def calculate_TfIdf(question,aid):
	tfidf_A[aid]={}                              #initialising each value as an empty dictionary
	for word in question:                        #loop for each word in that particular question 
		if word in allWords_A:                   #check if word is a part of the allWords_A file
			for uid in idf_A[word]:              #loop for each document that the word is present in
				x2=calculateTFIDFB(uid,word)     #now call calculateTFIDFB function to get the value of tfidf
		tfidf_A[aid][word]=x2                    #tfidf_A[aid][word] i.e. value for that word in aid


#for each answer id, calculate the tfidf value
for aid in list3:
	calculate_TfIdf(proc_ans[aid],aid)

with open('tfidf_ques.json','w') as fp:
	json = json.dumps(tfidf_A)
	fp.write(json)
		
