"""
@author: Srishti 
"""

#Calculating the frequency of each word in each question
from qdet import list2
from preprocess import *
import json
import nltk

data=getJSON("android_questions.json")

ans_id={}                         #to store the preprocessed data
ans_freq={}                       #to store the freq of each word

for aid in list2:
	ans=data[aid].get("body")
	if ans is not None:
		ans_id[aid]=preprocess(ans)
		ans_freq[aid]=nltk.FreqDist(ans_id[aid])             #calculating frequency

with open('wordFrequencyCount.json','w') as fp:              #storing the frequency values in wordFrequencyCount.json
	json = json.dumps(ans_freq)
	fp.write(json)