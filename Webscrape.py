#!/usr/bin/env python
# coding: utf-8




#Import Libraries


from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
from datetime import datetime
import re
from matplotlib import pyplot as plt
import seaborn as sb

#functions
def append(value, destination):
    '''This function appends values to a list '''
    value.append(destination)

def DataFrame(col1,col2,col3,col4):
    '''This function collects dictionaries and turns the
     dictionaries into a dataframes and merges the datafrmaes to form
     a single dataframe'''


    first_c = pd.DataFrame(col1)
    second_c = pd.DataFrame(col2)
    third_c = pd.DataFrame(col3)
    forth_c = pd.DataFrame(col4)

    df = col1|col2|col3|col4 #merging the dataframe

    return df

#### SCRAPE BOOMPLAY FOR SONGS AND ARTISTS

url='https://www.boomplay.com/playlists/26356675?from=home' #The URL


response = requests.get(url)
#response
soup= BeautifulSoup(response.content, 'lxml')


#Dictionaries
song_name = {'song_name':[]}
artist = {'artist_name':[]}
time= []


#Getting the Song title and artist name 
#Song name
artist_list = []

song_data = soup.findAll('div', {'class':'songNameWrap'})
artist_data= soup.findAll('a', {'class':'artistName'})


index=1
while index < 31:
    name = song_data[index].text.replace('\n','').split('ft.')
    if len(name)>=2: 
        name=name[0]
        #print(name)
    else:
        name = name[0]
        #print(name)

    append(song_name['song_name'],name) #appending to song_name dict
    index = index+1

#song title    
i = 0 
while i<30:
    artist_name = artist_data[i].text
    artist['artist_name'].append(artist_name)
    artist_list.append(artist_name)
    i = i+1


# #### Programatic web search for artist's age

#loop for building the url
age_url =[]

for i in artist_list:
    #first_C ="'"
    #second_C ="'"
    url2= "https://en.wikipedia.org/wiki/"+ i
    
    append(age_url,url2)    #append to age_url

#getting and storing the artist age
error = []
artist_age = {'a_age':[]}
n=0
pattern = "[0-9]{4}|[0-9]{2}|[0-9]{2}"
for j in age_url:
    
    response1 = requests.get(j)

    try:
        soup1 = BeautifulSoup(response1.content,'html.parser')
        age_data = soup1.select_one('span span',{'class':'bday'})
        age = age_data.text
       #checking if the the age data mathes the pattern 
        if (re.search(pattern, age)):
            artist_age['a_age'].append(age)
        else:
            artist_age['a_age'].append('NA')

    except AttributeError:
        artist_age['a_age'].append('NA')
        error.append('NA')              



pd.DataFrame(artist_age)


#Getting run_time
time = {'time':[]}

for t in range(30):
    time_data = soup.findAll('li',{'class':'clearfix play_one'})
    append(time['time'],time_data[t].time.text)



### Creating DataFrames



df = DataFrame(song_name,artist, artist_age, time)
df = pd.DataFrame(df)

# #### Cleaning
#changing a_age column to datetime datatime

df.a_age = pd.to_datetime(df.a_age, errors='coerce', format='%Y-%m-%d')



#checking
#df.info()


#getting the exact age of each artist and putting the result in a new column
df['age']=datetime.today().year - df.a_age.dt.year 


df.rename(columns={'a_age':'dob'}, inplace = True) #renaming a_age column to dob(date of birth)

print(df)


# In[28]:


df.to_csv("Top_Naija_Music_Trends_Boom_play.csv") #saving the dataframe


# ### Visualization

#group = df.groupby([df.artist_name]).size()

#Making the visualization
#color=('black','black','black','yellow','black','black','yellow','black','black','black','black','black','yellow','black','black','black','black','black','black','black',)
sb.countplot(data = df, x=df.artist_name, color ='black')
plt.xticks(rotation = 90)
plt.title('ARTIST WTIH THE MOST AMOUNT OF TRENDING SONGS')
plt.yscale('log')
plt.show()

#print (graph)




