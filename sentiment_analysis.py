#importing libraries
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

#loading data
data = pd.read_csv('./sentiments.csv')

y = data['label'].values

corpus = []

#used for applying stemming to the data
ps = PorterStemmer()
#data preprocessing
for sentence in data['tweet']:
    temp = re.sub('[^a-zA-Z]', ' ', sentence)
    temp = temp.lower()
    temp = nltk.word_tokenize(temp)
    temp = [ps.stem(word) for word in temp if word not in stopwords.words('english')]
    temp = ' '.join(temp)
    corpus.append(temp)


#applying BOG and transforming sentences into Vectors
cv = CountVectorizer(max_features=1500)
x = cv.fit_transform(corpus).toarray()

#splitting the data
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size = 0.20, random_state = 0)

#naive bayes algorithm
nb = MultinomialNB()

nb.fit(train_x, train_y)

y_pred = nb.predict(test_x)

mat = confusion_matrix(test_y, y_pred)
score = accuracy_score(test_y, y_pred)

print(score)