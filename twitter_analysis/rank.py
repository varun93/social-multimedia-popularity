from flask import Flask,url_for
from flask import render_template
from flask import request
from cluster import *
from Tweet import *
import pickle
import oauth2 as oauth
from TimeUtil import *
from Utils import *
from config import *
import json


app = Flask(__name__)

@app.route('/rank')
def RankClusters():

	tweets_entities = Utils.getObject(TWEETS_FILE)
	clusters_dict = Utils.getObject(CLUSTERS_FILE)
	

	print len(tweets_entities)
	print len(clusters_dict)

	count = 0

	for cluster_id,cluster in clusters_dict.iteritems():


		tweet_ids = cluster.getTweetIDs()

		# print tweet_ids
		total_change=0
		for tweet_id in tweet_ids:
			# print tweet_id
			tweet = tweets_entities[tweet_id]
			# print tweet
			# print tweet.as
			stats = "https://api.twitter.com/1.1/statuses/show.json?id=%s&trim_user=true"%(tweet_id)

			response, data = Utils.getOauthClient().request(stats)

			tweets = json.loads(data)
			previous_retweet_count = tweet.getRetweetCount()
			try:
				new_retweet_count =  tweets['retweet_count']
			except Exception, e:
				new_retweet_count = previous_retweet_count
			
			
			last_updated = tweet.getLastUpdated()
	        current_time = TimeUtil.getCurrentTime()
	        last_updated = last_updated.strftime("%Y-%m-%d %H:%M:%S")
	        time_difference = TimeUtil.getTimeDifference(last_updated,current_time)
	        rate_change = (new_retweet_count - previous_retweet_count)/float(time_difference)
	        tweet.setRetweetCount(new_retweet_count)
	        tweet.setLastUpdated(last_updated)
	        tweet.setRateChange(rate_change)
	        total_change+=rate_change


		print total_change
		cluster.setTotalRateChange(total_change)
		
	
	
	clusters = sorted(clusters_dict.values(), key=lambda x : x.total_rate_change,reverse=True)
	
	
	#how to send data 
	data_sent = {}
	clusters = clusters[:8]
	for cluster in clusters:
		hash_tags = cluster.hashtags_list
		tweet_ids = cluster.getTweetIDs()
		tweets = [tweets_entities[tweet_id] for tweet_id in tweet_ids]
		tweets = sorted(tweets, key=lambda x : x.rate_change,reverse=True)
		tweets = (tweets[:3],cluster.getRepresentativeWords())
		data_sent[int(cluster.getClusterId())] = tweets

	print data_sent
		
	pickle.dump(data_sent,open('new_exp_data_final.txt','w'))

    return render_template('test_template.html',data_sent = data_sent)


# @app.route('/')
# def hello_world():
	
# 	data_sent = {}
# 	data_sent = pickle.load(open('new_exp_data.txt','r'))
# 	return render_template('test_template1.html', data=data_sent)

 if __name__ == '__main__':
 	app.run()










