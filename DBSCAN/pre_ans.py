"""
@author: Srishti
"""

#storing the preprocessed questions in a file.

from qdet import list2
from preprocess import *
import json
import nltk

data=getJSON("android_questions_short.json")
print(len(list2))
ans_id={}

for aid in list2:
	ans=data[aid].get("body")
	if ans is not None:
		ans_id[aid]=preprocess(cleanhtml(ans))
		
with open('pre_android_questions.json','w') as fp:
	json = json.dumps(ans_id)
	fp.write(json)
