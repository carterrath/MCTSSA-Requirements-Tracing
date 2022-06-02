import pandas as pd
import nltk
import string 
from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
from sklearn import metrics
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from pandas import json_normalize


def inspect_cluster(grouped_data,por,cluster_number):
    '''Visualize what requirements are in a cluster.
    
    Args:
        grouped_data: object containing clusters and requirements
        por: POR subgroup
        cluster_number: cluster number you want to visualize
    
    Returns:
        list of requirements in cluster
    '''
    return list(grouped_data[por]['Requirement'].loc[grouped_data[por]['predicted'] == cluster_number])

def lemmatize(tokens):
    '''Lemmatizes words in list. Used in preprocess_text.
    
    Args:
        tokens: list of words to be lemmatized
    
    Returns:
        lemmas: list of lemmatized words
    '''
    lemmer = WordNetLemmatizer()
    lemmas = []
    for word, tag in nltk.pos_tag(tokens):
        pos = tag[0].lower()
        if pos in ('a', 'r', 'n', 'v'):
            lemma = lemmer.lemmatize(word, pos)
        else:
            lemma = lemmer.lemmatize(word)
        lemmas.append(lemma)
    return lemmas

def preprocess_text(text, my_stop_words, keep_original, display, pos_tags):
    '''Preprocesses text fields to convert to lowercase, remove any text in < >,
    and remove punctuation and stopwords.
    
    Args:
        text (str, list, pd.Series): The text to be preprocessed
        keep_original: if True, then do not remove stopwords or lemmatize.
        display: if True, then do not remove digits or capitalization.
     
    Returns:
        new_text: a list of strings that have been preprocessed
    '''
    #new_text = []
    my_stop_words = my_stop_words + stopwords.words('english')
    stop_words_nltk = set(my_stop_words)
    punct = dict.fromkeys(map(ord, string.punctuation))
    tmp_sent = text
    tmp_sent = re.sub(r'/', ' ', tmp_sent)
#     try:  
    if pos_tags:
        pos_temp = nltk.tokenize.word_tokenize(tmp_sent)
        tags = nltk.pos_tag(pos_temp)          
        tags_pos = [tag for word, tag in tags]
        pos_words = [word for word, tag in tags]

    if display == False:
        # removes anything not alphanumeric
        tmp_sent = [char for char in tmp_sent if char.isalnum() or char == ' '] 

        # convert back to string
        tmp_sent = ''.join([i for i in tmp_sent]) 

        # make lowercase
        tmp_sent = tmp_sent.lower() 

        if pos_tags:
            # Replaced commented below with keep_alphanumeric 
#             pos_words = ' '.join(pos_words)
#         removes anything not alphanumeric
#             pos_words = [char for char in pos_words if char.isalnum() or char == ' '] 
#             tags_pos = [char for char in tags_pos if char.isalnum() or char == '$' or char=='PRP$' or char == ' ' or char == 'WP$']
            pos_words, tags_pos = keep_alphanumeric(pos_words, tags_pos)
        
            # convert back to string
            pos_words = ' '.join([i for i in pos_words])
            # make lowercase
            pos_words = pos_words.lower()

            # tokenize
            pos_words = nltk.tokenize.word_tokenize(pos_words)


    # tokenize        
    tmp_sent = nltk.tokenize.word_tokenize(tmp_sent) 

    if keep_original == False:
        # lemmatize
        tmp_sent = lemmatize(tmp_sent) 

        # remove stop words
        tmp_sent = [w for w in tmp_sent if not w in stop_words_nltk]

        if pos_tags:
            # lemmatize
            pos_words = lemmatize(pos_words)

            # remove stop words
            tags_pos = [tags_pos[i] for i in range(len(pos_words)) if not pos_words[i] in stop_words_nltk]
            pos_words = [w for w in pos_words if not w in stop_words_nltk]

    # restring
    new_text = ' '.join(tmp_sent)                                 

#     except:
#         new_text = None
        
    if pos_tags:
        new_tags = []
        pos = nltk.tokenize.word_tokenize(new_text)

        for word in pos:
            try:
                new_tags.append(tags_pos[pos_words.index(word)])
            except:
                pos.remove(word)
        new_text = ' '.join(pos)        
        return new_text, new_tags
    else:
        return new_text

    
def helper(pos_words,tags_pos):
    print(len(pos_words),len(tags_pos))
    for i in range(min(len(pos_words),len(tags_pos))):
        print(pos_words[i],tags_pos[i], end = ', ')
    print()
    
def keep_alphanumeric(pos_words,tags_pos):
    if len(pos_words) == len(tags_pos):
        new_pos_words = []
        new_tags_pos = []
        for i in range(len(tags_pos)):
            string = ''
            for char in pos_words[i]:
                if char.isalnum() or char == ' ':
                    string = string + char
            if string != '':
                new_pos_words.append(string)
                new_tags_pos.append(tags_pos[i])
            else:
                continue
        return new_pos_words, new_tags_pos
    else:
        print('pos_words and tags_pos deos not have the same number of elements', len(pos_words), len(tags_pos)) 

def count_freq_by_group(dataframe, column_name):
    '''Finds the frequency or occurrence of each element, grouped according to a
    column of the dataframe.
    
    Args:
        dataframe (Pandas data frame): A tabular data frame for analysis.
        column_name (str): The column name to find and tally the element names.
     
    Returns:
        freq_table: The number of occurrences or rows per element.
    '''
    list_elements = dataframe.groupby(by=column_name)
    freq_table = list_elements.size()
    return freq_table

def count_vocab_freq(vocabulary_abc, corpus):
    '''Finds the frequency of each word inside a corpus of documents and/or 
    corpuses.

    Args:
        vocabulary_abc (dict): Dictionary of vocabulary words from TfidfVectorizer()
        library, with the dictionary's value being the alphabetical rank of the word.
        corpus (list): Each element shows each message in a corpus.

    Returns:
        vocabulary_freq (dict): Dictionary showing the frequency of each vocabulary
        word in the corpus.
    '''
    vocab_set = set(vocabulary_abc.keys())

    vocabulary_freq = dict.fromkeys(vocab_set, 0)
    for message in corpus:
        msg_word_list = message.split(" ")
        for word in msg_word_list:
            try:
                vocabulary_freq[word] += 1
            except KeyError:
                pass
    # Sort values from highest to lowest frequency
    vocabulary_freq = dict(sorted(vocabulary_freq.items(),
                                  key=lambda item: item[1],
                                  reverse=True))

    return(vocabulary_freq)