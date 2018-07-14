"""
@author: Srishti 
"""

#this file makes a dictionary idf_A which has each word in allWords as its key and the value is a list containing 
#all such questions which have the considered word in their description.
from qdet import list2
from preprocess import *
import json
import nltk

data=getJSON("android_questions.json")
proc_ans=getJSON("preprocessed_answers.json")           #this has all the preprocessed data stored beforehand
all_ans=getJSON("allWords.json")
                       
idf_A={}                                                #a dictionary to store each word alongwith the questions which have the word

for word in all_ans:
	#initialising the list as empty
	idf_A[word]=[]                                      
	print(word)
	for ansid in list2:
		if word in proc_ans[ansid]:
			idf_A[word].append(ansid)                  #appending the questions which possess the word in consideration

with open('wordDocumentCount.json','w') as fp:         #storing this data in wordDocumentCount.json
	json = json.dumps(idf_A)
	fp.write(json)
