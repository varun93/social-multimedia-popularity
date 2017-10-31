import re

class ParseTweet:
    
    regexp = {"RT": "^RT", "MT": r"^MT", "ALNUM": r"(@[a-zA-Z0-9_]+[:]*)",
              "HASHTAG": r"(#[\w\d]+[:]*)", "URL": r"(^http|^https)"}


    regexp = dict((key, re.compile(value)) for key, value in regexp.items())

    @staticmethod
    def getUserHandles(tweet):
        return [str(word) for word in re.findall(ParseTweet.regexp["ALNUM"], tweet)]

    @staticmethod
    def getHashtags(tweet):
        return [str(word) for word in re.findall(ParseTweet.regexp["HASHTAG"], tweet)]

    @staticmethod
    def getURLs(tweet):
        return [str(word) for word in  re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet)];

    @staticmethod
    def getRT(tweet):
        return [str(word) for word in re.findall(ParseTweet.regexp["RT"], tweet)]

  



# tweet = "RT @IBNLiveMovies #DilDhadakneDo: first look: Have you met the members of Mehra family yet?\nhttp://t.co/vpSzqfPLj5 http://t.co/f1o4mr9DBY"

# list =  ParseTweet.getUserHandles(tweet) + ParseTweet.getHashtags(tweet) + ParseTweet.getURLs(tweet) + ParseTweet.getRT(tweet)

# print list
# print [word for word in tweet.split() if word not in list]
 
