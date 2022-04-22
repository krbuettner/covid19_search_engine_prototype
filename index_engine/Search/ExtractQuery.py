import Classes.Query as Query
import Classes.Path as Path
from nltk.stem.porter import *

class ExtractQuery:

	def __init__(self):

		# Load queries by parsing through tags
		self.queries = []
		with open(Path.TopicDir, "r") as f:
			all_lines = f.readlines()
		topics = []
		count = -1
		for line in all_lines:
			if '<top>' in line:
				count = count + 1
				topics.append([])
			topics[count].append(line.strip())
		queries = []
		for topic in topics:
			for element in topic:
				if '<title>' in element:
					element = element.replace('<title>','').strip()
					queries.append(element.lower())						# Make lowercase here

		# Tokenize queries into words
		queries_split = [[] for i in range(len(queries))]
		index = 0
		for q in queries:
			queries_split[index] = q.split()
			index = index + 1

		# Load and remove stopwords, remove nonalphanumeric char, perform stemming
		stemmer = PorterStemmer()
		with open(Path.StopwordDir, 'r') as f:
			self.stop_words = []
			for l in f.readlines():
				self.stop_words.append(l.strip())
		queries_split_wo_stop = [[] for i in range(len(queries_split))]
		for i in range(len(queries_split)):
			queries_split_wo_stop[i] = ''
			for j in range(len(queries_split[i])):
				s = ''.join(filter(str.isalnum, queries_split[i][j]))				
				if not s in self.stop_words:
					s = stemmer.stem(s)
					if j == len(queries_split[i]) - 1:
						queries_split_wo_stop[i] = queries_split_wo_stop[i] + s 
					else:
						queries_split_wo_stop[i] = queries_split_wo_stop[i] + s + ' '

		# Store final processed queries with query objects
		self.processed_queries = []
		qid = 0
		for q in queries_split_wo_stop:
			new_q = Query.Query()
			new_q.setTopicId(qid)
			new_q.setQueryContent(q)
			self.processed_queries.append(new_q)
			qid = qid + 1

	# Return extracted queries with class Query in a list.
	def getQuries(self):
		# already did the processing, just return processed queries 
		return self.processed_queries

