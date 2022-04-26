import Classes.Query as Query
import Classes.Document as Document
import numpy as np

class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader):
        self.indexReader = ixReader
        self.mu = 2000                 # for smoothing

        # Get all document lengths and store in list
        self.doc_lengths = []
        i = 0
        while True:
            try:
                self.doc_lengths.append(self.indexReader.getDocLength(i))
                i = i + 1
            except:
                break
        self.total_doc_count = i
        self.entire_collection_word_count = sum(self.doc_lengths)


    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # Returned documents should be a list of Document.
    def retrieveQuery(self, query, topN, min_time=None):

        # Get query terms by splitting query content
        query_terms = query.queryContent.split()

        # Dictionaries represent word counts c(qi in d) and p(qi | d)
        word_counts_matrix = dict()         # c(qi in d)
        prob_word_in_doc_matrix = dict()    # p(qi | d) 

        # This contains P(Q|Md) per document (prod of all p(qi in d))
        overall_query_probs = np.ones((self.total_doc_count,))

        # Loop through each query term 
        for q in query_terms:

            # If word is not in collection, ignore
            collection_count = self.indexReader.CollectionFreq(q)
            if collection_count == 0:
                continue

            # Initialize matrix for term with numpy array of 0s (represent term counts and probs for each doc)
            word_counts_matrix[q] = np.zeros((self.total_doc_count,))
            prob_word_in_doc_matrix[q] = np.zeros((self.total_doc_count,))
        
            # Get postings list and counts # of words per document; index into word_counts_matrix with counts
            post_list = self.indexReader.getPostingList(q)
            for i in post_list.keys():
                word_count_in_this_doc = post_list[i]
                word_counts_matrix[q][int(i)] = word_count_in_this_doc

            # Compute prob of seeing word across entire collection
            prob_query_in_entire_collection = np.sum(word_counts_matrix[q]) / self.entire_collection_word_count
            
            # Compute P(Q|Md) = prod P(qi|Md); P(qi|Md) = (c(w;d) + mu*p(w|C)) / ((sum_w c(w;d))+mu) 
            # Query likelihood with Dirichlet smoothing
            for i in range(self.total_doc_count):
                prob_word_in_doc_matrix[q][int(i)] = (word_counts_matrix[q][int(i)] + (self.mu*prob_query_in_entire_collection)) / (self.doc_lengths[i] + self.mu)
                overall_query_probs[int(i)] = overall_query_probs[int(i)] * prob_word_in_doc_matrix[q][int(i)]

        # Get idx of topN docs in terms of P(Q|Md)
        topval = self.total_doc_count
        idx = np.argpartition(overall_query_probs, -topval)[-topval:]   
        idx = np.flip(idx[np.argsort(overall_query_probs[idx])])       # to make sure in correct order

        # Organize results into list of document objects
        docs = []
        for i in range(len(idx)):
            if min_time is None:
                doc_i = Document.Document()
                doc_i.setDocId(idx[i])
                doc_i.setDocNo(self.indexReader.getDocNo(idx[i]))
                doc_i.setDocDate(self.indexReader.getDocDate(idx[i]))
                doc_i.setScore(overall_query_probs[idx[i]])
                docs.append(doc_i)
            else:
                print(int(self.indexReader.getDocDate(idx[i])[:4]))
                if int(self.indexReader.getDocDate(idx[i])[:4]) >= min_time:
                    doc_i = Document.Document()
                    doc_i.setDocId(idx[i])
                    doc_i.setDocNo(self.indexReader.getDocNo(idx[i]))
                    doc_i.setDocDate(self.indexReader.getDocDate(idx[i]))
                    doc_i.setScore(overall_query_probs[idx[i]])
                    docs.append(doc_i)
            if len(docs) >= topN:
                break

        return docs
