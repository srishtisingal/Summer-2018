"""
@author: Srishti
"""

#Finding all the words present in the questions after preprocessing. 
from qdet import list2                      #list2 has the question ids
from preprocess import *                    #this file is for preprocessing the data
import json
import nltk

data=getJSON("android_questions_short.json")

all_ans=[]

for aid in list2:
	ans=data[aid].get("body")                   #get the textual data of question id aid
	if ans is not None:                          
		ans1=preprocess(cleanhtml(ans))        
		for w in ans1:                   
			all_ans.append(w)           

all_ans = set(all_ans)      
all_ans=list(all_ans)
print(all_ans)                                   
with open('allWords_short.json','w') as fp:            #saving all the words in allWords.json file
	json = json.dumps(all_ans)                      
	fp.write(json)
