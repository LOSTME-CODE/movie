# -*- coding: utf-8 -*-
"""mrs.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bNZr2KE6msSjt0J4JGM3zdS69gNAFzBI
"""

# Importing libraries and mounting drive
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


movies= pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

movies.head(1)

credits.head(1)

credits.head(2)['crew'].values

movies=movies.merge(credits,on='title')

movies.head(1)

movies.columns

movies=movies[['genres','keywords', 'overview',  'title', 'movie_id', 'cast', 'crew']]

"""data preprocessin

"""

movies.isnull().sum()

movies.dropna(inplace=True)   # removing 3 overview -missig column

movies.duplicated().sum()    # checking two duplicate row

movies.iloc[0].genres

# changing in form ['ation','adven','ffantasy','sci/fic']

# def convert (obj):
 # L=[]
  #for i in obj:
   # L.append(i['name'])
  #return L

# as it in string cant get outpt as desired
import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')

def convert (obj):
  L=[]
  for i in ast.literal_eval(obj):
    L.append(i['name'])
  return L

movies['genres']=movies['genres'].apply(convert)

movies['keywords']=movies['keywords'].apply(convert)

movies.head(1)

# cast only 3 imp
def convert3 (obj):
  L=[]
  counter=0
  for i in ast.literal_eval(obj):
    if counter !=3:
     L.append(i['name'])
     counter+=1
    else :
     break
  return L

movies['cast']=movies['cast'].apply(convert3)

movies.head(1)

# fetch director
def fdir (obj):
  L=[]
  for i in ast.literal_eval(obj):
    if i['job']=='Director':
        L.append(i['name'])
        break
  return L

movies['crew']=movies['crew'].apply(fdir)

movies['overview'][0]

movies['overview'] = movies['overview'].astype(str)

# # movies['overview'] = movies['overview'].apply(lambda x: x if isinstance(x, str) else None)
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies.head()

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])   #removing sace

movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])

movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])

movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])

movies.head(1)

# Concatenate values from different columns into a new 'tags' column with spaces
movies['tags'] = (movies['overview'].astype(str) + ' ' + movies['genres'].astype(str) + ' ' + movies['keywords'].astype(str) + ' ' + movies['cast'].astype(str) + ' ' + movies['crew'].astype(str))

#movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Remove leading and trailing spaces
movies['tags'] = movies['tags'].str.strip()

movies.head(1)

df=movies[['movie_id','title','tags']]

df
# Ensure every element in 'tags' is a list
movies['tags'] = movies['tags'].apply(lambda x: x if isinstance(x, list) else [x])

# Flatten the lists and join into a single string for each row
movies['tags'] = movies['tags'].apply(lambda x: ' '.join([str(elem) for elem in x]))

#df['tags']=df['tags'].apply(lambda x:" ".join(x))
df['tags'] = df['tags'].apply(lambda x: ' '.join([word for word in x.split() if word]))

df['tags'][0]

# Remove brackets and commas from the 'tags' column
df['tags'] = df['tags'].str.replace('[', '').str.replace(']', '').str.replace(',', '')

# Remove leading and trailing spaces
df['tags'] = df['tags'].str.strip()

df['tags'][0]

print(df.head(1))

from sklearn.feature_extraction.text import CountVectorizer

cv=CountVectorizer(max_features=5000,stop_words='english')

vectors= cv.fit_transform(df['tags']).toarray()    # #.shape

##from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text

# Preprocess 'tags' column to remove empty strings
df['tags'] = df['tags'].apply(lambda x: ' '.join([word for word in x.split() if word]))

# Define CountVectorizer with custom stop words
stop_words = text.ENGLISH_STOP_WORDS.union(["'"])  # Add any additional stop words
cv = CountVectorizer(stop_words='english', max_features=5000)

# Apply CountVectorizer to 'tags' column
vectors= cv.fit_transform(df['tags']).toarray()

# Define custom stop words as a list
#custom_stop_words = ['the', 'of', 'and','but','i','or','so']
#Define CountVectorizer with custom stop words
#cv = CountVectorizer(stop_words=custom_stop_words)

# Apply CountVectorizer to 'tags' column
#X = cv.fit_transform(df['tags']).toarray().shape

cv.get_feature_names_out()
import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
  y=[]

  for i in text.split():
    y.append(ps.stem(i))

  return " ".join(y)

df['tags']=df['tags'].apply(stem)

from sklearn.metrics.pairwise import cosine_similarity
#similarity = cosine_similarity(vectors).shape

# Compute the cosine similarity matrix
similarity = cosine_similarity(vectors)

similarity[1]
sorted(list(enumerate(similarity[1])),reverse=True,key=lambda x:x[1])[1:6]

df.iloc[1216].title

# Define the recommend function
def recommend(movie):
    try:
        movie_index = df[df['title'] == movie].index[0]
    except IndexError:
        print(f"Movie '{movie}' not found in the dataset.")
        return

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#def recommend(movie):
    #movie_index=movies[movies['title']==movies].index[0]
    #distances=similarity[movie_index]
    #movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    #for i in movies_list:
      #print(df.iloc[i[0]].title)




import pickle

pickle.dump(df,open('movies1.pkl','wb'))
df['title'].values

pickle.dump(df,open('movies1.pkl','wb'))

pickle.dump(df,open('similarity.pkl','wb'))


pickle.dump(df.to_dict, open('movies1_dic.pkl', 'wb'))

