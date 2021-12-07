import pandas as pd
from .user_details import *
## Getting some user stats using these functions
def getTweetPopularityStats(tweets_df):
    max_value = tweets_df['tweet_type'].value_counts().argmax()
    max = tweets_df['tweet_type'].value_counts().max()
    min_value = tweets_df['tweet_type'].value_counts().argmin()
    min = tweets_df['tweet_type'].value_counts().min()
    max_index = tweets_df['tweet_type'].value_counts().index[max_value]
    min_index = tweets_df['tweet_type'].value_counts().index[min_value]
    return_tuple = (
        max,
        min,
        max_index,
        min_index,
    )
    return return_tuple
def getUserInfo(user,tweets_df):
    retweet_sum = tweets_df['retweet_count'].sum()
    screen_name,image_url,followers,friends = getUserDetails(user)
    total_fav = tweets_df['favorite_count'].sum()

    return_tuple = (
        retweet_sum,
        screen_name,
        image_url,
        followers,
        friends,
        total_fav
    )
    return return_tuple

def getTweetLengthStats(tweets_df):
    maxlengthtype_index = tweets_df['tweetLengthType'].value_counts().argmax()
    minlengthtype_index = tweets_df['tweetLengthType'].value_counts().argmin()
    maxlength_count = tweets_df['tweetLengthType'].value_counts().max()
    minlength_count = tweets_df['tweetLengthType'].value_counts().min()
    maxlengthtype_index = tweets_df['tweetLengthType'].value_counts().index[maxlengthtype_index]
    minlengthtype_index = tweets_df['tweetLengthType'].value_counts().index[minlengthtype_index]
    return_tuple = (
        maxlength_count,
        minlength_count,
        maxlengthtype_index,
        minlengthtype_index,
    )
    return return_tuple
def getSentimentStats(tweets_df):
    avg_sentiment = tweets_df['positivity'].mean()
    max_sentiment_value = tweets_df['positivity'].max()
    return (avg_sentiment,max_sentiment_value)