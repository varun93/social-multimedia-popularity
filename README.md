
## Twitter News Ranking 

An application to cluster and rank twitter news sources.

Twitter news feeds are dynamically clustered and the news are ranked on basis of trendiness and the news sources within the cluster ranked too.


## Requirements

The application requires that you install following python modules.
* requests
* oauth library
* Tweeps
* nltk


##API KEYS REQUIRED

1. TWITTER 
2. ALCHEMY
3. TAGME



## Getting Started with the code

In order to register the application with ALCHEMY_API:
	python alchemyapi.py YOUR_API_KEY
	python example.py

In order to start getting the live news feeds from the subscribed channels
	python news-stream.py  

Note:Replace Twitter API_KEY with your Twitter API key in the file config.py file
	Replace tagme API_KEY with your key in the file feature_extract.py
	

In order to do cluster maintenance for deletion and for merging.
	python cluster-maintenance.py


In order to do ranking and get the web application up and running.
	python ranking.py
	


