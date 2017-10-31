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

CONSUMER_KEY = "2WT1TSU4IlVNUgX9hUB2hkEwp"
CONSUMER_SECRET  = "Bfh9WFZA4jUlGZj3DqgzhD8ecJ7zL78PDUYKQcM45WQofPoGUM"
OAUTH_TOKEN = "767206872-duSzf95K69mSe0QvKXZRJtx0M9clovjeh23vrJPp"
OAUTH_TOKEN_SECRET = "oGd3eGFaDXIgSJmpGUShahTDpDVXGEeklcn8utocmstUi"
