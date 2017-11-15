from __future__ import unicode_literals
import requests;
import nltk;
import numpy as np
import string
from config import *
from nltk.tag.stanford import NERTagger
from Parse_Tweet import *
from similarity import *
from alchemyapi import AlchemyAPI


#Possible features are named entities,word sense disambiguation,and stop word removal
class FeatureExtract:
    
    
    @staticmethod
    def getAlchemyEntities(tweet_text):

        alchemy_entities=[] 
        entities= alchemyapi.entities('text',tweet_text)

        for entity in entities['entities']:
            alchemy_entities.append(str(entity['text']).lower())

        return alchemy_entities

        


    @staticmethod
    def getDisamguatedTweet(tweet_text):
        try:
            url="http://tagme.di.unipi.it/spot?text=%s&key=XXXXXXXXXX"%(tweet_text);
            return filter(None,[str(element['spot']).lower() for element in requests.get(url).json()["spots"] if float(element['lp']) > 0.04]);
        except Exception,e:
            raise
        

    @staticmethod
    def getTweetText(tweet,hash_tags=None,urls=None,mentions=None,symbols=None):
        
        filter = hash_tags+urls+mentions+symbols;
        
        try:
            # print [word.encode('utf-8').translate(None, string.punctuation) for word in tweet.split() if word not in filter]
            return [word for word in tweet.split() if word not in filter]
        except Exception, e:
            raise
        


# print FeatureExtract.getAlchemyEntities('Congress pulling out all stops for farmers rally')