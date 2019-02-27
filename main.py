import tweepy                                # Twitter API wrapper
import pandas as pd                          # Pandas package
import numpy as np                           # Numpy package
import re                                    # Regex support
from textblob import TextBlob                # Package for sentiment analysis
from dev_logins import *                     # User-defined file that needs to be set up before use
from many_stop_words import get_stop_words   # Import of stop words

class Collect: 
   """Class sets up API and collects 1000 tweets"""
   text_lst = []

   def__init__(self):
      api = api.self


   def api_setup():
      """ Uses keys and tokens from dev_logins file to setup API access. Returns Tweepy API object """
      #Use imported keys/tokens to set up API. 
      auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_token_secret)
      api = tweepy.API(auth)

      return api

   def create_df():
   for tweet in tweepy.Cursor(api_setup().search, q='%23engvwales+-filter%3Aretweets%27').items(1000):
         text_lst.append(tweet.text)

   tweets = pd.DataFrame(text_lst, columns=['text'])
   tweets["Sentiment"] = ""

class Process:

   def clean_tweets(df): 
      """ For tweets in a Pandas dataframe under a column called 'text', will remove special characters and hyperlinks"""
      for index, row in df.iterrows():
         msg = row['text']
         msg = msg.lower()
         #Regex statement to remove hyperlinks and special characters
         msg = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", msg).split())
         row['text'] = msg

      return df

   def remove_stops(df):
      """ For tweets in a Pandas dataframe under a column called 'text', will remove all stop words from 'many_stop_words' package """
      stop_words = list(get_stop_words('en')) 
      for index, row in df.iterrows():
         msg = row['text'].split(" ")
         newmsg = ""
         for word in msg:
            if word not in stop_words:
               newmsg = newmsg + " " + word
      return df

stop_words = list(get_stop_words('en')) 
print(stop_words)

# tweets = clean_tweets(tweets)
# tweets = remove_stops(tweets)

# print(tweets)

