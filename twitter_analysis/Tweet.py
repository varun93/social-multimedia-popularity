#original tweet consits of time_stamp
#hash_tag is missing 
#channel_name is missing
#tweet_features is named wrongly 	
#does the tweet entity 
#should rename the tweet to twitter features

class Tweet:

	def __init__(self,tweet_id=None,tweet_feature=None,tweet=None,created_time=None,channel=None,hash_tag=None):
		
		self.tweet_id = tweet_id
		self.created_time = created_time
		self.tweet_feature  = tweet_feature
		self.tweet = tweet
		self.channel = channel
		self.hash_tag = hash_tag
		self.rate_change = 0
		self.cluster_id = None
		self.last_updated = None
		self.retweet_count = 0
		
    

	def setClusterId(self,cluster_id):
		self.cluster_id = cluster_id

	def  getClusterId(self):
		return self.cluster_id
		
	def setLastUpdated(self,last_updated):
		self.last_updated = last_updated

	def getLastUpdated(self):
		return self.last_updated

	def getRetweetCount(self):
		return self.retweet_count

	def setRetweetCount(self,retweet_count):
		self.retweet_count = retweet_count

	def setRateChange(self,rate_change):
		self.rate_change = rate_change

	def getRateChange(self):
		return self.rate_change

	def getTweet(self):
		return self.tweet

	def getTweetFeature(self):
		return self.tweet_feature
	
	def getTweetId(self):
		return self.tweet_id

	def getChannel(self):
		return self.channel

	def getHashTags(self):
		return self.hash_tag
    
    
   	def getCreatedTime(self):
   		return self.created_time
  

