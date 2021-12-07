from tweets.user.user_stats import *
from tweets.user.user_details import *
from tweets.graphs.plot_graph import GraphRenderer
import pandas as pd

# Getting some common things like retweets and favorites etc to be shown on dashboard
def getUserContext(user, tweets_df):
    ## Initializing the renderer for our dashboard
    renderer = GraphRenderer(tweets_df)

    ## Getting the maximum and minimum values along with the indexes for the popularity of tweets
    max,min,max_index,min_index = getTweetPopularityStats(tweets_df)
    # Getting the retweet sum, screen_ame and image_url etc to be shown on the dashboard
    retweet_sum,screen_name,image_url,followers,friends,total_fav = getUserInfo(user = user,tweets_df = tweets_df)
    
    # Getting the maximum and average sentiment score found in the tweets
    avg_sentiment,max_sentiment_value = getSentimentStats(tweets_df)
    
    # Getting the no of tweets which have a certain tweet length type("LONG=SIZED", "MEDIUM-SIZED", "SHORT")
    maxlength_count,minlength_count,maxlengthtype_index,minlengthtype_index = getTweetLengthStats(tweets_df)
    
    # Getting the graphs in JSON format to be plotted
    plot_graph = renderer.drawTweetTypeGraph()
    hist_graph = renderer.tweetLengthHist()

    # Passing these values in the context which would then be used in the html files
    context = {
        "plot_graph" : plot_graph,
        "retweet_sum" : retweet_sum,
        "screen_name" : screen_name,
        "image_url" : image_url,
        "followers" : followers,
        "friends" : friends,
        "favorites" : total_fav,
        "user" : user,
        "max_index" : max_index,
        "min_index" : min_index,
        "max" : max,
        "min" : min,
        "maxlength_count" : maxlength_count,
        "minlength_count" : minlength_count,
        "maxlengthtype_index" : maxlengthtype_index,
        "minlengthtype_index" : minlengthtype_index,
        "avg_sentiment" : int(avg_sentiment),
        "max_sentiment_value" : max_sentiment_value,
        "hist_graph" : hist_graph

    }
    return (context)