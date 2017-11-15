import requests
import json
from bs4 import BeautifulSoup
import urllib2 
import random
import datetime
import eventlet
import os
from db import *

API_KEY = "PLACE YOUR API KEY HERE"
views = {}


def updateImageStatistics():

	length = 0
	path = os.getcwd()
	folders = os.listdir(path)
	folders = [folder for folder in folders if folder.endswith("ing") or folder.endswith("mal")] 
	files = [{folder:file} for folder in folders for file in os.listdir(path+"/"+folder)]

	for item in files:
		for folder,file in item.iteritems():
			text = open(path + "/" + folder + "/" + file).read()
			try:
				persistImageStatistics(json.loads(text))
			except:
				print "folder =" +folder + "file =" + file


def generatetags(image_url):
	files = {}
	params = {'nearest': True, 'imageurl': image_url, 'timestamp':1408230573799}
	request = requests.post('http://clarifai.com/demo/upload/', files=files, data=params)
	output = request.json()
	return " ".join(json.dumps(output['files'][0]['predicted_classes']))



# Obtain Flickr Views
def findViews(user_id,photo_id):

	url = 'https://www.flickr.com/photos/%s/%s/'%(user_id,photo_id)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	for element in soup.find_all('span'):
		if(element.text.find('Views') >= 0):
        		views[photo_id] = str(element.text).lstrip().rstrip().split(' ')[0]

    return views

 

# ======================================= SAVE IMAGE ========================= 
def saveimage(image_url,filename):
	image = requests.get(image_url)
	file = open(filename,'wb')
	file.write(image.content)
	file.close()

	   

def imageurlbuilder(farm_id,server_id,id,secret):
	url = "https://farm%s.staticflickr.com/%s/%s_%s_s.jpg"%(farm_id,server_id,id,secret)
	return url


def photosearch(upload_date):
	url = "https://www.flickr.com/services/rest?method=flickr.photos.search&api_key=%s&min_upload_date=%s&max_upload_date=%s&per_page=%s&page=%s&extras=description,views,machine_tags,date_upload,date_taken&format=json&nojsoncallback=1"%(API_KEY,upload_date,upload_date,300,1)
	data = requests.get(url).json()

	with open('n' + str(upload_date)+'.json', 'a') as fp:
    		json.dump(data, fp)
    		
    	
def interestingPhotos(date):
	url = "https://www.flickr.com/services/rest?method=flickr.interestingness.getList&api_key=%s&date=%s&per_page=300&page=1&extras=description,views,machine_tags,date_upload,date_taken&format=json&nojsoncallback=1"%(API_KEY,date)
	data = requests.get(url).json()

	with open('i' + str(date) +'.json', 'a') as fp:
   			json.dump(data, fp)
		


# save the data in JSON 
def buildImageDataset():

	dates = []
	months = [31,29,31,30,31,30,31,31,30,31,30,31]

	for i,month in enumerate(months):
		
		days = random.sample(range(1, month), 21)
		
		for day in days:
			dates.append(datetime.date(2012,i+1,day)) 
			pool = eventlet.GreenPool(100)
			
		for date in pool.imap(interestingPhotos, dates):
			interestingdata = interestingPhotos(str(date),10,1)
			with open('i' + str(date) +'.json', 'wb') as fp:
				json.dump(interestingdata, fp)
		
		for date in pool.imap(photosearch, dates):
			data = photosearch(str(date),str(date),10,1)
			with open('n' + str(date)+'.json', 'wb') as fp:
				json.dump(data, fp)
		

