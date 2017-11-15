import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import oauth2 as oauth
from config import *


class AuthUtils:
    


   
                                                                                                                
    @staticmethod
    def getOauthClient():

        consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        access_token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_TOKEN_SECRET)
        client = oauth.Client(consumer, access_token)
        return client

    @staticmethod
    def getStreamOauth():
          auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
          auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
          return auth
