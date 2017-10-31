import math;
import numpy as np;
from nltk import PorterStemmer




class Similarity:

	
	@staticmethod
	def intersection(list1,list2):
		if list1 == None or list2 == None:
			return [];
		return [w1 for w1 in list1 for w2 in list2 if w1 == w2 or w1 in w2.split() or w2 in w1.split()];
	
	
	@staticmethod
	def union(list1,list2):
		if list1 == None and list2 == None:
			return [];
		elif list1 == None:
			return list2;
		elif list2 == None:
			return list1;
		else:
			result = list1+list2;
			removed = [];
			for word in result:
		            ngram = word.split();
		            if len(ngram) > 1:
		                for term in result:
		                    if term != word and term in ngram:
		                        removed.append(term);

			return [term for term in result if term not in removed];


	@staticmethod
	def greater(a,b):
		len_a = len(a)
		len_b = len(b)
		if len_a > len_b:
			return a

		return b


	@staticmethod
	def isEqual(a,b):

		stemmer = PorterStemmer()
		
		if a is None or b is None or len(a) == 0 or len(b) == 0:
			return False

		if a == b:
			return True

		len_a = len(a.split())
		len_b = len(b.split())

		if len_a == 1 and len_b == 1:
			stem_a = stemmer.stem(a)
			stem_b = stemmer.stem(b)
			if stem_a == stem_b:
				return True
			else:
				return False



		max_len = len_b
		max_str = b
		other_str = a



		if len_a > max_len:
			max_len = len_a
			max_str = a
			other_str = b


		
		equal_counter = False

		for word_a in max_str.split():
			for word_b in other_str.split():
				stem_a = stemmer.stem(word_a)
				stem_b = stemmer.stem(word_b)
				
				if stem_a == stem_b:
					equal_counter = True
					break
			
			if equal_counter == True:
				return True

		return False


	@staticmethod
	def intersection2(list1,list2):
		if list1 is None or list2 is None:
			return [];
		return [Similarity.greater(w1,w2) for w1 in list1 for w2 in list2 if Similarity.isEqual(w1,w2)];
		

	@staticmethod
	def union2(list1,list2):
		if list1 is None and list2 is None:
			return [];
		elif list1 is None:
			return list2
		elif list2 is None:
			return list1
		else:
			result = list1+list2
			for item_a in list1:
				for item_b in list2:
					if Similarity.isEqual(item_a,item_b):
						if len(item_a) > len(item_b):
							if item_b in result:
								result.remove(item_b)
							
						else:
							if item_a in result:
								result.remove(item_a)
						break	
							
							
		return result


	@staticmethod
	def remove_dup(result):
		removed = [];
		for word in result:
		    ngram = word.split();
		    if len(ngram) > 1:
		        for term in result:
		            if term != word and term in ngram:
		                removed.append(term);

		return [term for term in result if term not in removed];

	@staticmethod
	def jaccard(twitter_feature,representative_words):
		num  = set(Similarity.intersection2(twitter_feature,representative_words));#intersection is wrong
		denom = set(Similarity.union2(twitter_feature,representative_words)); # union is wrong so using set
		num=Similarity.remove_dup(num)
		
		try:
			return len(num)/float(len(denom));
		except Exception, e:
			return 0;
		else:
			pass
		finally:
			pass

	@staticmethod
	def sigmoidSim(jaccard,time_dif):
		time_dif=float(time_dif)/1800
		return 1.0 / (1.0 + np.exp(-(jaccard/(np.log(time_dif+1)/np.log(3)))))    
        #sim=pow(time_dif,-(1-jaccard)) 
     

# print Similarity.jaccard(['dravid', 'india'],['sachin','india'])

# print Similarity.jaccard(['world cup', 'dale steyn', 'chris gayle', 'firing line', 'cwc15'],['cwc15', 'monk', 'batsman'])

# print Similarity.jaccard(['samsung', 'samsung galaxy', 's6', 'edge', 'htc', 'htc one', 'm9', 'flagships'],
#['samsung galaxy', 's6', 'htc one', 'm9'])

#print Similarity.remove_dup(['samsung', 'samsung galaxy', 's6', 'edge', 'htc', 'htc one', 'm9', 'flagships'])

#print Similarity.jaccard(['india'],['rainfall', 'shivers', 'north india'])

#print Similarity.jaccard(['police', 'convoy', 'fadnavis'],['sohrabuddin sheikh fake encounter', 'cbi', 'gujarat', 'gujarat police', 'police officer', 'johri'])

#print Similarity.jaccard(['narendra modi', 'parliament', 'canteen', 'mps', 'gujarat', 'rs', 'thali'],['mps', 'gujarat'])
# '''
# f1=['sohrabuddin sheikh fake encounter', 'cbi', 'gujarat police', 'police officer', 'johri']
# f2=['police', 'convoy', 'fadnavis']

# print Similarity.jaccard(f2,f1)'''
