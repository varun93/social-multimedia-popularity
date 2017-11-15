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

views=[]
images=[]
path="Path to images"

#==============================================================================
def normalize(a):
    a = np.array(a)
    min,max=np.min(a),np.max(a)
    #print max
    nmin,nmax=1,100
    dif=max-min
    ndif=nmax-nmin
    return [(((float(item)-min)/dif)*ndif)+nmin for item in a ]



#==========================SVR=================================================  

def svrmodel():
    
    fp4=open("feature_vectors.txt",'r')
    feature=pickle.load(fp4)

    fp5=open("imdb_ratings.txt",'r')
    views=pickle.load(fp5)

    
    train_feature=feature[:800]
    train_views=views[:800]
    test_feature=feature[700:]
    test_views=views[700:]

    print len(train_feature)
    print len(train_views)

     
    c_range= np.logspace(-4, 4, 6)
    g_range=np.logspace(-4, 4, 6)
    # parameters = {'kernel':['linear'], 'C':c_range}

    tuned_parameters = [{'kernel': ['rbf'], 'gamma': g_range,'C': c_range}]
    estimator = linear_model.LinearRegression()
    # estimator = SVR()
    svr_lin=GridSearchCV(estimator=estimator, param_grid={'C':c_range},cv=10)
    svr_lin.fit(train_feature,train_views)

    # with a rbf 
    # svr_rbf=GridSearchCV(estimator=estimator, param_grid=tuned_parameters,cv=5)
    # svr_rbf.fit(train_feature,train_views)

    #cross_score=cross_validation.cross_val_score(svr_lin,train_feature,train_views,cv=5)
    #print cross_score
     

    #fp8=open("svr.txt",'r')
    #svr_lin=pickle.load(fp8)
   
    """svr_lin=SVR(kernel='rbf', C=1e4, gamma=1e4,cache_size=500)
    #svr_lin=SVR(kernel='linear', C=1e4)
    svr_lin.fit(train_feature,train_views)"""
     
    predicted_views=svr_lin.predict(test_feature)
    real_score=svr_lin.score(test_feature,test_views)
   

    #print spearmanr(test_views,predicted_views)
    print spearmanr(test_views,predicted_views)
    print math.sqrt(metrics.mean_squared_error(test_views,predicted_views))
    #print metrics.r2_score

    #fp7=open("svr_objects2.txt",'w')
    #pickle.dump(svr_lin,fp7)  

    print datetime.datetime.now().time()

#==============================================================================  
svrmodel()


