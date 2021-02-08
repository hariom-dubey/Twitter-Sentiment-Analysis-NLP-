# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 09:46:38 2021

@author: Hariom
"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

data = pd.read_csv('./data/sentiments.csv')

y = data['label'].values

#data preprocessing
corpus = []
ps = PorterStemmer()

for sentence in data['tweet']:
    temp = re.sub('[^a-zA-Z]', ' ', sentence)
    temp = temp.lower()
    temp = nltk.word_tokenize(temp)
    temp = [ps.stem(word) for word in temp if word not in stopwords.words('english')]
    temp = ' '.join(temp)
    corpus.append(temp)


model = make_pipeline(CountVectorizer(max_features=2000), MultinomialNB())

model.fit(corpus, y)

dict_sent = {
    0 : 'negative',
    2 : 'neutral',
    4 : 'positive',
    }

def get_type(txt):
    temp = re.sub('[^a-zA-Z]', ' ', txt)
    temp = temp.lower()
    temp = nltk.word_tokenize(temp)
    temp = [ps.stem(word)for word in temp if word not in stopwords.words('english')]
    temp = ' '.join(temp)

    emotion_index = model.predict([temp])

    return dict_sent[emotion_index[0]]