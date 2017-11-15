from datetime import datetime, timedelta
import time

class TimeUtils:
   


    
    @staticmethod
    def getTimestamp(date):
        return time.mktime(date.timetuple())



    @staticmethod
    def getTimeDifference(time1,time2):
        FMT = '%Y-%m-%d %H:%M:%S'
        tdelta = datetime.strptime(time2, FMT) - datetime.strptime(time1, FMT)
        total_seconds = tdelta.days*24*60*60 + tdelta.seconds
        total_minutes = total_seconds / 60.0
        return total_minutes


    @staticmethod
    def getCurrentTime():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       

