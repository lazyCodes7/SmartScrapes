# Necessary imports
import plotly.express as px
import plotly
import seaborn as sns
import matplotlib.pyplot as plt
import json
from collections import Counter
import pandas as pd
from expertai.nlapi.cloud.client import ExpertAiClient
from ..preprocess.preprocess_functions import *
from ..nlp_functions.sentiments import *
from reviews.nlp_functions.sentiments import *
class GraphRenderer:
    def __init__(self, df):
        self.df = df

    # Plotly graph for drawing the tweet length vs the tweet type
    def drawTweetTypeGraph(self):
        # Drawing the plot using plotly
        fig = px.histogram(self.df,y="tweet_type",color="tweetLengthType")

        # Converting the figure into JSON format which would then be displayed on the site
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Returning JSON response
        return plot_json

    # Visualization for top keywords found
    def drawTopKeywords(self):
        # Counting 10 most used words from the tweets
        tweets = self.df['user_tweets']
        cnt = Counter(" ".join(tweets).split()).most_common(10)

        # Converting it to a DataFrame
        word_frequency = pd.DataFrame(cnt, columns=['Top Keywords', 'Frequency'])

        # Plotting and converting to json
        wordfreq = px.histogram(word_frequency,x="Top Keywords",y="Frequency",color_discrete_sequence=px.colors.qualitative.Pastel)
        keyword_plot_json = json.dumps(wordfreq, cls=plotly.utils.PlotlyJSONEncoder)
        wordfreq.update_yaxes(automargin=True)

        return keyword_plot_json

    # Visualization for the length of tweets vs the tweet type
    def tweetLengthGraph(self):
        # Converting the figure into JSON format which would then be displayed on the site
        lengthvstweettype = px.histogram(self.df,x="tweet_type",y="tweet_length",color_discrete_sequence=px.colors.qualitative.Safe)
        length_json = json.dumps(lengthvstweettype, cls=plotly.utils.PlotlyJSONEncoder)
        return length_json

    # Sentiment visualization for the sentiments found in the tweets
    def sentimentGraph(self):
        
        try:
            # Going with a detailed version if some variations of tweet types were found
            fig = px.scatter(self.df, y="positivity",x="tweet_length",color="tweet_type",size="social_count",size_max=60)
        except:
            # Going with a less detailed version if tweet type is of a single category only
            fig = px.scatter(self.df,y="positivity",x="tweet_length",size="social_count",size_max=60)
        sentiment_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return sentiment_json

    # A histogram for tweet length
    def tweetLengthHist(self):
        # Converting the figure into JSON format which would then be displayed on the site
        fig = px.histogram(self.df, x="tweet_length")
        hist_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return hist_json

    # Donut chart used to visualize emotional traits
    def drawDonutCharts(self, df):
        # Drawing a pie chart with hole param to make it look like a donut
        fig = px.pie(df, names='emotional_traits', title='Emotional traits',hole=.6)
        e_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        # Returning the JSON object to be rendered on to the site
        return e_json

    # Visualizing top reviews found
    def drawTopLocationChart(self):
        # Converting the figure into JSON format which would then be displayed on the site
        fig = px.bar(self.df,x='Location',color_discrete_sequence=px.colors.qualitative.Pastel)
        loc_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return loc_json

    # Visualizing the ratings found
    def drawRatingChart(self):
        # Converting the figure into JSON format which would then be displayed on the site
        fig = px.histogram(self.df,x='Rating')
        rate_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return rate_json

    # Visualization of Behavorial and emotional traits in reviews
    def drawBehavorialEmotionalChart(self, df):
        # Getting the emotional traits and big 5 traits from the function
        emotional_traits, big5_traits = getUserTraits(df)

        # Drawing a Pie Chart for getting the big 5 traits
        big5_traits_graph = px.pie(big5_traits, names='final_traits', title='',hole=.6)
        
        # Bar Plot for getting the big 5 traits along with a measure of how prevalent each trait is
        big5_traits_val_graph = px.bar(big5_traits, x='big_5_traits', color= 'big_5_trait_rate',color_discrete_sequence=px.colors.qualitative.Pastel)
        
        # Converting the graphs to JSON format to be rendered on to the site
        f_graph_json = json.dumps(big5_traits_graph, cls=plotly.utils.PlotlyJSONEncoder)
        big5_graph_json = json.dumps(big5_traits_val_graph, cls=plotly.utils.PlotlyJSONEncoder)

        # Drawing the figure for emotional traits
        fig = px.pie(emotional_traits, names='emotional_traits',hole=.6)

        # Converting to JSON 
        e_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Returning the graphs
        return (e_json,f_graph_json,big5_graph_json)

    # Behavorial traits found in the tweets
    def drawBig5TraitCharts(self, df):
        # Drawing the pie charts
        big5_traits_val_graph = px.pie(df, names='final_traits', title='',hole=.6)
        big5_traits_graph = px.bar(df, x='big_5_traits', color= 'big_5_trait_rate',color_discrete_sequence=px.colors.qualitative.Pastel)
        
        # Converting to JSON
        f_graph_json = json.dumps(big5_traits_val_graph, cls=plotly.utils.PlotlyJSONEncoder)
        big5_graph_json = json.dumps(big5_traits_graph, cls=plotly.utils.PlotlyJSONEncoder)

        # Returning the graphs
        return (f_graph_json,big5_graph_json)

    

    






    



