# import packages'
import string
import ast
from matplotlib import use
import pandas as pd
from sklearn import preprocessing
import utils 
import pickle
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import gensim
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

def main2():
    # userInput = 'cs1 maint attained national stature as the including exportation characters excluding whitespace and a vast tropical forest home to the practice of further clarification to testify even when they finished were described are having difficulty taking off france also staged a begins with funded as of 2010 it'
    inputfile = "dummy_requirements.csv"
    df = pd.read_csv(inputfile)
            
    print("preprocessing data with Doc2Vec...")
    df = df.astype(str)
    my_stop_words = [] # minimal preprocessing. do not remove stopwords or lemmatize for doc2vec
    df['Requirement'] = df.apply(lambda x: utils.preprocess_text(x['Description'], my_stop_words,keep_original=True, display=False, pos_tags=True), axis=1)
    #includes POS
    df['POS'] = df.apply(lambda x: x['Requirement'][1], axis=1)
    df['Requirement'] = df.apply(lambda x: x['Requirement'][0], axis=1)
    
    #retur npickle file with preprocess data
    with open("cleaned_dummy_doc2vec.pickle", "wb") as pickle_file:
        pickle.dump(df, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
        
    print("grouping components...")
    components = df.groupby(by='Component/s')
    components.size()
    groups = components.groups.keys()
    grouped_data = {}
    for g in groups:
        # print(g)
        sub_df = components.get_group(g)
        sub_df = sub_df.astype(str)
        X = sub_df
        grouped_data[g] = X
        # print(X)
    #Adds grouped preprocess data into data into pickle file 
    with open("DummyPreproccessedForDoc2Vec.pickle", "wb") as pickle_file:
        pickle.dump(grouped_data, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

    print("vectorization of each component...")
#will create vectorization object for each componet and kmeans cluster for each component
# def createclusterforspecificcomponent():
    num_clusters = 5
    #opens grouped data file 
    with open("DummyPreproccessedForDoc2Vec.pickle", "rb") as pickle_file:
        grouped_data = pickle.load(pickle_file)
    #obtains components
    groups = grouped_data.keys()
    
    # Doc to Vec

    def tagged_document(list_of_lists):
        for i, list_of_words in enumerate(list_of_lists):
            yield gensim.models.doc2vec.TaggedDocument(list_of_words, [i])

    print("adding components to dictionary")
   # def compoonenttodictionary():
    group_X = {}
    for g in groups:
        corpus = list(tagged_document(grouped_data[g]['Requirement']))
        d2v = gensim.models.doc2vec.Doc2Vec(vector_size=200, dm=0, min_count=2, epochs=50, seed=5)
        d2v.random.seed(5)
        d2v.build_vocab(corpus)
        d2v.random.seed(5)
        d2v.train(corpus, total_examples=d2v.corpus_count, epochs=d2v.epochs)
        # fit language model
        X = []
        for row in grouped_data[g]['Requirement']:
            d2v.random.seed(5)
            X.append(d2v.infer_vector(row.split(' ')))
    
        X = np.array(X)
        group_X[g] = X
        # print('Word embeddings shape: ', end=' ')
        # print(X.shape)
        # print("Testing...")
    #grouped data placed in pickle file   
    with open("VectorizationDoc2Vec.pickle", "wb") as pickle_file:
        pickle.dump(group_X, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
        
#def createkmeansskusterforspecificcomponent():
    #do not use for loop but searchh for cpecific component first
    # FIXME: Each subgroup will have a different optimal K clusters... 
    # num_clusters = 6 # defined on top cell

    for g in groups:
        if (len(grouped_data[g]) < num_clusters):
            num_clusters = 1
        model = KMeans(n_clusters=num_clusters, init='k-means++', random_state=5).fit(group_X[g])
        sizes = np.array(np.unique(model.labels_, return_counts=True))[1]



        # print('Cluster sizes: ', end=' ')
        # print(sizes)

        grouped_data[g]['predicted'] = model.labels_
        grouped_data[g].head()
        
    #cluster placed in pickle flie
    with open("DummyPreproccessedForDoc2Vec.pickle", "wb") as pickle_file:
        pickle.dump(grouped_data, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

    print("creating clusters for each component...")
    #pass component
    with open("DummyPreproccessedForDoc2Vec.pickle", "rb") as pickle_file:
        grouped_data = pickle.load(pickle_file)
    output =  open("output.txt", 'w')
    # groups = ['OMEGA', 'OMICRON', 'PHI', 'PI', 'PSI', 'RHO', 'SIGMA', 'TAU', 'THETA', 'UPSILON', 'XI', 'ZETA']
    groups = ['ALPHA', 'BETA', 'CHI', 'DELTA', 'EPSILON', 'ETA', 'GAMMA', 'IOTA', 'KAPPA', 'LAMBDA', 'MU', 'NU', 'OMEGA', 'OMICRON', 'PHI', 'PI', 'PSI', 'RHO', 'SIGMA', 'TAU', 'THETA', 'UPSILON', 'XI', 'ZETA']


    cluster_X = {}

    for g in groups:
        corpus = list(tagged_document(grouped_data[g]['Requirement']))
        d2v = gensim.models.doc2vec.Doc2Vec(vector_size=200, dm=0, min_count=2, epochs=50, seed=5)
        d2v.random.seed(5)
        d2v.build_vocab(corpus)
        d2v.random.seed(5)
        d2v.train(corpus, total_examples=d2v.corpus_count, epochs=d2v.epochs)
        # fit language model
        X = []
        for row in grouped_data[g]['Requirement']:
            d2v.random.seed(5)
            X.append(d2v.infer_vector(row.split(' ')))

        X = np.array(X)
        cluster_X[g] = X
        # print('Word embeddings shape: ', end=' ')
        # print(X.shape)
        # print(grouped_data)
        # Cluster
    print("writing clusters to output.txt...")

    dictionary = {}
    for g in groups:
        
        #FIXME: Each subgroup will have a different optimal K clusters... 
        # num_clusters = 6  
        if len(grouped_data[g]) < num_clusters:
            num_clusters = 1
            
        
        model = KMeans(n_clusters=num_clusters, init='k-means++', random_state=5).fit(cluster_X[g])
        # sizes = np.array(np.unique(model.labels_, return_counts=True))[1]
        # print('Cluster sizes: ', end=' ')
        # print(sizes)
        # print("cluster length")
        grouped_data[g]['Predicted_Cluster_#'] = model.labels_
        # print(grouped_data[g][0:len(model.labels_):500])

            ### VISUALIZE ### What requirements are in the cluster?

        # Update the following to inspect the clusters
        view = 'Requirement' # Uncomment to view prepocessed message 
        # view = 'Summary' # Uncomment to view original summary message 
        for cluster_number in range(num_clusters):
            # print(f'Component Name: {g}')
            # print(f'Cluster Number: {cluster_number}')
            clusters = list(grouped_data[g][view].loc[grouped_data[g]['Predicted_Cluster_#'] == cluster_number].head(20))
            # test_requirement = list(grouped_data[g][view].loc[grouped_data[g]['Predicted_Cluster_#'] == cluster_number].head(20))
            
            output.write(str(g + ' ' + str(cluster_number) + '?'))
            output.write(str(clusters))
            output.write('\n')

    print("reading clusters from output.txt...")
    with open("output.txt") as file:
        for line in file:
            (key, value) = line.split('?')
            #convert string list back to a list
            dictionary[key] = ast.literal_eval(value)
            # print(type(dictionary[key]))
    return dictionary

        # print(dictionary['ALPHA 0'])
# print ('\ntext file to dictionary=\n',dictionary)           
            # print("Testing Grouped Data...")
            # print(grouped_data[g][view])

            # if userInput in test_requirement:
            #         print(test_requirement)



# if __name__ == "__main__":
#     main()