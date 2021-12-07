# Necessary imports
import re
import requests
import os
from expertai.nlapi.cloud.client import ExpertAiClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
from time import sleep
from dotenv import load_dotenv
from textblob import TextBlob
load_dotenv() 
# Setting up the access keys from the .env file
os.environ["EAI_USERNAME"] = os.environ['EMAIL']
os.environ["EAI_PASSWORD"] = os.environ['PASSWORD']
class Preprocessor:
    def __init__(self):
        self.client = ExpertAiClient()
        # Creating the corpus
        self.STOP_WORDS = stopwords.words()
        # Initalizing the lemmatizer
        self.wnl = WordNetLemmatizer()
        self.language = 'en'

    # Pre-processing function to get the rating involved in the review
    def cleanTraitRate(self, text):
        rating_text = text.split(" ")[1]
        return rating_text

    # Function used to create a new feature tweet-type
    def classifyTweets(self, count):
        if(count>20000):
            return "POPULAR"
        elif(count>10000 and count<20000):
            return "NORMAL"
        elif(count>0 and count<10000):
            return "UNPOPULAR"

    # Function used to create a new feature tweet-length type
    def classifyTweetLength(self, length):
        if(length>0 and length<50):
            return "SHORT TWEET"
        elif(length>=50 and length<=100):
            return "MEDIUM SIZED TWEET"
        elif(length>100 and length<=280):
            return "LONG TWEET"

    # Function used to create a new feature i.e sentiment
    def getPositiveSentiment(self, text):
        return (TextBlob(text).sentiment.polarity)*100

    # Preprocessing using NLTK library to remove noise in the data collected"
    def remove_links(self, text):

        # Removing RT text in tweets since it won't be useful
        text = text.replace("RT","")

        text = re.sub(r'\d+', "", text)

        # Removing hyperlinks
        text = re.sub('http://\S+|https://\S+', '', text)

        # Removing emojis
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"
                            u"\U0001F680-\U0001F6FF"
                            u"\U0001F1E0-\U0001F1FF"
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)

        # Removing some common symbols
        text = re.sub(r'@\w+',  '', text).strip()
        text = re.sub("[^a-zA-Z0-9 ']", "", text)

        # Using a lemmatizer to get a final text
        text=' '.join([self.wnl.lemmatize(i) for i in text.lower().split()])

        # Tokenize the text
        text_tokens = word_tokenize(text)

        # Itertating through the word and if a word is not in the stop words then adding it to the list
        tokens_without_sw = [word for word in text_tokens if not word in self.STOP_WORDS]

        # Getting the filtered sentence
        filtered_sentence = (" ").join(tokens_without_sw)
        text = filtered_sentence

        # Returning the transformed/filtered text
        return text
    
    