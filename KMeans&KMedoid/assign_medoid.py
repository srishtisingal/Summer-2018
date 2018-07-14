"""
@author: Srishti 
"""

#K Medoid clustering

import json
from preprocess import *
from qdet import list2

C = getJSON("initial_cluster.json")
X = getJSON("tfidf_ques.json")

final_cl={}
final_cl[1]=C

cluster={}
cluster[1]={}

#computing the magnitude of each vector beforehand
def compute(C, ind):
	mag_cl={}
	cluster[ind]={}
	for c in C:
		cluster[ind][c]=[]
		mag_cl[c]=0.0
		centroid=C[c]
		for word in centroid:
			mag_cl[c] += centroid[word]*centroid[word]
	return mag_cl

#finding the distance between qid and each medoid
def find_dist(ind,qid, tmp, mag_c):
	final={}
	score={}
	for c in C:
		clust = C[c]
		mag_t=0.0
		sc=0.0
		for word in tmp:
			if word in clust:
				sc +=tmp[word]*clust[word]
			mag_t += tmp[word]*tmp[word]
		score[c]=sc
		final[c] = score[c]/(mag_t**0.5 * mag_c[c]**0.5)
	c_id=max(final.keys(), key=(lambda j:final[j]))
	cluster[ind][c_id].append(qid)
	return final[c_id]

i=1
j=1
list9 = []
for key in C.keys():
	list9.append(key)

sc = {}

val1 = list9[0]
val2 = list9[1]
val3 = list9[2]
val4 = list9[3]

tf=0.0
mag = compute(C,i)
for qid in X:
	tf += find_dist(i,qid,X[qid], mag)
sc[1]=tf
final_cl[1]=C

# applying k medoid algorithm
# i is the index storing the no. of iteration so that they can be compared once each combination has been tried
for key1 in cluster[i][list9[0]]:
	#print("Loop1")
	if key1 not in C.keys():
		#print("In loop1 ")
		C[key1]=X[key1]
		del C[list9[0]]
		list9[0]=key1
	for key2 in cluster[i][list9[1]]:
		#print("loop2")
		if key2 not in C.keys():
			#print("In LOop2")
			C[key2]=X[key2]
			del C[list9[1]]
			list9[1]=key2
		for key3 in cluster[i][list9[2]]:
			#print("loop3")
			if key3 not in C.keys():
				#print("in loop3")
				C[key3]=X[key3]
				del C[list9[2]]
				list9[2]=key3
			for key4 in cluster[i][list9[3]]:
				#print("Hello")
				#print(C[list9[3]])
				if key4 not in C.keys():
					#print("in loop4")
					C[key4]=X[key4]
					del C[list9[3]]
					list9[3]=key4
					mag_c = compute(C,i+1)
					tf=0.0
					for qid in X:
						tf += find_dist(i+1, qid, X[qid], mag_c)
					sc[i+1] = tf
					final_cl[i+1] = C
					i=i+1

dfq = max(sc.keys(), key=(lambda j:sc[j]))
final_clusters = cluster[dfq]

final_cent={}

for cid in final_clusters:
	final_cent[cid]=X[cid]

print(final_cent)
print(final_clusters)

with open("Medoid.json","w") as fp:
	json1=json.dumps(final_cent)
	fp.write(json1)

with open("Clusters_med.json","w") as f:
	json = json.dumps(final_clusters)
	f.write(json)