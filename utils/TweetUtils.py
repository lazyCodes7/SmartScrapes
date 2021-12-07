# Necessary imports
import pandas as pd
import tweepy
from tweets.preprocess.preprocess import *
import os
from dotenv import load_dotenv
from textblob import TextBlob
import gensim
import gensim.corpora as corpora
from gensim.parsing.preprocessing import (preprocess_string, strip_punctuation, strip_numeric)
load_dotenv() 
class TweetUtils:
    def __init__(self):
        # Initializing the utils class
        self.tweets_df = None
        self.consumer_key = os.environ['CONSUMER_KEY']
        self.consumer_secret = os.environ['CONSUMER_SECRET']
        self.access_key = os.environ['ACCESS_KEY']
        self.access_secret = os.environ['ACCESS_SECRET']

    def populateDataFrame(self, df):
        # Populate dataframe with collected twitter data
        self.tweets_df = df
    
    def getDataFrame(self):
        return self.tweets_df

    def get_tweets(self, username):
        # Authorization to consumer key and consumer secret
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)

        # Access to user's access key and access secret
        auth.set_access_token(self.access_key, self.access_secret)

        # Calling api
        api = tweepy.API(auth)

        # 100 tweets to be extracted
        number_of_tweets=100
        tweets = api.user_timeline(screen_name=username,count=number_of_tweets)
        retweet_count = []
        texts = []
        possibly_sensitive = []
        favorite_count = []
        for tweet in tweets:
            texts.append(tweet.text)
            retweet_count.append(tweet.retweet_count)
            favorite_count.append(tweet.favorite_count)
          
        
        dict = {"user_tweets" : texts, "retweet_count" : retweet_count, "favorite_count" : favorite_count, "unfiltered": texts}
        df = pd.DataFrame(dict)
        df = preprocess(df)
        self.tweets_df = df

        return self.tweets_df
    
    
    def reviews_split(self):
        # Functions to split reviews based on sentiments
        positive_reviews = []
        negative_reviews = []
        reviews = self.associate_reviews()
        for review in reviews:
            analysis = TextBlob(review)
            if analysis.sentiment.polarity > 0:
                positive_reviews.append(str(review))
            else:
                negative_reviews.append(str(review))
        return (sorted(positive_reviews),sorted(negative_reviews))

    def associate_reviews(self):
        # Sorting the reviews
        reviews = self.tweets_df.unfiltered.tolist()
        unique_words = set(reviews)
        freq = {}
        for w in unique_words:
            freq[w] = reviews.count(w)
        sorted_freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
        result = []
        for r in reviews:
            for word in sorted_freq.keys():
                if word in r and len(r) > 10:
                    r.replace('\n','')
                    result.append(r)
        return list(set(result))

    # Using gensim to generate imp topics
    def get_topics(self):
        ## List conversion
        topics = [d.split() for d in self.tweets_df['user_tweets'].tolist()]
        ## Mapping words to indexes by passing our documents
        id2word = corpora.Dictionary(topics)
        ## Creating the corpus using the bow model
        self.corpus = [id2word.doc2bow(text) for text in topics]
        self.lda_model = gensim.models.ldamodel.LdaModel(
            corpus=self.corpus,
            id2word=id2word,
            num_topics=10, 
            random_state=100,
            update_every=1,
            chunksize=100,
            passes=10,
            alpha='auto',
            per_word_topics=True
        )
        ## Generating the topics 
        lda_topics = self.lda_model.show_topics(num_words=10)
        imp_topics = []
        ## Preprocessing the topics acquired
        filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]
        for topic in lda_topics:
            ## Appending to the list of imp_topics
            imp_topics.append(" ".join(preprocess_string(topic[1], filters)))
        
        ## Returning the topics
        self.imp_topics = imp_topics
        return self.imp_topics

    def findDominantTopics(self, imp_topics):
        ## Getting our corpus
        corpus_sel = self.corpus
        dominant_topics = []
        topic_percentages = []
        for i, corp in enumerate(corpus_sel):
            ## Getting topic percs and ids for topics by passing our corpus to the model
            topic_percs, wordid_topics, wordid_phivalues = self.lda_model[corp]
            ## Sorting the topic in reverse fashion
            dominant_topic = sorted(topic_percs, key = lambda x: x[1], reverse=True)[0][0]
            ## Appending it
            dominant_topics.append((i, dominant_topic))
            topic_percentages.append(topic_percs)
        
        ## Returning the most important and least important topic
        df = pd.DataFrame(dominant_topics, columns=['Document_Id', 'Dominant_Topic'])
        dominant_topic_in_each_doc = df.groupby('Dominant_Topic').size()
        df_dominant_topic_in_each_doc = dominant_topic_in_each_doc.to_frame(name='count').reset_index()
        most_imp_topic = imp_topics[df_dominant_topic_in_each_doc['count'].argmax()].split(" ")
        print("most:".format(most_imp_topic))
        least_imp_topic = imp_topics[df_dominant_topic_in_each_doc['count'].argmin()].split(" ")
        return (most_imp_topic, least_imp_topic)


