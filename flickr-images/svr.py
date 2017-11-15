import os
import pickle
import datetime
import numpy as np
from sklearn.svm import SVR
from sklearn import cross_validation
import matplotlib.pyplot as plt
from sklearn.grid_search import GridSearchCV
from sklearn import preprocessing
from sklearn import  metrics
import math
from scipy.stats import spearmanr
from sklearn import linear_model
from db import *

views=[]
images=[]
path="PATH TO IMAGES"


#===========================pre-processing=====================================
def scaledViews():
     
     #fp4=open("hog.txt",'r')
     #feature=pickle.load(fp4)

     fp5=open("views.txt",'r')
     #fp5=open("viewsnorm.txt",'r')
     views=pickle.load(fp5)

     views_f=[float(view) for view in views]
    
     views_scaled = preprocessing.scale(views_f)
     fp6=open("scaled_views.txt",'w')
     pickle.dump(views_scaled,fp6)
     
     #print views_scaled[100:200]

     log2views=[math.log(view,2) for view in views]

     
     # norm_views=preprocessing.normalize(views_f, norm='l2')
     #print norm_views[100:200]

     #print views_scaled.mean(axis=0)
     #print views_scaled.std(axis=0)

     #scscaled_views={view:view_scaled for view in views for view_scaled in views_scaled}
     #print scscaled_views


#==========================SVR================================================  
def svrmodel():
    
    fp4=open("hog.txt",'r')
    feature=pickle.load(fp4)
    
    # fp5=open("views.txt",'r')
    fp5=open("scaled_views.txt",'r')
    views=pickle.load(fp5)
    
    train_feature=feature[:9500]
    train_views=views[:9500]
    test_feature=feature[9500:]
    test_views=views[9500:]

    c_range= np.logspace(-4, 4, 10)
    #parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
    estimator = SVR(kernel='linear')
    svr_lin=GridSearchCV(estimator=estimator, param_grid=dict(C=c_range),cv=2)
    #svr_lin=SVR(kernel='linear', C=1e3)
    svr_lin.fit(train_feature,train_views)

    #cross_score=cross_validation.cross_val_score(svr_lin,train_feature,train_views,cv=5)
    predicted_views=svr_lin.predict(test_feature)
    real_score=svr_lin.score(test_feature,test_views)



