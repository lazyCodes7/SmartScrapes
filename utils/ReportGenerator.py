import pandas as pd
import numpy as np
from tweets.graphs.plot_graph import GraphRenderer
from tweets.user.user_context import getUserContext,getUserInfo
from collections import Counter
from tweets.user.user_details import *
from tweets.user.user_stats import *
# Util class to generate reports
class ReportGenerator:
    # Initializing with requried classes
    def __init__(self, tweet_utils, store_review_utils,username):
        self.tweet_utils = tweet_utils
        self.store_review_utils = store_review_utils
        self.username = username

    def generateReports(self):
        tweets_df = self.tweet_utils.tweets_df
        # Getting word frequencies
        twitter_keyword_insights,twitter_word_freq = self.getTopKeywordInsights(
            text=tweets_df['user_tweets']
        )
        # Getting some user details
        screen_name,image_url,followers,friends = getUserDetails(self.username)

        # Getting the topics from LDA model
        twitter_imp_topics = self.tweet_utils.get_topics()

        # Finding the dominant topics
        twitter_most_dominant, twitter_least_dominant = self.tweet_utils.findDominantTopics(
            twitter_imp_topics
        )

        # Getting some stats
        retweet_sum,screen_name,image_url,followers,friends,total_fav = getUserInfo(
            user = self.username,
            tweets_df = tweets_df
        )

        # Splitting reviews
        twitter_positive_reviews, twitter_negative_reviews = self.tweet_utils.reviews_split()

        try:
            # Splitting reviews
            playstore_positive_reviews, playstore_negative_reviews = self.store_review_utils.reviews_split(
                df = self.store_review_utils.app_reviews_df,
            )
            # Getting the topics from LDA model
            playstore_imp_topics = self.store_review_utils.get_topics(
                df = self.store_review_utils.app_reviews_df,
                type = "playstore"
            )
             # Finding the dominant topics
            playstore_most_dominant, playstore_least_dominant = self.store_review_utils.findDominantTopics(
                imp_topics = playstore_imp_topics
            )
            # Getting word frequencies
            playstore_keyword_insights,playstore_word_freq = self.getTopKeywordInsights(
                text=self.store_review_utils.app_reviews_df['reviews']
            )
            
        except:
            playstore_positive_reviews = ["Sorry we weren't able to find any reviews."]
            playstore_negative_reviews = ["Sorry we weren't able to find any reviews."]
            playstore_imp_topics = ["UNK"]
            playstore_least_dominant, playstore_most_dominant = ["UNK"],["UNK"]
            playstore_keyword_insights, playstore_word_freq = ["UNK","UNK"], {"0": ["UNK",1]}
        try:
            # Splitting reviews
            appstore_positive_reviews, appstore_negative_reviews = self.store_review_utils.reviews_split(
                df = self.store_review_utils.store_reviews_df
            )
            # Getting the topics from LDA model
            appstore_imp_topics = self.store_review_utils.get_topics(
                df = self.store_review_utils.store_reviews_df,
                type = "appstore"
            )
            # Finding the dominant topics
            appstore_most_dominant, appstore_least_dominant = self.store_review_utils.findDominantTopics(
                imp_topics = appstore_imp_topics
            )
            # Getting word frequencies
            appstore_keyword_insights,appstore_word_freq = self.getTopKeywordInsights(
                text=self.store_review_utils.store_reviews_df['reviews']
            )
        except:
            appstore_positive_reviews = ["Sorry we weren't able to find any reviews."]
            appstore_negative_reviews = ["Sorry we weren't able to find any reviews."]
            appstore_imp_topics = ["UNK"]
            appstore_least_dominant, appstore_most_dominant = ["UNK"],["UNK"]
            appstore_keyword_insights, appstore_word_freq = ["UNK","UNK"], {"0": ["UNK",1]}


        # Creating context which would be used to access these values in the html file
        context = {
            "twitter_keyword_insights" : twitter_keyword_insights,
            "twitter_word_freq" : twitter_word_freq,
            "appstore_keyword_insights" : appstore_keyword_insights,
            "appstore_word_freq" : appstore_word_freq,
            "playstore_keyword_insights" : playstore_keyword_insights,
            "playstore_word_freq" : playstore_word_freq,
            "image_url" : image_url,
            "screen_name" : screen_name,
            "followers" : followers,
            "retweets" : retweet_sum,
            "friends" : friends,
            "total_fav" : total_fav,
            "user" : self.username,
            "twitter_positive_reviews" : twitter_positive_reviews,
            "twitter_negative_reviews" : twitter_negative_reviews,
            "playstore_positive_reviews" : playstore_positive_reviews,
            "playstore_negative_reviews" : playstore_negative_reviews,
            "appstore_positive_reviews" : appstore_positive_reviews,
            "appstore_negative_reviews" : appstore_negative_reviews,
            "twitter_imp_topics" : twitter_imp_topics,
            "appstore_imp_topics" : appstore_imp_topics,
            "playstore_imp_topics" : playstore_imp_topics,
            "appstore_most_dominant" : appstore_most_dominant,
            "appstore_least_dominant" : appstore_least_dominant,
            "playstore_most_dominant" : playstore_most_dominant,
            "playstore_least_dominant" : playstore_least_dominant,
            "twitter_most_dominant" : twitter_most_dominant,
            "twitter_least_dominant" : twitter_least_dominant,
        
        }
        return context

    # Function to get some insights from keywords
    def getTopKeywordInsights(self,text):
        cnt = Counter(" ".join(text).split()).most_common(10)
        word_frequency = pd.DataFrame(cnt, columns=['Top Keywords', 'Frequency'])
        keyword_insights = [
            word_frequency['Top Keywords'][word_frequency['Frequency'].argmin()],
            word_frequency['Top Keywords'][word_frequency['Frequency'].argmax()]
        ]
        return_cnt = {}
        for idx, (keyword, freq) in enumerate(cnt):
            return_cnt[idx] = [keyword, freq]
        
        return keyword_insights,return_cnt