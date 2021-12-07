from app_reviews.graphs.AppReviewGraphRenderer import AppReviewGraphRenderer
from textblob import TextBlob
import re
import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.parsing.preprocessing import (preprocess_string, strip_punctuation, strip_numeric)

class CustomReviewUtils:
    def __init__(self, reviews_df):
        self.reviews_df = reviews_df
       

    def renderCustomReviewGraphs(self):
        renderer = AppReviewGraphRenderer(self.reviews_df)
        emotional_chart, behavorial_chart, iptc_chart = renderer.drawBehavorialEmotionalChart()
        top_keywords_chart = renderer.drawTopKeywords()
        positive_reviews, negative_reviews = self.reviews_split(self.reviews_df)

        context = {
            "emotional_chart" : emotional_chart,
            "behavioral_chart" : behavorial_chart,
            "top_keywords_chart" : top_keywords_chart,
            "positive_reviews" : positive_reviews,
            "negative_reviews" : negative_reviews
        }

        return context

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
