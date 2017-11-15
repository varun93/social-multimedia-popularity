import requests
import json
import eventlet
import MySQLdb
import re
import numpy as np
import pickle

DEVELOPER_KEY = "DEVELOPER_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


feature_vectors = []
imdb_ratings = []
likes_feautures = []


def updateSatistics(video_id,stats):
  cursor = db.cursor()
  sql = "UPDATE youtubeIMDB SET likes_count='%d',views_count='%d',dislikes_count='%d',favourite_count='%d',comment_count='%d',stats_updated=1 WHERE video_id='%s'"%(int(stats["likeCount"]),int(stats["viewCount"]),int(stats["dislikeCount"]),int(stats["favoriteCount"]),int(stats["commentCount"]),video_id) 

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


def insert_video(video,titleN,rating,rt_critic,rt_people,movie_id):
  cursor = db.cursor()
  video_id = str(video["id"]["videoId"])
  sql = "INSERT INTO youtubeIMDB(video_id,imdb_id,title,ratings,rt_critic,rt_people) VALUES('%s','%d','%s','%s','%s','%s')"%(video_id,movie_id,titleN,rating,rt_critic,rt_people)
  try: 
    cursor.execute(sql)
    db.commit()
  except:
    print titleN
      

def getStatistics(video_id):
  url = "https://www.googleapis.com/youtube/v3/videos?id=%s&key=%s&fields=items(statistics)&part=statistics"%(video_id,DEVELOPER_KEY)
  data = requests.get(url).json()
  updateSatistics(video_id,data["items"][0]["statistics"])


def getTitles():
  queries = []
  cursor = db.cursor()
  sql = "SELECT * FROM movies"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    queries.append(row[7])

  return queries


def normalizeLikes(likes):
  likes = []
  feature_vectors = []
  cursor = db.cursor()
  sql = "SELECT * FROM youtubeIMDB"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
     vector = []
     l = (row[4] - likes[0])/float(likes[1])
     vector.append(l)
     feature_vectors.append(np.array(vector))

    
  file = open('likes.txt','wb')
  pickle.dump(feature_vectors,file)
  file.close()
 

def normalizeViews(views):
  likes = []
  feature_vectors = []
  cursor = db.cursor()
  sql = "SELECT * FROM youtubeIMDB"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
     vector = []
     l = (row[5] - views[0])/float(views[1])
     vector.append(l)
     feature_vectors.append(np.array(vector))

  
  file = open('views.txt','wb')
  pickle.dump(feature_vectors,file)
  file.close()


def populateYoutubeIMDB():
  ids = []
  cursor = db.cursor()
  sql = "SELECT * FROM moviesIMDB where is_updated=0"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    movie_id = row[0]
    title = row[2]
    rating = row[3]
    year = row[4]
    rt_critic = row[7]
    rt_people = row[8]
    query = title + " " + str(year) + " " + "official trailer"  
    url = "https://www.googleapis.com/youtube/v3/search?key=%s&part=snippet&q=%s&maxResults=1&type=video"%(DEVELOPER_KEY,query)
    data = requests.get(url).json()
    video = data["items"][0]
    insert_video(video,title,rating,rt_critic,rt_people,movie_id)

def normalize(likes,views,dislikes,comments):
  cursor = db.cursor()
  sql = "SELECT * FROM youtubeIMDB"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    vector = []
    l = (row[4] - likes[0])/float(likes[1])
    v = (row[5] - views[0])/float(views[1])
    d = (row[6] - dislikes[0])/float(dislikes[1])
    c = (row[8] - comments[0])/float(comments[1])
    vector.append(l)
    vector.append(v)
    vector.append(d)
    vector.append(c)
    imdb_ratings.append(float(row[2]))
    feature_vectors.append(np.array(vector))


  file = open('feature_vectors.txt','wb')
  pickle.dump(feature_vectors,file)
  file.close()

  file = open('imdb_ratings.txt','wb')
  pickle.dump(imdb_ratings,file)
  file.close()
  

def normalizeData():
  cursor = db.cursor()
  views_count = []
  comment_count = []
  likes_count = []
  dislikes_count = []
  views = ()
  likes = ()
  dislikes = ()
  comments = ()
  sql = "SELECT * FROM youtubeIMDB"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    likes_count.append(row[4])
    views_count.append(row[5])
    dislikes_count.append(row[6])
    comment_count.append(row[8])

  likes_pcount = np.array(likes_count)
  views_pcount = np.array(views_count)
  dislikes_pcount = np.array(dislikes_count)
  comment_pcount = np.array(comment_count)

  likes = likes_pcount.mean(),likes_pcount.std()
  views = views_pcount.mean(),views_pcount.std()
  dislikes = dislikes_pcount.mean(),dislikes_pcount.std()
  comments = comment_pcount.mean(),comment_pcount.std()

  # normalize(likes,views,dislikes,comments)
  normalizeViews(likes)
  # normalizeViews(views)

    

def populateMovies(query):
  url = "https://www.googleapis.com/youtube/v3/search?key=%s&part=snippet&q=%s&maxResults=1&type=video"%(DEVELOPER_KEY,query)
  data = requests.get(url).json()
  for video in data["items"]:
    insert_video(video,query)



db = MySQLdb.connect(host = "localhost",user = "root",passwd = "",db = "test")

normalizeData()


