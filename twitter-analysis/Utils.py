import oauth2 as oauth
from tweepy import OAuthHandler
import pickle
import os
import requests
from config import *

class Utils:
    


    # CONSUMER_KEY = "2WT1TSU4IlVNUgX9hUB2hkEwp"
    # CONSUMER_SECRET  = "Bfh9WFZA4jUlGZj3DqgzhD8ecJ7zL78PDUYKQcM45WQofPoGUM"
    # OAUTH_TOKEN = "767206872-duSzf95K69mSe0QvKXZRJtx0M9clovjeh23vrJPp"
    # OAUTH_TOKEN_SECRET = "oGd3eGFaDXIgSJmpGUShahTDpDVXGEeklcn8utocmstUi"

    @staticmethod
    def saveimage(image_url,filename):
        image = requests.get(image_url)
        file = open(filename,'wb')
        file.write(image.content)
        file.close()
    
                                                                                                                
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

    @staticmethod
    def persist(filename,object):
        file_handle = open(filename,'w')
        pickle.dump(object,file_handle)

    @staticmethod
    def isFileEmpty(filename):
        return os.stat(filename).st_size == 0

    @staticmethod
    def getObject(filename):

        if Utils.isFileEmpty(filename):
            return dict()
            
        try:
            return pickle.load(open(filename,'r'))
        except Exception, e:
            raise
       