import MySQLdb
from sklearn import cluster,datasets
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pylab as pl
import pickle
from operator import itemgetter

def getViews():
  views = []
  cursor = db.cursor()
  sql = "SELECT * FROM PHOTO_INFO"
  cursor.execute(sql)
  results = cursor.fetchall()
  for result in results:
    views.append(result[4])
    
  return views



# ============================================= DB related functions =============================

def updateTags(id,tags):
  cursor = db.cursor()
  sql = "UPDATE PHOTO_INFO SET tags='%s' WHERE PHOTO_ID='%d' AND is_crawled=0"%(tags,id) 

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


# insert the photos in the database
def persistImageStatistics(stats):
  
  cursor = db.cursor()
  
    for item in stats['photos']['photo']:
    photo_id = int(item['id'])
    farm = int(item['farm'])
    views = int(item['views'])
    server_id = int(item['server'])
    secret = str(item['secret'])
    owner = str(item['owner'])
    date_taken = str(item['datetaken'])
    date_upload = str(item['dateupload'])
    sql = "INSERT INTO PHOTO_INFO(PHOTO_ID,FARM,VIEWS,SERVER_ID,SECRET,OWNER,date_taken,upload_date) VALUES('%d','%d','%d','%d','%s','%s','%s','%s')"%(photo_id,farm,views,server_id,secret,owner,date_taken,date_upload)
    
    try:
        cursor.execute(sql)
        db.commit()
      except:
      print 'screwed up'


  
# ==================================== NEEDED IN GATHER PHOTS=================
def updateCrawled(id):
  cursor = db.cursor()
  sql = "UPDATE PHOTO_INFO SET is_crawled=1 WHERE PHOTO_ID='%d'"%(id) 

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


# ==================== GATHER PHOTOS =======================

def gatherPhotos():
  urls = []
  path = os.getcwd()
  path = path + "/" + "Photos"
  cursor = db.cursor()
  sql = "SELECT * FROM PHOTO_INFO WHERE is_crawled=0 LIMIT 3000"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    saveimage(imageurlbuilder(row[3],row[5],row[0],row[6]),(path + "/" +str(row[0])+".jpeg"))
    updateCrawled(int(row[0]))




db = MySQLdb.connect(host = "",user = "",passwd = "",db = "flickr_images")







