"""
@author: Srishti 
"""

#initialise the k clusters by k means++ algorithm
import operator
from preprocess import *

#loading the json files of questions and their tfidf vectors
data_Q = getJSON("android_questions.json")
data_tfidf_Q = getJSON("tfidf_ques.json")

#calculate the distance between tdidf vectors
def distance(q1,c):
	score=0.0
	mag_q=0.0
	mag_c=0.0
	cl=X[c]
	for word in q1:
		mag_q += q1[word]*q1[word] 
		if word in cl:
			score = q1[word]*cl[word]
	for word in cl:
		mag_c += cl[word]*cl[word]
	final = score/(mag_q**0.5 * mag_c**0.5)		
	return final

#function to calculate the similarity between qid and each centroid and return the minimum value of distance
def similarity(tmp):
	q1=tmp
	dis=[]
	for c in C:
		dis.append(distance(q1,c)) 
	min_d = min(dis)
	return min_d*min_d 	

def initialize(X,K):
	#run the loop K times so as to get a new centroid in each iteration which is at the maximum distance from the k centroids
    for k in range(1, K):
        #D2 will store the dissimilarity of each qid from already chosen centroids
        D2={}
        for qid in X:
        	D2[qid]=1-similarity(X[qid])                                #dissimilarity = 1 - similarity
        
        s = sorted(D2.items(),key=(lambda i: i[1]))                     #sort D2 and store in s
        #clust_id=max(D2.keys(), key=(lambda j:D2[j]))
        leng=len(s)
        clust_id=s[-1][0]                                               
        if clust_id in C.keys():
        	for ind in range(2,leng):
        		clust_id=s[-ind][0]
        		if clust_id not in C.keys():
        			break
        C[clust_id]=X[clust_id]											#assign clust_id to C along with it's tfidf vector
    return C

#k is the no. of initial centroids you want
K=4
X = data_tfidf_Q
cnt=0
#C is a dictionary which will store the initial centroids
#the key will be the question id and the value will be it's tfidf vector 
C={}

#putting the first question id as the initial centroid
for qid in X:
	if(cnt==0):
		C[qid]=X[qid]
		cnt=cnt+1
	else:
		break

#this will initialise the centroids and store them in list1
list1=initialize(X,K)

with open("initial_cluster.json","w") as fp:
	json=json.dumps(list1)
	fp.write(json)
