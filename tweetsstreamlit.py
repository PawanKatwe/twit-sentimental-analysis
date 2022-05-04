# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 21:25:29 2021

@author: PawanK
"""
#importing required libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from textblob import TextBlob
import tweepy
import re
from wordcloud import WordCloud
import streamlit as st

#assinging secret keys and token

## api removed from public code please use your own api

consumer_key = #
consumer_key_s = #
access_token = #
access_token_s = #
#authenticating
auth = tweepy.OAuthHandler(consumer_key, consumer_key_s)
auth.set_access_token(access_token,access_token_s)
api = tweepy.API(auth)

def main():
    st.title("Sentiment Analysis of tweets")
    
if __name__=='__main__':
        main()
        
#searchcriteria
searchtype = st.selectbox("search with",('Username','Hashtag'))
searchvalue = st.text_input("Enter usrer name or hashtag")


#searching the tweets
def searchValue():
    if searchtype == 'Hashtag':
       searchv  = api.search(searchvalue, count = 1000, lang='en', tweet_mode= 'extended')
       return searchv
    elif searchtype == 'Username':
        searchv = api.user_timeline(screen_name = searchvalue,count = 1000 ,lang='en', tweet_mode= 'extended')
        return searchv
    else:
        print('ok')

searchv = searchValue()

#creating dataframe
if searchtype == 'Username':
    data = pd.DataFrame([tweet.full_text for tweet in searchv], columns=['tweets'])
elif searchtype == 'Hashtag':
    data = pd.DataFrame([tweet.full_text for tweet in searchv], columns=['tweets'])
else:
    pass


#creating the function to clean the text 
def cleanText(text):
    text = re.sub(r'@[A-Za-z0-9_:]+', '', text) #removin @mention
    text = re.sub(r'#', '', text) #removing '#' syboll
    text = re.sub(r'RT[\s]+', '', text) #removing retweets
    text = re.sub(r'https?:\/\/\S+', '', text) #removing links
    
    return text

data['tweets'] = data['tweets'].apply(cleanText)

#creting a funcitno to get subjectivity
def getSubejectivity(text):
    return TextBlob(text).sentiment.subjectivity

#creating a function to get polarity 
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

#creating a new column for subjectivity and polority 
data['Polarity'] = data['tweets'].apply(getPolarity)
data['Subjectivity'] = data['tweets'].apply(getSubejectivity)

#plot the wordclaud
def PlotWordcloud():
    allwords = ''.join(twts for twts in data['tweets'])
    wrdcld = WordCloud(width = 500, height=300, random_state=21, max_font_size= 120).generate(allwords)
    plt.axis('off')
    fig, ax = plt.subplots()
    ax = plt.imshow(wrdcld, interpolation = 'bilinear')
    return fig

st.pyplot(PlotWordcloud())

#plotting the subjectivity and poloarity 
def scatterPlot():
    plt.figure(figsize=(15,7))
    plt.title('Sentimental Analysis')
    plt.xlabel('Tweets')
    plt.ylabel('Polarity & Subjectivity')
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=data.iloc[:,1:2])
    return fig

st.pyplot(scatterPlot())
#creating fucntion for analysis
def computePositivity(polarityvalue):
    if polarityvalue > 0:
        return "Positive"
    elif polarityvalue < 0:
        return "Negative"
    else:
        return "Nutral"
    
data['Analysis'] = data['Polarity'].apply(computePositivity)
   
st.write(data)

