import tweepy                                # Twitter API wrapper
import pandas as pd                          # Pandas package
import numpy as np                           # Numpy package
import re                                    # Regex support
import seaborn as sns                        # Seaborn for plotting
from textblob import TextBlob                # Package for sentiment analysis
from dev_logins import *                     # User-defined file that needs to be set up before use
from many_stop_words import get_stop_words   # Import of stop words


def api_setup():

   """ Uses keys and tokens from dev_logins file to setup API access. Returns Tweepy API object """
   
   #Use imported keys/tokens to set up API. 
   auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_token, access_token_secret)
   api = tweepy.API(auth)

   return api

def collect_tweets(searchterm):

   """ Collects 1000 tweets matching searchterm through the api and returns a dataframe with a column of tweets """

   text_lst = []
   time_lst = []

   for tweet in tweepy.Cursor(api_setup().search, q=searchterm).items(1000):
      text_lst.append(tweet.text)
      time_lst.append(tweet.created_at)

   #Turn list into pandas dataframe object
   tweets = pd.DataFrame()
   tweets['text'] = text_lst
   tweets['time'] = time_lst
   
   return tweets

def remove_specials(df): 

   """ For tweets in a Pandas dataframe under a column called 'text', will remove special characters, hyperlinks"""

   for row in df.index:
      msg = df.loc[row,'text']
      msg = msg.lower()
      #Regex statement to remove hyperlinks and special characters
      msg = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", msg).split())
      df.loc[row,'text'] = msg

   return df

def remove_stops(df):

   """ For tweets in a Pandas dataframe under a column called 'text' will remove all stop words from 'many_stop_words' package """

   stop_words = list(get_stop_words('en')) 
   stop_words.append('rt') #add RT as a stopword because it does not add value to the dataset. 

   for row in df.index:

      #split message into list of individual words
      msg = df.loc[row,'text'].split(" ")
      newmsg = ""

      #for each word in the list, if it's not in stop_words then keep in by adding to newmsg. 
      for word in msg:
         if word not in stop_words:
            newmsg = newmsg + " " + word

      #reassign value of df cell as newmsg which has no stop words 
      df.loc[row,'text'] = newmsg

   return df

def clean_tweets(df):

   """ Cleans tweets in dataframe column 'tweets' ready for sentiment analysis """

   df = remove_specials(df)
   df = remove_stops(df)

   return df

def tweet_setup(searchterm):
   
   """ General function which returns a clean dataframe of 1000 tweets, matching the searchterm"""

   tweets = collect_tweets(searchterm)
   tweets = clean_tweets(tweets)

   return tweets

def sentiment_analysis(df):

   """ Given dataframe with tweets in 'text' column, returns dataframe with sentiment polarity and subjectivity for each tweet """

   df["Polarity"] = ""
   df["Subjectivity"] = ""

   for row in df.index: 
      df.loc[row,'Polarity'] = TextBlob(df.loc[row,'text']).sentiment.polarity
      df.loc[row,'Subjectivity'] = TextBlob(df.loc[row,'text']).sentiment.subjectivity

   return df

def visualise(df):
   """ Creates a bar chart of the number of positive, neutral and negative tweets """

   # Initialise counters
   pos = 0
   neu = 0 
   neg = 0

   #Count number of positive, negative and neutral tweets about brexit by polarity
   for row in df.index:
      if df.loc[row,'Polarity'] == 0:
         neu += 1
      elif df.loc[row,'Polarity'] < 0:
         neg += 1
      elif df.loc[row,'Polarity'] > 0:
         pos += 1
      
   # Use values gathered to create a bar plot of the distribution of tweet polarity
   polarity_dict = { 'Positive':pos, 'Neutral' : neu , 'Negative' : neg }
   df = pd.DataFrame.from_dict(data=polarity_dict, orient = 'index')
   sns.set(style="whitegrid")
   plot = sns.barplot(data = df.transpose())

   return plot
   

#Create a dataframe with tweets - search terms should be URL encoded. 
#Twitter dev site: https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators 

#tweets = tweet_setup('%23engvwales+-filter%3Aretweets%27')

brexit_tweets = tweet_setup('%23brexit%20-filter%3Aretweets')

brexit_tweets  = sentiment_analysis(brexit_tweets)

visualise(brexit_tweets)