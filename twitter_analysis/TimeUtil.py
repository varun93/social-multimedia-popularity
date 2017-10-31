from datetime import datetime, timedelta
import time

class TimeUtil:
    
    regexp = {"RT": "^RT", "MT": r"^MT", "ALNUM": r"(@[a-zA-Z0-9_]+[:]*)",
              "HASHTAG": r"(#[\w\d]+[:]*)", "URL": r"(^http|^https)"}


    
    @staticmethod
    def getTimestamp(date):
        return time.mktime(date.timetuple())



    @staticmethod
    def getTimeDifference(time1,time2):
        FMT = '%Y-%m-%d %H:%M:%S'
        tdelta = datetime.strptime(time2, FMT) - datetime.strptime(time1, FMT)
        total_seconds = tdelta.days*24*60*60 + tdelta.seconds
        total_hours = total_seconds / 3600.0
        return total_hours


    @staticmethod
    def getCurrentTime():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       

