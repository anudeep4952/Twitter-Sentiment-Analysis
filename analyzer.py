'''
hash_tag_list = ["worldcup", "newzeland", "england"]
    fetched_tweets_filename = "tweets.json"
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    print(twitter_streamer)
    # twitter_client=TwitterClient("Samanthaprabhu2")
    # print(twitter_client.get_friend_list(10))


    listener = StdOutListener("tweets.json")
        auth=self.twitter_autenticator.authenicate_twitter_app()
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)


'''



from  tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from  tweepy import Stream
from tweepy import API
from tweepy import Cursor

from textblob import TextBlob

import twitter_credentials

import numpy as np
import pandas as pd
import re


#twitter client
class TwitterClient():
    def __init__(self,twitter_user=None):
       self.auth=TwitterAuthenicator().authenicate_twitter_app()
       self.twitter_client=API(self.auth)
       self.twitter_user=twitter_user

    def get_twitter_client_api(self):
        return  self.twitter_client


    def get_user_timeline_tweets(self,num_tweets):
        tweets=[]
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
       # print(len(tweets))
        return tweets
    def get_friend_list(self,num_friends):
        friend_list=[]
        for friend in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list
    def get_homeline_twets(self,num_tweets):
        tweets=[]
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweet


#TWITTER_AUTHENICATOR
class TwitterAuthenicator():
    def authenicate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


#TWITTER_STREAMER
class TwitterStreamer():
    '''
    class for straeming live tweets
    '''

    def __init__(self):
        self.auth = TwitterAuthenicator().authenicate_twitter_app()
        self.api = API(self.auth)
        self.twitter_autenticator=TwitterAuthenicator()

    def stream_tweets(self,hash_tag_list):
        results = []
        for tweet in Cursor(self.api.search, q=hash_tag_list, lang="en").items(20):
            results.append(tweet)
        return results

        #this handles twitter authenication and the connection to twitter streamong api


class StdOutListener(StreamListener):
    '''this is a basic listner clas that just prints received tweets to stdout'''

    def __init__(self,fetched_tweets_filname):
        self.fetched_tweets_filname=fetched_tweets_filname

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filname,'a') as tf:
               tf.write(data)
            return True
        except BaseException as e:
            print("error on data : %s" %str(e))

    def on_error(self, status_code):
        if status_code==420:
            return False
            #rate exceeded

        print(status_code)
class TweetAnalyzer():
    '''
    functionalit for analyzing and categorizing content from tweets.
    '''

    def clean_tweet(self,tweet):
        x= ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        return x
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self,tweets):
        df=pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['tweets'])
        '''df['id']=np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
'''
        return df




if __name__=="__main__":
  n=int(input("1:hashtag\n2:profile\n"))
  tweet_analyzer = TweetAnalyzer()
  if n==1:
     t = TwitterStreamer()
     h = input("enter hash tag : ")
     tweets = t.stream_tweets(h)
  elif n==2:
      twitter_client = TwitterClient()
      api = twitter_client.get_twitter_client_api()
      h = input("enter person id : ")
      tweets = api.user_timeline(screen_name=h, count=20)
  else:
      exit(0)


  df = tweet_analyzer.tweets_to_data_frame(tweets)
  df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
  df['text'] = np.array([tweet_analyzer.clean_tweet(tweet) for tweet in df['tweets']])

 # print(df[['text','sentiment']])
 #print(df['sentiment'].value_counts().idxmax())
  score=df['sentiment'].value_counts().idxmax()

  if score==0:
      print("neutral")
  if score==1:
      print("positive")
  if score==-1:
      print("negative")
''' 
    print(dir(tweets[0]))
'''




