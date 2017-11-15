import pickle;

#data structure for the cluster
#initilize a list,append a point to the cluster
#add a list of data point

class Cluster:
    # total_time = 0;
    
    def __init__(self,cluster_id,created_time):
        
        self.cluster_id = cluster_id
        self.tweet_ids = []
        self.created_time = created_time
        self.total_time = 0
        self.total_rate_change = 0
        self.neighbour_list=[]
        self.hashtags_list=[]
        self.representative_words = []

                
     
    def getMeanTime(self):
        try:
            return self.total_time/float(len(self.tweet_ids));
        except Exception, e:
            return 0;
        else:
            pass
        finally:
            pass



    def addNeighbour(self,neighbour):
        self.neighbour_list.append(neighbour)

    def getNeighbours(self):
        return self.neighbour_list
       
    def setTotalRateChange(self,total_rate_change):
        self.total_rate_change = total_rate_change

    def setClusterId(self,cluster_id):
        self.cluster_id = cluster_id

    def getClusterId(self):
        return self.cluster_id

    def getTweetList(self):
        return self.tweet_list
    
    def getFeatureList(self):
        return self.feature_list

    def getTweetIDs(self):
        return self.tweet_ids

    def getHashTags(self):
        return self.hashtags_list

    def getTotalRateChange(self):
        return self.total_rate_change

    def addHashTag(self,hashtag):
        self.hashtags_list.append(hashtag)

    def removeNeighbour(self,tweet_id):
        self.neighbour_list.remove(tweet_id)

    def add(self,vector):
        removed = [];
        if vector is None:
            return

        for term in vector:
            if term not in self.representative_words:
                self.representative_words.append(term);

        for word in self.representative_words:
            ngram = word.split();
            if len(ngram) > 1:
                for term in self.representative_words:
                    if term != word and term in ngram:
                        removed.append(term);

        self.representative_words = [term for term in self.representative_words if term not in removed];

    

    def addData(self,tweet_id,time_stamp):
        self.tweet_ids.append(tweet_id)
        # self.total_time = self.total_time + time_stamp;
     
        
    def getRepresentativeWords(self):      
        return self.representative_words;

        
        