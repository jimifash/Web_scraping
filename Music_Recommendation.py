#!/usr/bin/env python
# coding: utf-8

# # Music Recommendation

# In[2]:


#import libraries
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import Webscrape


# In[3]:


#load the scraped and cleaned data
df = pd.read_csv("Boomplay Scraped songs.csv")
df


# In[4]:


#Copy dataset to avoid tampering with the original
df_new = df.copy()


#convert timestamp to string
df_new['time']=df_new['time'].astype('str')
df_new['a_age']=df_new['a_age'].astype('str')


# In[5]:


#check
df_new.info()


# In[6]:


#Create tags
df_new['tags'] = df_new['song_name']+df_new['artist_name']+df_new['a_age']+df_new['time']
df_new['song_name'] = df_new['song_name'].apply(lambda x:x.strip())
df_new


# In[7]:


#vectorize the tags
cv = CountVectorizer(max_features=5000, stop_words='english')


# In[8]:


#Reducing or stemming words to it's roots
ps = nltk.stem.PorterStemmer()


def stem(obj):
    y = []
    for i in obj.split():
        y.append(ps.stem(i))
    return " ".join(y)


# In[9]:


df_new['tags'] = df_new['tags'].apply(stem)


# In[10]:


vector = cv.fit_transform(df_new['tags']).toarray()
vector


# In[11]:


#finding the cosine similarities in the vector using cosine siimilarities

similarity = cosine_similarity(vector)


# In[25]:


similarity.shape


# In[14]:


#reduce all the song title to lower case
df_new['song_name'] = df_new['song_name'].apply(lambda x:x.lower())


# In[49]:

def recommend(key):
    key = key.lower()
    matching_rows = df_new[df_new['song_name'] == key]
    
    if not matching_rows.empty:
        index = matching_rows.index[0]
        sim_row = similarity[index]
        song_ls = sorted(list(enumerate(sim_row)), reverse=True, key=lambda x: x[1])[1:15]

        recommended_songs = [df_new.iloc[i[0]].song_name for i in song_ls]
        return recommended_songs
    else:
        return ["Song not found"] 
        


# # FINAL OUTPUT TEST
# 

# In[50]:



# # Ask for Recommendations

# In[17]:


#while True:
#    try:
#        # Prompt the user for input
#        input_ = input("Enter your song:\n")
        
#        if not input_:
#            # If the user didn't enter anything, break out of the loop
#            break

#        # Call the recommend function with the user's input
#        recommend(input_)

#    except Exception as e:
#        # Handle any exceptions that occur during the processing
#        print("Not in our database")
#        print("Please try again.")

#print("Exiting the program.")



# In[ ]:




