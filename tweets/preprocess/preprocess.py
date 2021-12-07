# Necessary imports
import pandas as pd
import numpy as np
from .preprocess_functions import *

# Preprocess function which use the preprocess_functions defined in preprocess_functions.py
def preprocess(tweets_df):
    preprocessor = Preprocessor()
    tweets_df['social_count'] = tweets_df['favorite_count'] + tweets_df['retweet_count']
    tweets_df['positivity'] = tweets_df['user_tweets'].apply(preprocessor.getPositiveSentiment)

    tweets_df['tweet_length'] = tweets_df['user_tweets'].apply(len)
    tweets_df['user_tweets'] = tweets_df['user_tweets'].apply(preprocessor.remove_links)
    tweets_df['tweet_type'] = tweets_df['social_count'].apply(preprocessor.classifyTweets)
    tweets_df['tweetLengthType'] = tweets_df['tweet_length'].apply(preprocessor.classifyTweetLength)
    return tweets_df
