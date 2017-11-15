import requests
import json
from bs4 import BeautifulSoup
import urllib2 
import random
import datetime
import eventlet
import MySQLdb
import os
import re
from textblob import TextBlob
import pickle
import math


# =============== DB related actions ===================
def getIds():
  ids = []
  cursor = db.cursor()
  sql = "SELECT * FROM youtube LIMIT 1"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    ids.append(row[0])

  return ids

# ============== insert comments =======================
def insertComments(commentS,video_id):
  cursor = db.cursor()
  cursor.executemany("INSERT INTO comments(video_id,comment) values (video_id,'%s')",commentS)
  db.commit()


def updateComments(video_id):
  cursor = db.cursor()
  sql = "UPDATE youtubeIMDB SET stats_updated=1 WHERE video_id='%s'"%(video_id) 

  try:
    try:
        cursor.execute(sql)
    except:
      db.rollback()
      raise
    else:
      db.commit()
  finally:
    cursor.close()


def updateTags(video_id,tags):
  cursor = db.cursor()
  sql = "UPDATE youtube SET tags=%s WHERE video_id=%d"%(tags,id) 
  try:
    try:
        cursor.execute(sql)
      except:
        db.rollback()
        raise
      else:
        db.commit()
    finally:
      cursor.close()


def getSetimentScore(text):
  comment = TextBlob(text)
  sentiment = comment.sentiment.polarity
  subjectivity = comment.sentiment.subjectivity
  return sentiment,subjectivity


def round(val):
  return int(math.floor(val)) if (val - math.floor(val)) else int(math.ceil(val))

def getAllComments(video_id):
  
  comments = []
  
  url = 'https://gdata.youtube.com/feeds/api/videos/%s/comments'%(video_id)
  data = requests.get(url).content 
  soup = BeautifulSoup(data)
  max_results = 100
  try:
    max_results = int(soup.find('opensearch:totalresults').text)
  except:
    max_results = 100
  indicies = [1 if i==0 else (i*25+1) for i in range(0,round(max_results/25.0))]
  for index in indicies:
    url = 'https://gdata.youtube.com/feeds/api/videos/%s/comments?start-index=%d&maxResults=25'%(video_id,index)
    data = requests.get(url).content 
    soup = BeautifulSoup(data)
    for comment in soup.find_all("content"):
      if comment is not None:
        try:
          print comment.text.encode('ascii','ignore')
          comments.append(comment.text.encode('ascii','ignore'))
        except:
          print 'unicode error'

  file = open(str(video_id) +'.txt', 'wb')
  pickle.dump(comments,file)
  updateComments(video_id)




def getSentimentScores():
  file = open('7q51vwapBXE.txt')
  soup = BeautifulSoup(file.read())
  comments = [comment.text.encode('ascii','ignore') for comment in soup.find_all("content")]
  sentiment_total = sum([TextBlob(comment).sentiment.polarity for comment in comments])
  print sentiment_total
  sentiments.append(sentiment_total)
  


db = MySQLdb.connect(host = "localhost", user = "root", passwd = "",db = "")

ids = getIds()
for id in ids:
  persistYoutubeComments(id)