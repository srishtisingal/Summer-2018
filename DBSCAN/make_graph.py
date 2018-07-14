"""
@author: Srishti
"""

#make a graph connecting all those qids which have at least 1 word in common
from preprocess import *
from qdet import list2

data = getJSON("pre_android_questions.json")

ques_list={}
for qid in data:
	ques_list[qid]=[]
	for qid2 in data:
		if qid!=qid2:
			for word in data[qid]:
				if word in data[qid2]:
					ques_list[qid].append(qid2)
					break
			#if(list(set(data[qid]).intersection(data[qid2]))):
			#	ques_list[qid].append(qid2)

json = json.dumps(ques_list)
f=open("ques_list_short.json","w")
f.write(json)
f.close()