import requests
import json
import eventlet
import MySQLdb
import re

API_KEY = "place you api key here"
ROTTEN_TOMATO_API_KEY = "ROTTEN_TOMATO_API_KEY"
years = [2008]


def rottenTomatoesData(data,movie_id):
  rt_critic = str(data["movies"][0]["ratings"]["critics_score"])
  rt_people = str(data["movies"][0]["ratings"]["audience_score"])
  cursor = db.cursor()
  sql = "UPDATE moviesIMDB SET rt_critic=%s,rt_people=%s,is_updated=1 WHERE movie_id=%d"%(rt_critic,rt_people,movie_id) 

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



def update_rotten_tomatoes():

  cursor = db.cursor()
  sql = "SELECT * FROM moviesIMDB where is_updated=0"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    title = row[2]
    url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=%s&q=%s&page_limit=1"%(ROTTEN_TOMATO_API_KEY,title)
    try:
      data = requests.get(url).json()
      rottenTomatoesData(data,row[0])
    except:
      print 'something wrong'


def update_imdb_movie():
  cursor = db.cursor()
  sql = "SELECT * FROM moviesIMDB where is_updated=0"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    title = row[2]
    year = row[5].split("-")[0]
    url = "http://www.omdbapi.com/?t=%s&y=%s&plot=short&r=json"%(title,year)
    try:
      data = requests.get(url).json()
      dummy_update(data,row[0])
    except:
      print 'something wrong'




def insert_video(movie):
  cursor = db.cursor()
  imdb_id = int(movie["id"])
  title = movie["title"]
  popularity = str(movie["popularity"]) 
  release_date = str(movie["release_date"])
  rating = str(movie["vote_average"])
  vote_count =  int(movie["vote_count"])
  sql = "INSERT INTO movies(imdb_id,title,popularity,release_date,rating,vote_count) VALUES('%d','%s','%s','%s','%s','%d')"%(imdb_id,title,popularity,release_date,rating,vote_count)

  try:
  	cursor.execute(sql)
  	db.commit()
  except:
    print 'screwed up'

def insert_movies(ids):
  cursor = db.cursor()
  for id in ids:
    sql = "SELECT * FROM movies WHERE imdb_id=%d"%(id)
    cursor.execute(sql)
    results = cursor.fetchall()
    row = results[0]
    cursor1 = db.cursor()
    title = row[2]
    release_date = row[6]
    sql = "INSERT INTO moviesIMDB(title,release_date) VALUES('%s','%s')"%(title,release_date)
    try:
      cursor1.execute(sql)
      db.commit()
    except:
      print 'screwed up'



def prepareList():

  cursor = db.cursor()
  sql = "SELECT * FROM movies"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    title = row[2] + " " + row[6].split("-")[0] + " " + "official trailer" 
    movie_id = row[0]
    update_query(title,movie_id)

def getMovies(year,page):
	url = "https://api.themoviedb.org/3/discover/movie?api_key=%s&year=%d&adult=false&language=english&page=%d"%(API_KEY,year,page)
	data = requests.get(url).json()
	return data

db = MySQLdb.connect(host = "localhost",user = "root",passwd = "",db = "test")

update_rotten_tomatoes()




	