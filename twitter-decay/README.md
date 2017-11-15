# Lifetime of a Tweet

The project was undertaken to analyze the number of retweets as a function of time and study the decay behaviour of tweets.

## Twitter News Ranking

Twitter news feeds are dynamically clustered and the news are ranked on basis of trendiness and the news sources within the cluster ranked too.

## Requirements

The application requires that you install following python modules.
* requests
* oauth library
* Tweeps
* nltk

## API KEYS REQUIRED

1.TWITTER 

## Getting Started with the code

In order to start getting the live news feeds from the subscribed channels
python news-stream.py  

The above script used Twitter Streaming API to continuosly collect the tweets published in real time.

Note : Replace Twitter API_KEY with your Twitter API key in the file config.py file
	 
A scheduler is used to periodically update the retweet count by querying the API

In order to update the retweet count 
python tweet_decay.py
	


