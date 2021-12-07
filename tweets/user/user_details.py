import tweepy
import os
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_key = os.environ['ACCESS_KEY']
access_secret = os.environ['ACCESS_SECRET']

def getUserDetails(username):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_key, access_secret)

    # Calling api
    api = tweepy.API(auth)
    user = api.get_user(screen_name=username)
    return(user.screen_name,user.profile_image_url_https,user.followers_count,user.friends_count)
