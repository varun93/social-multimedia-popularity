from __future__ import unicode_literals
import math
import json
from ftfy import fix_text
import string
from config import *
from Parse_Tweet import *
from AuthUtils import *
from DBUtils import *


def getTweetText(tweet,hash_tags=None,urls=None,mentions=None,symbols=None):
        
    filter = hash_tags+urls+mentions+symbols;

    try:
        # print [word.encode('utf-8').translate(None, string.punctuation) for word in tweet.split() if word not in filter]
        return [word for word in tweet.split() if word not in filter]
    except Exception, e:
        raise

class StdOutListener(StreamListener):



    def on_data(self, data):

        # load the update dictionary here
        last_update = FileUtils.getObject('last_update.txt')
        
        try:

            tweet= json.loads(data)
            
            if tweet['user']['screen_name'] in news_channels_list:
            
                text = fix_text(tweet['text'])
                original_text = text
                created = tweet['created_at']
                channel = tweet['user']['screen_name']
                retweet_count = tweet['retweet_count']
                tweet_id = str(tweet['id_str'])


                hash_tags = ParseTweet.getHashtags(text)
                urls = ParseTweet.getURLs(text)
                user_mentions = ParseTweet.getUserHandles(text) 
                symbols = ParseTweet.getRT(text)
                text =  getTweetText(text,hash_tags,urls,user_mentions,symbols)
                
                last_update[tweet_id] = TimeUtils.getCurrentTime()
                
                if text is not None:
                    text = ' '.join(text)
                    text = regex.sub('', text)
                    print text
                    DBUtils.insertTweet(tweet_id,text)
                    FileUtils.persist('last_update.txt',last_update)

                
        except Exception, e:
            print e
            pass
        else:
            pass
        finally:
            pass

    def on_error(self, status):
        print status

    



if __name__ == '__main__':
   
    l = StdOutListener()
    stream = Stream(AuthUtils.getStreamOauth(), l)
    stream.filter(follow=['240649814'],track=[])

   


   



