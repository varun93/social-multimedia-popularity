from config import *

class DBUtils:
        
    @staticmethod
    def insertStats(tweet_id,retweet_count):

        cursor = db.cursor()
        sql = "INSERT INTO stats(tweet_id,retweet_count,last_updated) VALUES('%s','%d','%s')"%(tweet_id,retweet_count,TimeUtils.getCurrentTime())
        try:
            cursor.execute(sql)
            db.commit()
        except:
            raise

        cursor.close()
   

    @staticmethod
    def insertTweet(tweet_id,tweet_text):
        cursor = db.cursor()
        sql = "INSERT INTO twitter_data(tweet_id,tweet_text) VALUES('%s','%s')"%(tweet_id,tweet_text)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            raise

        cursor.close() 



    