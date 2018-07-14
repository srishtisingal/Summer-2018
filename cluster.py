"""
@author: Srishti

This is a modified implementation. Here dbscan clustering is applied on textual data.
Clustering is done till a single cluster is obtained at the end. 
Till then, I have kept on clustering considering the clusters as new data points in each iteration.

"""

from preprocess import *
import math
import numpy
from qdet import list2

data = getJSON("allWords_short.json")
tfidf = getJSON("wordDocument_tfidf.json")
ques_list = getJSON("ques_list_short.json")
tot = len(data)
C=0
level=0
mag = {}
def calculate_mag(tfidf):
	
	for uid in tfidf:
	    s = 0.0
	    for i in range(tot):
	        s += tfidf[uid][i]**2
	    mag[uid] = math.sqrt(s)

def MyDBSCAN(tfidf, D, eps, MinPts):
    global C
    cluster = {}
    labels={}
    for uid in D.keys():
        labels[uid]=0
   
    
    for P in D:
        if not (labels[P] == 0):
           continue
        
        # Find all of P's neighboring points.
        NeighborPts = regionQuery(tfidf, D, P, eps)
        #print(P, NeighborPts)
        # If the number is below MinPts, this point is noise. 
        # This is the only condition under which a point is labeled 
        # NOISE--when it's not a valid seed point. A NOISE point may later 
        # be picked up by another cluster as a boundary point (this is the only
        # condition under which a cluster label can change--from NOISE to 
        # something else).
        if len(NeighborPts) < MinPts:
            #print(P)
            labels[P] = -1
        # Otherwise, if there are at least MinPts nearby, use this point as the 
        # seed for a new cluster.    
        else: 
           #print("Initial seed point, ", P," ",C)
           C += 1
           cluster[C] = growCluster(tfidf, D, labels, P, NeighborPts, C, eps, MinPts, cluster)
    
    # All data has been clustered!
    return cluster


def growCluster(tfidf, D, labels, P, NeighborPts, C, eps, MinPts, cluster):
    """
    Grow a new cluster with label `C` from the seed point `P`.
    
    This function searches through the dataset to find all points that belong
    to this new cluster. When this function returns, cluster `C` is complete.
    
    Parameters:
      `D`      - The dataset (a list of vectors)
      `labels` - List storing the cluster labels for all dataset points
      `P`      - Index of the seed point for this new cluster
      `NeighborPts` - All of the neighbors of `P`
      `C`      - The label for this new cluster.  
      `eps`    - Threshold distance
      `MinPts` - Minimum required number of neighbors
    """

    # Assign the cluster label to the seed point.
    labels[P] = C
    
    # Look at each neighbor of P (neighbors are referred to as Pn). 
    # NeighborPts will be used as a FIFO queue of points to search--that is, it
    # will grow as we discover new branch points for the cluster. The FIFO
    # behavior is accomplished by using a while-loop rather than a for-loop.
    # In NeighborPts, the points are represented by their index in the original
    # dataset.
    i = 0
    while i < len(NeighborPts):    
        
        # Get the next point from the queue.        
        Pn = NeighborPts[i]
       
        # If Pn was labelled NOISE during the seed search, then we
        # know it's not a branch point (it doesn't have enough neighbors), so
        # make it a leaf point of cluster C and move on.
        if labels[Pn] == -1:
           #print("Inside grow cluster, a noise ele ",Pn," ",C)
           labels[Pn] = C
        
        # Otherwise, if Pn isn't already claimed, claim it as part of C.
        elif labels[Pn] == 0:
            # Add Pn to cluster C (Assign cluster label C).
            #print("Inside grow cluster, ", Pn," C",C, " i",i)    
            labels[Pn] = C
            
            # Find all the neighbors of Pn
            PnNeighborPts = regionQuery(tfidf, D, Pn, eps)
            # If Pn has at least MinPts neighbors, it's a branch point!
            # Add all of its neighbors to the FIFO queue to be searched. 
            if len(PnNeighborPts) >= MinPts:
                list1 = []
                for val in PnNeighborPts:
                    if val not in NeighborPts:
                        list1.append(val)
                NeighborPts = NeighborPts + list1
            # If Pn *doesn't* have enough neighbors, then it's a leaf point.
            # Don't queue up it's neighbors as expansion points.
            #else:
                # Do nothing                
                #NeighborPts = NeighborPts               
        
        # Advance to the next point in the FIFO queue.
        i += 1        
    cluster[C] = NeighborPts   
    return cluster[C] 
    # We've finished growing cluster C!


def regionQuery(tfidf, D, P, eps):
    """
    Find all points in dataset `D` within distance `eps` of point `P`.
    
    This function calculates the distance between a point P and every other 
    point in the dataset, and then returns only those points which are within a
    threshold distance `eps`.
    """
    neighbors = []
    
    # For each point in the dataset...
    if(level==1):
    	arr = ques_list[P]
    else:
    	arr = D
    for Pn in arr:
        # If the distance is below the threshold, add it to the neighbors list.
        sum = 0.0
        for i in range(tot):            
            sum += (tfidf[P][i]*tfidf[Pn][i])
        #print(level, sum)
        calculate_mag(tfidf)
        sim = sum /((math.sqrt(mag[Pn]))*(math.sqrt(mag[P])))
        #print(level, Pn, sim)
        if sim > eps:
           neighbors.append(Pn)
            
    return neighbors

ct = {}
ct[level] = MyDBSCAN(tfidf,tfidf,1,1)
level+=1
if(level==1):
	ct[level] = MyDBSCAN(tfidf, tfidf, 0.19, 2)
	n1 = len(ct[level].keys())
	#print(ct)
n2 = 1
while(len(ct[level].keys())>1 and n1!=n2):
	#print(level, ct)
	tf = {}
	for key in ct[level].keys():
		tf[key] = []
		for i in range(tot):
			s = 0
			for qid in ct[level][key]:
				if level==1:
					s += tfidf[qid][i]
				else:
					s += tf[qid][i]
			s = s/len(ct[level][key])
			tf[key].append(s)
	#print(tf)
	n1 = len(ct[level].keys())
	#print(level, ct)
	level += 1
	#print(level, ct)
	ct[level] = MyDBSCAN(tf, tf, -1, 1)
	#print(level, ct)
	n2 = len(ct[level].keys())
	#print(t[level])

print(ct)

json1 = json.dumps(tf)
f = open("tfidf_cluster.json","w")
f.write(json1)
f.close()

json = json.dumps(ct)
f = open("bottom_up_cluster.json","w")
f.write(json)
f.close()

