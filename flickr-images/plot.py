import MySQLdb
from sklearn import cluster,datasets
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pylab as pl
import pickle
import math
from operator import itemgetter
from db import *


def KMeans(views):
  k_means = cluster.KMeans(n_clusters=3)
  views = np.array(views).reshape(len(views),1)
  k_means.fit(views)
  print(k_means.labels_[:])
  print(k_means.cluster_centers_[:])

  for item in k_means.labels_[:]:
    print item

def viewsDistribution(views):
  views.sort()
  fit = stats.norm.pdf(views, np.mean(views), np.std(views))  #fitting indeed
  pl.plot(views,fit,'-o')
  pl.hist(views,normed=True)      #use this to draw histogram of your data
  pl.show()  


def outliers(views):
  views = np.array(views)
  mean = views.mean()
  std = views.std()
  outliers = [element for element in views if ((math.fabs(element-mean)) > (3*std))] 
  return outliers



# dict = pickle.load(open('views.txt','rb'))
# views = np.array(sorted(dict.values()))
# viewsDistribution(views)
# KMeans(views)
# views = getViews()







