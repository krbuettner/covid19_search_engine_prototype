import IndexingWithWhoosh.MyIndexReader as MyIndexReader
import Search.QueryRetreivalModel as QueryRetreivalModel
import Search.QueryRetreivalModelBoolean as QueryRetreivalModelBoolean
import Classes.Query as Query
from nltk.stem.porter import PorterStemmer
import datetime

# Removing nonalphanumeric chars may not be good if symbols are of value


def clean_content(query, make_lowercase=True, stem=True, remove_nonalpha=True):
    stemmer = PorterStemmer()
    query_list = query.split()
    clean_string = ''

    for term in query_list:
        a = term
        if make_lowercase:
            a = term.lower()
        if stem:
            a = stemmer.stem(a)
        if remove_nonalpha:
            a = ''.join(filter(str.isalnum, a))
        clean_string += a + ' '

    return clean_string


def get_query():
    query = input("Enter your query: ")
    return query


def set_query(query):
    aQuery = Query.Query()
    aQuery.setQueryContent(query)
    aQuery.setTopicId('Topic 1')
    return aQuery


index = MyIndexReader.MyIndexReader("trectext")

model = input("Boolean or BM25? ")
q = get_query()
clean = clean_content(q)
query = set_query(clean)

if (model == "Boolean"):
    limit = int(input("How many documents would you like returned? "))
    search = QueryRetreivalModelBoolean.QueryRetrievalModelBoolean(index)
    results = search.retrieveQuery(query, 20)
    rank = 1
    for result in results:
        print(query.getTopicId(), " Q0 ", result.getDocNo(),
              ' ', rank, " ", " MYRUN",)
        rank += 1
        if (rank == limit):
            break

else:
    search = QueryRetreivalModel.QueryRetrievalModel(index)
    results = search.retrieveQuery(query, 20)
    rank = 1
    for result in results:
        print(query.getTopicId(), " Q0 ", result.getDocNo(),
              ' ', rank, " ", result.getScore(), " MYRUN",)
        rank += 1
