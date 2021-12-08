# Necessary Imports
from flask import Flask, render_template, make_response, url_for, request,redirect,session
import pandas as pd
from tweets import *
from utils import *
import os
from flask_session import Session
import secrets
import json
import logging
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
# Initializing the flask app
app = Flask(__name__,static_url_path='/static', static_folder="templates/assets/")
app.config["SESSION_PERMANENT"] = False

# Adding a secret key randomly decided
app.secret_key = os.environ["APP_SECRET_KEY"]

# Initializing a session
sess = Session()

# Home route where the landing page is shown
@app.route('/',methods = ['POST', 'GET'])
def home():
    # POST method used to get the username entered by the user
    if request.method == 'POST':
        user = request.form['username']
        appstore_link = request.form['appstore']
        playstore_link = request.form['playstore']
        session['playstore'] = playstore_link
        session['appstore'] = appstore_link
        
        # Redirecting the user to the dashboard page
        return redirect(url_for('dashboard',username=user))
    return render_template('landing.html')
# Dashboard route
@app.route('/<username>/dashboard',methods=['GET','POST'])
def dashboard(username):
    #print(username)
    try:
        tweet_utils = TweetUtils()
        tweets_df = tweet_utils.get_tweets(username)
        context = getUserContext(user=username, tweets_df = tweets_df)
        return render_template('index.html',context=context)
    except Exception as e:
        # Debug statement
        logging.exception(e)
        return redirect(url_for('error', code = 'DASHBOARD_ERR'))

# Reports route where the reports are shown
@app.route('/<username>/reports')
def textAnalyze(username):
    tweet_utils = TweetUtils()
    tweets_df = tweet_utils.get_tweets(username)
    store_review_utils = StoreReviewUtils()
    store_review_utils.setUsername(username)

    try:
        try:
            if(session["appstore"]==""):
                app_reviews_df = store_review_utils.searchAppStore()
            else:
                app_reviews_df = store_review_utils.searchAppStore(link = session["appstore"])

        except:
            logging.warning("App Not found")

        try:
            if(session["playstore"]==""):
                app_reviews_df = store_review_utils.searchPlaystore()
            else:
                app_reviews_df = store_review_utils.searchPlaystore(link = session["playstore"])
        except:
            logging.warning("App Not found")

        # Generating the reports to be rendered using a util class
        gen = ReportGenerator(tweet_utils, store_review_utils, username)
        context = gen.generateReports()
        
        return render_template(
            'reports.html',
            twitter_len = len(context['twitter_positive_reviews']),
            playstore_len = len(context['playstore_positive_reviews']),
            appstore_len = len(context['appstore_positive_reviews']),
            appstore_negative_len = len(context['appstore_negative_reviews']),
            playstore_negative_len = len(context['playstore_negative_reviews']),
            twitter_negative_len = len(context['twitter_negative_reviews']),
            context = context
        )
    except Exception as e:
        # Debug statement
        logging.exception(e)
        return redirect(url_for('error', code = "REPORT_ERR"))

# Error page
@app.route('/<code>/error')
def error(code):
    if(code == "DASHBOARD_ERR" or code == "TWITTER_ERR"):
        message = "Please check the twitter username provided."

    elif(code == "APPSTORE_ERR" or code == "PLAYSTORE_ERR"):
        message = "The app link provided might not be valid or we weren't able to find your app"
    
    elif(code == "REPORT_ERR"):
        message = "The reports section is not accessible if all the links are not provided. Please try with something else."
    elif(code == "UB_ERROR"):
        message = "We weren't able to find your app on trustpilot"

    context = {
        "message" : message
    }
    return render_template('error.html', context = context)

# Route for showing the detailed analysis of the brand on twitter
@app.route('/<username>/analyze/twitter')
def charts(username):
    # Getting the tweets collected
    try:
        tweets_df = None
        tweet_utils = TweetUtils()
        tweets_df = tweet_utils.get_tweets(username)
        # Initializing a renderer for collecting graphs:
        renderer = GraphRenderer(tweets_df)
        # Collecting the graphs in JSON format to be shown on the site
        e_df = getEmotionalTraits(tweets_df)
        keyword_graph = renderer.drawTopKeywords()
        screen_name,image_url,followers,friends = getUserDetails(username)
        b_df = getBehavorialTraits(tweets_df)
        f_graph_json,big5_graph_json = renderer.drawBig5TraitCharts(b_df)
        length_graph = renderer.tweetLengthGraph()
        sentiment_graph = renderer.sentimentGraph()
        emot_graph = renderer.drawDonutCharts(e_df)
        
        # Creating context to access these values in our html file
        context = {
            "keyword_graph":keyword_graph,
            "length_graph" :length_graph,
            "sentiment_graph":sentiment_graph,
            "e_graph" : emot_graph,
            "user" : username,
            "screen_name" : screen_name,
            "image_url" : image_url,
            "f_graph_json" : f_graph_json,
            "big5_graph_json" : big5_graph_json, 
        }
        return render_template('chart.html',context=context)
    except Exception as e:
        # Debug statement
        logging.exception(e)
        return redirect(url_for('error', code = "TWITTER_ERR"))

# Route for showing detailed analysis of app on playstore
@app.route('/<username>/analyze/playstore')
def playstoreAnalysis(username):
    try:
        store_review_utils = StoreReviewUtils()
        store_review_utils.setUsername(username)
        if(session["playstore"]==""):
            app_reviews_df = store_review_utils.searchPlaystore()
        else:
            app_reviews_df = store_review_utils.searchPlaystore(link = session["playstore"])

        # Collecting the graphs
        context = store_review_utils.renderPlaystoreGraphs()
        context['user'] = username
        screen_name,image_url,followers,friends = getUserDetails(username)
        context['screen_name'] = screen_name
        context['image_url'] = image_url
        context['followers'] = followers
        context['friends'] = friends
        return render_template('playstore-analytics.html', context = context)
    except Exception as e:
        # Debug statement
        logging.exception("e")
        return redirect(url_for('error', code = "PLAYSTORE_ERR"))

# Route for showing detailed analysis of app on appstore
@app.route('/<username>/analyze/appstore')
def appStoreAnalysis(username):
    try:
        store_review_utils = StoreReviewUtils()
        store_review_utils.setUsername(username)
        if(session["appstore"]==""):
            app_reviews_df = store_review_utils.searchAppStore()
        else:
            app_reviews_df = store_review_utils.searchAppStore(link = session["appstore"])
 
        # Collecting the graphs
        context = store_review_utils.renderAppStoreGraphs()
        context['user'] = username
        screen_name,image_url,followers,friends = getUserDetails(username)
        context['screen_name'] = screen_name
        context['image_url'] = image_url
        context['followers'] = followers
        context['friends'] = friends
        return render_template('app-store-analytics.html', context = context)
    except Exception as e:
        # Debug statement
        logging.exception("e")
        return redirect(url_for('error', code = "APPSTORE_ERR"))

# Route for showing the detailed analysis of user-reviews
@app.route('/<username>/user-base-analysis')
def userBaseAnalysis(username):
    try:
        # Searching for the company on trustpilot(user-review site) with the username
        review_utils = ReviewUtils(username = username, n_pages = 2)
        review_utils.getReviewEndPoint()
        review_utils.scrape_reviews()
        
        # Getting the data back as Pandas dataframe
        user_reviews_df, scrape_success = review_utils.user_reviews_df, review_utils.scrape_success
        
        # Redirecting user to error page if the site was not found on trustpilot
        if(scrape_success == 0):
            return(redirect(url_for('error')))
        
        # Initialize graph renderer
        renderer = GraphRenderer(user_reviews_df)
        # Collecting the graphs in JSON format
        loc_json = renderer.drawTopLocationChart()
        rate_json = renderer.drawRatingChart()
        review_json,f_graph_json,big5_graph_json = renderer.drawBehavorialEmotionalChart(user_reviews_df)
        screen_name,image_url,followers,friends = getUserDetails(username)
        
        # Creating the context to be used in our html file
        context = {
            "image_url" : image_url,
            "screen_name" : screen_name,
            "user" : username,
            "loc_json" : loc_json,
            "rate_json" : rate_json,
            "review_json" : review_json,
            "f_graph_json" : f_graph_json,
            "big5_graph_json" : big5_graph_json
        }
        return render_template('user-analysis.html',context=context, code = "UB_ERROR")
    except Exception as e:
        # Debug statement
        logging.exception(e)
        return redirect(url_for('error'))

@app.route('/<username>/custom',methods = ['POST', 'GET'])
def customDataAnalysis(username):
    screen_name,image_url,followers,friends = getUserDetails(username)
    if request.method == 'POST':
        req_file = request.files['file'].read()
        try:
            reviews_df = pd.read_csv(BytesIO(req_file))
            custom_data_utils = CustomReviewUtils(reviews_df)
            context = custom_data_utils.renderCustomReviewGraphs()
            context['user'] = username
            context['screen_name'] = screen_name
            context['image_url'] = image_url
            context['followers'] = followers
            context['friends'] = friends
            return render_template(
                'custom-reviews.html',
                context = context,
                p_reviews_len = len(context['positive_reviews']),
                n_reviews_len = len(context['negative_reviews']),

            )
        except Exception as e:
            logging.exception(e)
    else:
        context = {
            "image_url" : image_url,
            "screen_name" : screen_name,
            "user" : username,
        }
        return render_template('custom.html', context = context)

# Starting the app
if __name__ == '__main__':
   app.run(debug=True)
