from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from config import *
from DBUtils import *	
from AuthUtils import *



def updateTwitterStatistics(tweet_id):

	endpoint = "https://api.twitter.com/1.1/statuses/show.json?id=%d&trim_user=true"%(int(tweet_id))
	response, data = AuthUtils.getOauthClient().request(endpoint)
	tweets = json.loads(data)

	if tweets is not None:
		try:
			retweet_count =  tweets['retweet_count']
			print retweet_count
			DBUtils.insertStats(tweet_id,retweet_count)
		except KeyError:
			pass

# shchedule for tweet
def checkForPolling():

	last_update = FileUtils.getObject('last_update.txt')
	for tweet_id,last_updated in last_update.iteritems():
		current_time = TimeUtils.getCurrentTime()
		time_difference = TimeUtils.getTimeDifference(last_updated,current_time)
		
		if time_difference > 5:
			
			last_update[tweet_id] = TimeUtils.getCurrentTime()
			updateTwitterStatistics(tweet_id)
			FileUtils.persist('last_update.txt',last_update)
			


merge_scheduler = BackgroundScheduler()
merge_scheduler.add_job(checkForPolling,'interval',seconds=60)


try:	
    merge_scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass

try:
	while True:
		time.sleep(1)
except (KeyboardInterrupt, SystemExit):
	pass











