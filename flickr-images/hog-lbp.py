from skimage import io, color
from skimage.feature import hog
from skimage.feature import local_binary_pattern
import os
import pickle
import datetime
import numpy as np
from db import *


views = []
images = []
path = "PATH TO IMAGES"


#========================= Read Images and get views========================================
def read_image(path):
    list_img=os.listdir(path)
    cursor = db.cursor()
    for image in list_img:
        sql = "SELECT views FROM PHOTO_INFO WHERE photo_id=%s"%(image[:10])
        cursor.execute(sql)
        results = cursor.fetchall()
        if results[0][0]!=0:
            views.append(int(results[0][0]))
            im = io.imread(path+"/"+image)
            images.append(im)
    cursor.close()
    fp=open("image.txt",'w')
    pickle.dump(images,fp)
    fpv=open("views.txt",'w')
    pickle.dump(views,fpv)

    fp=open("imagenorm.txt",'w')
    pickle.dump(images,fp)
    fpv=open("viewsnorm.txt",'w')
    pickle.dump(views,fpv)
 
 
#=============================hog descriptor=====================================    
def hog_descriptor():
    print datetime.datetime.now().time()
    fp1=open("image.txt",'r')
    images=pickle.load(fp1)
    feature=[]
    for image in images:
        gray=color.rgb2gray(image)
        fd = hog(gray, orientations=8, pixels_per_cell=(16, 16),
                 cells_per_block=(1, 1))
        feature.append(fd)
    fp2=open("hog.txt",'w')
    pickle.dump(feature,fp2)
    print datetime.datetime.now().time()
 

#===============================lbp===========================================
def lbp():
    print datetime.datetime.now().time()
    fp1=open("image.txt",'r')
    images=pickle.load(fp1)
    print datetime.datetime.now().time()
    gray=color.rgb2gray(images[0])
    lbp= local_binary_pattern(gray, P =16, R =2 , method ='uniform')
    print lbp.shape
    print lbp


#read_image(path)
#hog_descriptor()
#lbp()


