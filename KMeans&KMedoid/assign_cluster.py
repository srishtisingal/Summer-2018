"""
@author: Srishti 
"""

#k means clustering

from preprocess import *

C = getJSON("initial_cluster.json")
X = getJSON("tfidf_ques.json")

cluster={}

#this function is used to calculate and save the magnitude of each vector in mag_cl dictionary
def compute(C):
	mag_cl={}
	for c in C:
		cluster[c]=[]
		mag_cl[c]=0.0
		centroid=C[c]
		for word in centroid:
			mag_cl[c] += centroid[word]*centroid[word]
	return mag_cl

#Find distance between qid and each centroid. 
#Finally assign the qid to the cluster with which the score or similarity is max. 
def find_dist(qid, tmp, mag_c):
	final={}
	score={}
	for c in C:
		clust = C[c]
		mag_t=0.0
		sc=0.0
		#finding the cosine similarity between qid and each centroid
		for word in tmp:
			if word in clust:
				sc +=tmp[word]*clust[word]
			mag_t += tmp[word]*tmp[word]
		score[c]=sc
		final[c] = score[c]/(mag_t**0.5 * mag_c[c]**0.5)
	#find the id with which the similarity is maximum and store it in c_id
	c_id=max(final.keys(), key=(lambda j:final[j]))
	#append the qid to the cluster with c_id as the centroid
	cluster[c_id].append(qid)

cnt=1
cnt2=1

while(1):
	print('----------------------------------------')
	mag_c=compute(C)
	#initialising the cluster with the centroids
	if(cnt2==1):
		for c in C:
			cluster[c].append(c)
		cnt2=0

	for qid in X:
		find_dist(qid,X[qid],mag_c)
	print(cluster)
	i=1
	if(cnt==1):
		tfidf_clust={}
		new_c={}
		new_Cent={}
		for cid in cluster:
			new_Cent[i]=C[cid]
			new_c[i]=cluster[cid]
			tfidf_clust[i]=X[cid]
			i=i+1
		cnt=0
		cluster=new_c
		C=new_Cent

	count=0
	#for the next iteration, for each cluster, we have to change the centroid 
	#i.e. assign new tfidf values to the centroid which will be the mean of its cluster elements.
	for cid in cluster:
		list1 = cluster[cid]
		len1=len(list1)
		tfidf_clust[cid]={}
		for ele in list1:
			for word in X[ele]:
				if word not in tfidf_clust[cid]:
					val_word=0
					for ele2 in list1:
						if word in X[ele2]:
							val_word += X[ele2][word]
					tfidf_clust[cid][word]=val_word/len1
		prev_val=C[cid]
		new_val=tfidf_clust[cid]
		#checking if no new change is made in the existing cluster.
		for key in new_val.keys():
			if(key in prev_val.keys()) :
				if abs(new_val[key] - prev_val[key]) > 0.0005:
					#print("Whoosh")
					count=1
			else:
				#print("Duh")
				count=1
	#condition to break out of the lopp and finalise the clusters
	if count==0 :
		print("Toodles")
		break
	C=tfidf_clust	

with open("Final_clusters.json","w") as f:
	json1=json.dumps(cluster)
	f.write(json1)

with open("Final_centroids.json","w") as fp:
	json=json.dumps(tfidf_clust)
	fp.write(json)		