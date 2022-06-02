# Test Automation for Requirements

This folder contains a series of notebooks for use to evaluate the 'dummy_requirements.csv' file. 
The goal is to use natural language processing (NLP) models to cluster similar requirements. 

**NOTE**: Please run the notebooks in order, so that the datasets that are created from previous notebooks will allow the subsequent notebooks to work.

## 2.1-preprocessForTfidf

This notebook imports the saved 'dummy_requirements.csv'.
It uses 'utils.py' to preprocess the Description field in preparation for TF-IDF Vectorization.
It removes stop words, lemmatizes, removes digits and capitalization as preprocessing steps.
FIXME: the parts of speech pos_tags=True feature needs further debugging, set to `False` for sake of time. 
The 'Requirements' are then sorted and grouped by 'Component' and saved to 'DummyPreproccessedForTfidf.pickle'.

## 2.2-preprocessforDoc2Vec

This notebook imports the saved 'dummy_requirements.csv'.
It uses utils to preprocess the Description field in preparation for Doc2Vec Vectorization.
It DOES **NOT** remove stop words or lemmatize, but it DOES removes digits and capitalization as preprocessing steps.
FIXME: the parts of speech `pos_tags=True` feature needs further debugging, set to `False` for sake of time. 
The 'Requirements' are then sorted and grouped by 'Component' and saved to 'DummyPreproccessedForDoc2Vec.pickle'.

## 3-Dataset-Kmeans

This notebook performs the K-means clustering model (with differing results after TF-IDF preprocessing vs. Doc2Vec preprocessing) for the whole requirements dataset. The clustering does not depend on the system name. 

## 3.1-Components-Tfidf-Kmeans

This notebook loads the saved pickle 'DummyPreproccessedForTfidf.pickle'.
For loops are used to iterate through the list of components to create vectorization sets for each component.  These are saved to a dictionary `group_X` and dumped into the pickle called 'VectorizationTfidf.pickle'.
The vocabulary for each component is also saved for each component.
The notebook is set up to iterate through all components and run *K* means clustering on each Component.  
TODO: Currently, a hard coded k is set to 5 (with the exception of the component that has only one requirement).  This is where I would suggest updating based on your analysis finding optimal for for each component.  Easiest way would to be to create a dictionary, let's call it 'optimalK' with the Components as keys and values as a int of optimal *k*.  This can easily be added to the for loop setting num cluster to `optimalK[g]`...
Once clustering is completed, the Clusters are saved to the pickle 'ClustersTfidf.pickle'.

## 3.1.1-One-System-Tfidf-Kmeans

This notebook shows an example of using K-means for the ALPHA system component only, after TF-IDF preprocessing.

## 3.1.2-Multiple-Systems-Tfidf-Kmeans

This notebook shows an example of using K-means for both the ALPHA and GAMMA systems, after TF-IDF preprocessing.

## 3.2-Components-Doc2Vec-Kmeans

**Same as 3.1 but using Doc2Vec Vectorization method

This notebook loads the saved pickle 'DummyPreproccessedForDoc2Vec.pickle'.
For loops are used to iterate through the list of Components to create vectorization sets for each component.  These are saved to a dictionary `group_X` and dumped into the pickle called 'VectorizationDoc2Vec.pickle'.
The vocabulary for each component is also saved for each component.
The notebook is set up to iterate through all components and run *K* means clustering on each Component.  
TODO: Currently, a hard coded k is set to 5 (with the exception of the component that has only one requirement). This is where I would suggest updating based on your analysis finding optimal for for each component. Easiest way would to be to create a dictionary, let's call it 'optimalK' with the Components as keys and values as a int of optimal *k*.  This can easily be added to the for loop setting num cluster to `optimalK[g]`...
Once completed clustering, the Clusters are saved to the pickle 'ClustersDoc2Vec.pickle'.

## 3.2.1-One-System-Doc2Vec-Kmeans

This notebook shows an example of using K-means for the ALPHA system component only, after Doc2Vec preprocessing.

## 3.2.2-Multiple-Systems-Doc2Vec-KMeans

This notebook shows an example of using K-means for both the ALPHA and GAMMA systems, after Doc2Vec preprocessing.

## 4-DetermineOptimalKClusters

This notebook loads either the two pickles for:
TF-IDF ('DummyPreproccessedForTfidf.pickle' and 'DummyTfidf.pickle')
OR 
Doc2Vec ('RequirementsPreproccessedForDoc2Vec.pickle' and 'VectorizationDoc2Vec.pickle')
Select which component you wish to examine and set `g` to component.
Use the provided elbow method and `silhouette_coefficient` method to determine the optimal *k* for each dataset.  

You can adjusts the window range *K* in the for loop provided.  This takes a while as it runs *K* means clustering for each *k* in the list.
TODO: Manually create `optimalK` dictionary.  
```
optimalK = {'AFATDS' : 93,          
             ...}
```
I suggest saving and loading to workbooks 3.

## 5-InspectClusters

This notebook uploads either pickles: 'ClustersTfidf.pickle' or 'ClustersDoc2Vec.pickle'.
There are helper functions included in utils to inspect what is within each cluster.
YAKE is used to determine Keywords within the cluster to help describe each cluster.
