from __future__ import unicode_literals
from cluster import *
import numpy as np
import math
import nltk
from TimeUtil import *
from Utils import *
import json
from Parse_Tweet import *
from Tweet import *
from feature_extract import *
from similarity import *
from ftfy import fix_text
import requests
from nltk.tag.stanford import NERTagger
import tweepy
import pickle
from alchemyapi import AlchemyAPI
from nltk.stem.porter import *
from datetime import datetime, timedelta
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import string
from config import *




filter=["TimesNow","HeadlinesToday","ndtv","ibnlive","IndiaToday","tweet","Twitter","news","news flash",
                "breaking","PTI","pti","http",'#','NEWSROOM','india today','ndtv 24x7','times now',':','?','india'
                'newsroom',';','tweet','India Today','click','GMT','IST','twitter','the','The','Press Trust of India'
                ,'IndiaAt9','India']

hashtag_filter=["Latest","NEWSROOM","newsroom"]

news_channels_list=["TimesNow","ndtv","ibnlive","IndiaToday"]


def update_hashtag_table(hashtag_list,best_cid,hashtag_dict,clusters_dict):
    
    for hashtag in hashtag_list:
        hashtag_dict.setdefault(hashtag,[])
        if hashtag in hashtag_dict.keys():
            cluster_ids = hashtag_dict[hashtag]
            if best_cid not in cluster_ids:
                hashtag_dict[hashtag].append(best_cid)
                clusters_dict[best_cid].addHashTag(hashtag)
        else:
            hashtag_dict[hashtag].append(best_cid)
            clusters_dict[best_cid].addHashTag(hashtag)



#====================================================================================================================

def clusterTweets(tweet_entity,tweet_entities):

    clusters_dict = Utils.getObject(CLUSTERS_FILE)
    hashtag_dict = Utils.getObject(HASHTAGS_FILE)

        

    best_jaccard = 0
    jaccard_score= 0
    best_hash_sim=0
    best_cluster_flag=0

    tweet_feature =tweet_entity.getTweetFeature()
    
    if tweet_feature:
        tweet_feature = [word for word in tweet_feature if word not in filter]
        #remove unigrams in bigrams
        tweet_feature=Similarity.remove_dup(tweet_feature)
        
        
        hashtag_list = tweet_entity.getHashTags()
        
        hashtag_list = [hashtag for hashtag in hashtag_list if hashtag not in hashtag_filter]
        
                                                                                                    
        if hashtag_list:
            for hashtag in hashtag_list:
               
                if hashtag in hashtag_dict.keys():
                                    
                    cluster_list = hashtag_dict[hashtag]
               
                    for cid in cluster_list:
                        cluster = clusters_dict[cid]
                        sim=Similarity.jaccard(tweet_feature,cluster.getRepresentativeWords())
                        if sim>=best_hash_sim:
                            best_hash_sim=sim
                            best_hash_cluster=cluster
                            best_cluster_flag=1
                            
            if best_cluster_flag:
                best_hash_cluster.add(tweet_feature);
                best_hash_cluster.addData(tweet_entity.getTweetId(),tweet_entity.getCreatedTime());
                best_cid=best_hash_cluster.getClusterId()
                tweet_entity.setClusterId(best_cid)
                #update hashtag table
                update_hashtag_table(hashtag_list,best_cid,hashtag_dict,clusters_dict)
                return
        

        for cluster in clusters_dict.values():
            representative_words = cluster.getRepresentativeWords()
            jaccard_score = Similarity.jaccard(representative_words,tweet_feature)


            
            
            if jaccard_score>0.10:
                cluster.addNeighbour(tweet_entity.getTweetId())


            if (best_jaccard < jaccard_score):
                best_jaccard = jaccard_score;
                best_cluster=cluster;

        
                #choose appropriate threshold

        if(best_jaccard >=0.20):
            best_cluster.add(tweet_feature);
          
            best_cluster.addData(tweet_entity.getTweetId(),TimeUtil.getTimestamp(tweet_entity.getCreatedTime()))
            best_cluster.removeNeighbour(tweet_entity.getTweetId())
          
            tweet_entity.setClusterId(best_cluster.getClusterId())
            #update hashtag table
          
            update_hashtag_table(hashtag_list,best_cluster.getClusterId(),hashtag_dict,clusters_dict) 


        else:
            if tweet_feature is not None or len(clusters) == 0: #wat is the use of this
                new_cid=tweet_entity.getTweetId()
                cluster = Cluster(new_cid,tweet_entity.getCreatedTime())
                cluster.add(tweet_feature)
                cluster.addData(tweet_entity.getTweetId(),TimeUtil.getTimestamp(tweet_entity.getCreatedTime()))
                clusters_dict[new_cid]=cluster
                #update hashtag table
                update_hashtag_table(hashtag_list,new_cid,hashtag_dict,clusters_dict)

   

    Utils.persist(CLUSTERS_FILE,clusters_dict)    
    Utils.persist(HASHTAGS_FILE,hashtag_dict)       
        
#========================================   =================================================================



class StdOutListener(StreamListener):

    def on_data(self, data):

       
        tweet_entities = Utils.getObject(TWEETS_FILE)
        
        try:

            tweet= json.loads(data)
            
            
            if tweet['user']['screen_name'] in news_channels_list:
            
                text = fix_text(tweet['text'])
                original_text = text
                created = tweet['created_at']
                channel = tweet['user']['screen_name']
                # channel = 'TimesNow'
                retweet_count = tweet['retweet_count']
                tweet_id = str(tweet['id_str'])
                

                current_time  = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created,'%a %b %d %H:%M:%S +0000 %Y'))
                current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S") 
                current_time += timedelta(hours=5,minutes=30)
                current_time = datetime.strptime(current_time.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
               


                hash_tags = ParseTweet.getHashtags(text)
                urls = ParseTweet.getURLs(text)
                user_mentions = ParseTweet.getUserHandles(text) 
                symbols = ParseTweet.getRT(text)
                text =  FeatureExtract.getTweetText(text,hash_tags,urls,user_mentions,symbols)
              
                print 'Plain Text ',text

                if text is not None:
                    text = ' '.join(text)

                print 'Here before if'
                list = FeatureExtract.getAlchemyEntities(text)
                # list = FeatureExtract.getDisamguatedTweet(text)
               
                if list is not None and len(list) > 0:

                    tweet_entity = Tweet(tweet_id,list,original_text,current_time,channel,hash_tags)

                    tweet_entity.setLastUpdated(current_time)
                    tweet_entity.setRetweetCount(retweet_count)

                    tweet_entities[tweet_id] = tweet_entity
                    

                    print  'Named entities :',  ' '.join(list)

                    clusterTweets(tweet_entity,tweet_entities)
                    Utils.persist(TWEETS_FILE,tweet_entities) 


                    
                  
                 
               
        except Exception, e:
            print e
            pass
        else:
            pass
        finally:
            pass

    def on_error(self, status):
        print status



if __name__ == '__main__':
    print 'started'


    l = StdOutListener()
    stream = Stream(Utils.getStreamOauth(), l)
    stream.filter(follow=['240649814','37034483','6509832','19897138'],track=[])

   


   



