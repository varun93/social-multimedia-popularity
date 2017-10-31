from __future__ import unicode_literals
from ftfy import fix_text
import math
import nltk
from TimeUtil import *
from Utils import *
import oauth2 as oauth
import json
from Parse_Tweet import *
import requests
from nltk.tag.stanford import NERTagger
import tweepy
import pickle
import numpy as np
from alchemyapi import AlchemyAPI
from config import *
from similarity import *
#from apscheduler.schedulers.blocking import BlockingScheduler
#from apscheduler.schedulers.background import BackgroundScheduler
					


def sayHello():
	print 'Hello'

def sayBye():
	print 'Bye'


def deleteClusters():
	
	tweets_entities = Utils.getObject(TWEETS_FILE)
	clusters = Utils.getObject(CLUSTERS_FILE)
	hashtag_dict = Utils.getObject(HASHTAGS_FILE)
	
	for cluster in clusters.values():
		total_change = 0
		tweet_ids = cluster.getTweetIDs()
		for tweet_id in tweet_ids:
			
			tweet = tweets_entities[tweet_id]
			rate_change = tweet.getRateChange()
			total_change += rate_change
			
			
		cluster.setTotalRateChange(total_change)
	
	
	clusters_sorted= sorted(clusters.values(), key=lambda x : x.total_rate_change)
	num_delete_clusters = (len(clusters)*1)/3

	count = 0
	for cluster in clusters_sorted:
		cluster_id=cluster.getClusterId()
		cluster_created_time = cluster.created_time
		cluster_created_time = cluster_created_time.strftime("%Y-%m-%d %H:%M:%S")
		current_time = TimeUtil.getCurrentTime()
		time_difference =TimeUtil.getTimeDifference(cluster_created_time,current_time)
		if time_difference > 1:
			count+=1
			tweet_ids = cluster.getTweetIDs()
			for tweet_id in tweet_ids:
				del tweets_entities[tweet_id]

			hashtags = cluster.getHashTags()
			for hash_tag in hashtags:
				cluster_ids = hashtag_dict[hash_tag]
				cluster_ids.remove(cluster_id)
				if len(cluster_ids) == 0:
					del hashtag_dict[hash_tag]


			del clusters[cluster_id]




		if count == num_delete_clusters:
			break


	Utils.persist(CLUSTERS_FILE,clusters)    
	Utils.persist(TWEETS_FILE,tweets_entities)   
	Utils.persist(HASHTAGS_FILE,hashtag_dict) 

#===================================================================================================================

def getClusters_hav_neighb(clusters_dict):

    tot_neighbours=0;
    clusters_having_neighb=[]
    for cluster in clusters_dict.values():
        if cluster.getNeighbours():
            clusters_having_neighb.append(cluster.getClusterId())# keeping ids is efficient than keeping clusters
        tot_neighbours=tot_neighbours+len(cluster.getNeighbours())
    #print tot_neighbours
    return clusters_having_neighb



#================================================================================================================

def merge_clusters():


	tweets_entities = Utils.getObject(TWEETS_FILE)
	clusters_dict = Utils.getObject(CLUSTERS_FILE)
	hashtag_dict = Utils.getObject(HASHTAGS_FILE)

	merged=[]
	count_comp=0
	cluster_ids=getClusters_hav_neighb(clusters_dict)


	while 1:
	    i=0
	    #cluster_ids=clusters_dict.keys()
	    #print len(cluster_ids)
	    #dummy_cluster=clusters_dict.values()[0] #just to avoid tweets not having cluster_id
	    for cluster_id in cluster_ids:

	        i=i+1
	        compared=[]
	        best_neighb_sim=0
	        cluster=clusters_dict[cluster_id]
	        neighb_tweets=cluster.getNeighbours()
	        #print neighb_tweets

	        for tweet_id in neighb_tweets:
	            tweet_entity=tweets_entities[tweet_id]
	            neighb_cid=tweet_entity.getClusterId() 
	            if neighb_cid not in compared:  
	                compared.append(neighb_cid)
	                #if neighb_cid not in clusters_dict.keys():
	                    #break
	                try:
	                	neighb_cluster=clusters_dict[neighb_cid]
	                	neighb_sim=Similarity.jaccard(cluster.getRepresentativeWords(),neighb_cluster.getRepresentativeWords())
	                	if best_neighb_sim<neighb_sim:
		                    best_neighb_sim=neighb_sim
		                    best_neighb_cluster=neighb_cluster

	                except Exception,e:
	                	print str(e) 
	                	
	                #compute similarity between cluster and neighb_cluster

	        count_comp=count_comp+len(compared)
	        if best_neighb_sim>0.15:
	            cluster.add(best_neighb_cluster.getRepresentativeWords())

	            neighb_tweet_list = best_neighb_cluster.getTweetIDs()
	            cluster_tweet_list = cluster.getTweetIDs()
	           	
	            for tweet_id in neighb_tweet_list:

	            	tweet = tweets_entities[tweet_id]
	            	tweet_created_time = tweet.getCreatedTime()

	                tweet.setClusterId(cluster.getClusterId())
	                cluster.addData(tweet_id,tweet_created_time)
	                #and if tweet in neighbour cluster remove it from clusters neighbours list
	                if tweet_id in neighb_tweets:
	                    cluster.removeNeighbour(tweet_id)
	                    #neighb_tweets.remove(item[0]) #this step not required happens by default


	            n_c_neighb_tweets=best_neighb_cluster.getNeighbours()
	            #if any neighbour of neigbour cluster belongs to cluster remove it from neighbour list []
	            for tweet_id in cluster_tweet_list:
	                if tweet_id in n_c_neighb_tweets:
	                    n_c_neighb_tweets.remove(tweet_id)


	            new_neighb_tweets=np.union1d(neighb_tweets,n_c_neighb_tweets)

	            for tweet_id in new_neighb_tweets:
	                if tweet_id not in neighb_tweets:
	                    cluster.addNeighbour(tweet_id)

	            #if merged cluster is in cluster_ids list remove
	            if best_neighb_cluster.getClusterId() in cluster_ids:
	                cluster_ids.remove(best_neighb_cluster.getClusterId())

	            merged.append((cluster.getClusterId(),best_neighb_cluster.getClusterId(),best_neighb_sim))

	            #updating hashtags data
	            hashtags=best_neighb_cluster.getHashTags()

	            for hashtag in hashtags:
	                cids=hashtag_dict[hashtag]
	                cids.remove(best_neighb_cluster.getClusterId())
	                if cluster_id not in cids:
	                    hashtag_dict[hashtag].append(cluster_id)
	                    cluster.addHashTag(hashtag)

	            #remove best_neighb_cluster from clusters
	            del clusters_dict[best_neighb_cluster.getClusterId()]
	            break


	    if i==len(cluster_ids):
	        break          

    
	Utils.persist(CLUSTERS_FILE,clusters_dict)    
	Utils.persist(TWEETS_FILE,tweets_entities)   
	Utils.persist(HASHTAGS_FILE,hashtag_dict)

	# deleteClusters()


#===================================================================================



'''
merge_scheduler = BackgroundScheduler()
merge_scheduler.add_job(sayBye,'interval',seconds=60)


try:
    merge_scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass

try:
        
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    pass'''


#merge_clusters()
deleteClusters()


	