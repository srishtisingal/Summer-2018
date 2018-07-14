/***********************************
Author: Srishti 

***********************************/

Initial step is to preprocess the data. The files responsible for that are:
1. preprocess.py
2. qdet.py
3. pre_ans.py
4. allwords.py
5. word_freq_count.py
6. word_doc_count.py
7. make_tfidf.py

Then initialise the clusters for k means & k medoids using init_cluster.py 
For the cluster initialisation, k means++ has been used.

After the initialisation, you are ready to assign clusters in case of k means OR medoids in case of k medoids.
Execute assign_cluster.py OR assign_medoid.py 