# Necessary Imports
from bs4 import BeautifulSoup
from app_reviews.scraper.playstore.AppReviewScraper import AppReviewScraper
from app_reviews.scraper.appstore.AppStoreReviewScraper import AppStoreReviewScraper
from app_reviews.graphs.AppReviewGraphRenderer import AppReviewGraphRenderer
import requests
from urllib.parse import unquote
from textblob import TextBlob
import re
import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.parsing.preprocessing import (preprocess_string, strip_punctuation, strip_numeric)

class StoreReviewUtils:
    def __init__(self):
        self.username = None
        self.scraper = None
        self.app_reviews_df = None
        self.store_reviews_df = None

    def setUsername(self, username):
        self.username = username

    def populateDataFrames(self, app_reviews_df, store_reviews_df):
        self.app_reviews_df = app_reviews_df
        self.store_reviews_df = store_reviews_df
    # Finding playstore reviews based on username provided
    def searchPlaystore(self, link = None):
        if(link == None):
            keyword = "google playstore"
            page = requests.get("https://www.google.dz/search?q={} {}".format(self.username, keyword))
            soup = BeautifulSoup(page.content)
            links = soup.findAll("a")
            scraped_links = []
            for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
                scraped_links.append(re.split(":(?=http)",link["href"].replace("/url?q=","")))
                break
            link = unquote(str(scraped_links[0]))

        print(link)
        link = link.split("&")[0]
        id = link[link.index('=')+1:]

        self.scraper = AppReviewScraper(app_id = id)
        self.app_reviews_df = self.scraper.get_reviews()

        return self.app_reviews_df

    # Finding appstore reviews based on username provided
    def searchAppStore(self, link = None):
        if(link == None):
            keyword = "appstore"
            page = requests.get("https://www.google.dz/search?q={} {}".format(self.username, keyword))
            soup = BeautifulSoup(page.content)
            links = soup.findAll("a")
            scraped_links = []
            for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
                scraped_links.append(re.split(":(?=http)",link["href"].replace("/url?q=","")))
                break
            link = unquote(str(scraped_links[0]))
        link = link.split("&")[0]

        name = link[30:link.rindex('/')]
        self.scraper = AppStoreReviewScraper(app_name = name)
        self.store_reviews_df = self.scraper.get_reviews()
        return self.store_reviews_df

    # Rendering graphs from appstore reviews
    def renderAppStoreGraphs(self):
        renderer = AppReviewGraphRenderer(self.store_reviews_df)
        emotional_chart, behavorial_chart, iptc_chart = renderer.drawBehavorialEmotionalChart()
        top_keywords_chart = renderer.drawTopKeywords()
        rating_bar_chart = renderer.drawRatingHistogram()
        rating_line_chart = renderer.drawRatingLinePlot()

        return {

                "emotional_chart" : emotional_chart,
                "behavorial_chart" : behavorial_chart,
                "iptc_chart" : iptc_chart,
                "top_keywords_chart" : top_keywords_chart,
                "rating_bar_chart" : rating_bar_chart,
                "rating_line_chart" : rating_line_chart,
        }

    # Rendering graphs from playstore reviews
    def renderPlaystoreGraphs(self):
        renderer = AppReviewGraphRenderer(self.app_reviews_df)
        emotional_chart, behavorial_chart, iptc_chart = renderer.drawBehavorialEmotionalChart()
        top_keywords_chart = renderer.drawTopKeywords()
        rating_bar_chart = renderer.drawRatingHistogram()
        rating_line_chart = renderer.drawRatingLinePlot()

        return {

                "emotional_chart" : emotional_chart,
                "behavorial_chart" : behavorial_chart,
                "iptc_chart" : iptc_chart,
                "top_keywords_chart" : top_keywords_chart,
                "rating_bar_chart" : rating_bar_chart,
                "rating_line_chart" : rating_line_chart,
        }

    
    def reviews_split(self,df):
        # Functions to split reviews based on sentiments
        positive_reviews = []
        negative_reviews = []
        reviews = self.associate_reviews(df)
        for review in reviews:
            analysis = TextBlob(review)
            if analysis.sentiment.polarity > 0:
                positive_reviews.append(str(review))
            else:
                negative_reviews.append(str(review))
        return (sorted(positive_reviews)[0:10],sorted(negative_reviews)[0:10])

    def associate_reviews(self, df):
        # Sorting the reviews
        reviews = df.reviews.tolist()
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
    def get_topics(self,df, type = "appstore"):
        ## List conversion
        topics = [d.split() for d in df['reviews'].tolist()]
        ## Mapping words to indexes by passing our documents
        id2word = corpora.Dictionary(topics)

        ## Creating the corpus using the bow model
        self.corpus = [id2word.doc2bow(text) for text in topics]

        ## Generating the topics 
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
        ## Getting the imp topics
        lda_topics = self.lda_model.show_topics(num_words=10)
        imp_topics = []

        ## Preprocessing the topics acquired
        filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]

        ## Appending to the list of imp_topics
        for topic in lda_topics:
            imp_topics.append(" ".join(preprocess_string(topic[1], filters)))

        ## Returning the topics
        if(type == "appstore"):
            self.imp_appstore_topics = imp_topics
            return self.imp_appstore_topics

        else:
            self.imp_playstore_topics = imp_topics
            return self.imp_playstore_topics

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
        least_imp_topic = imp_topics[df_dominant_topic_in_each_doc['count'].argmin()].split(" ")
        return (most_imp_topic, least_imp_topic)


        

