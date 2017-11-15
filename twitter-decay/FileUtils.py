import pickle
import os


class FileUtils:
    


    @staticmethod
    def persist(filename,object):
        file_handle = open(filename,'w')
        pickle.dump(object,file_handle)

    @staticmethod
    def isFileEmpty(filename):
        return os.stat(filename).st_size == 0

    @staticmethod
    def getObject(filename):

        if FileUtils.isFileEmpty(filename):
            return dict()
            
        try:
            return pickle.load(open(filename,'r'))
        except Exception, e:
            raise
       