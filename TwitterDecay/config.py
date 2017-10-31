import requests
import MySQLdb
import logging
import json
import string
import re
from TimeUtils import *
from FileUtils import *

 

regex = re.compile('[%s]' % re.escape(string.punctuation))
logging.basicConfig()
db = MySQLdb.connect(host = "127.0.0.1",user = "root",passwd = "root",db = "Twitter_Statistics")

news_channels_list=["TimesNow","ndtv","ibnlive","IndiaToday"]

CONSUMER_KEY = ""
CONSUMER_SECRET  = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""
