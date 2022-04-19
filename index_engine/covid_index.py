import IndexingWithWhoosh.PreProcessedCorpusReader as PreprocessedCorpusReader
import IndexingWithWhoosh.MyIndexWriter as MyIndexWriter
import IndexingWithWhoosh.MyIndexReader as MyIndexReader
import datetime
from nltk.stem.porter import PorterStemmer


def WriteIndex(type):
    count = 0
    # Initiate pre-processed collection file reader.
    corpus = PreprocessedCorpusReader.PreprocessedCorpusReader(type)
    # Initiate the index writer.
    indexWriter = MyIndexWriter.MyIndexWriter(type)
    # Build index of corpus document by document.
    while True:
        doc = corpus.nextDocument()
        if doc == None:
            break
        indexWriter.index(doc[0], doc[1])
        count += 1
        if count % 1000 == 0:
            print("finish ", count, " docs")
    print("totally finish ", count, " docs")
    indexWriter.close()
    return

# IMPORTANT - MAKE THIS SAME AS DOC PARSER - TO DO


# Removing nonalphanumeric chars may not be good if symbols are of value
def clean_content(term, make_lowercase=True, stem=True, remove_nonalpha=True):
    stemmer = PorterStemmer()
    clean_content = term
    if make_lowercase:
        clean_content = clean_content.lower()
    if stem:
        clean_content = stemmer.stem(term)
    if remove_nonalpha:
        clean_content = ''.join(filter(str.isalnum, term))
    return clean_content


def ReadIndex(type, token):
    token = clean_content('mask')
    # Initiate the index file reader.
    index = MyIndexReader.MyIndexReader(type)
    # retrieve the token.
    df = index.DocFreq(token)
    ctf = index.CollectionFreq(token)
    print(" >> the token \""+token+"\" appeared in " + str(df) +
          " documents and " + str(ctf) + " times in total")
    if df > 0:
        posting = index.getPostingList(token)
        for docId in posting:
            docNo = index.getDocNo(docId)
            print(docNo+"\t"+str(docId)+"\t"+str(posting[docId]))


startTime = datetime.datetime.now()
WriteIndex("trectext")
endTime = datetime.datetime.now()
print("index web corpus running time: ", endTime - startTime)
startTime = datetime.datetime.now()
ReadIndex("trectext", "pandemic")
endTime = datetime.datetime.now()
print ("load index & retrieve the token running time: ", endTime - startTime)
