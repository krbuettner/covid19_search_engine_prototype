import Classes.Query as Query
import Classes.Document as Document
import Classes.Path as Path
import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh import scoring


class QueryRetrievalModelBoolean:

    indexReader = []

    query_parser = []
    searcher = []

    def __init__(self, ixReader):
        path_dir = Path.IndexTextDir
        self.searcher = index.open_dir(path_dir).searcher()
        self.query_parser = QueryParser("doc_content", self.searcher.schema)
        return

    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.

    def retrieveQuery(self, query):
        corrector = self.searcher.corrector("doc_content")
        q = self.query_parser.parse(query.getQueryContent())

        corrected = self.searcher.correct_query(q, query.getQueryContent())
        if corrected.query != q:
            print("Did you mean:", corrected.string)

        query_input = self.query_parser.parse(corrected.string)
        search_results = self.searcher.search(
            query_input, scored=False, sortedby="doc_date", reverse=True)

        return_docs = []
        for result in search_results:
            a_doc = Document.Document()
            a_doc.setDocId(result.docnum)

            a_doc.setDocNo(self.searcher.stored_fields(
                result.docnum)["doc_no"])

            a_doc.setDocDate(self.searcher.stored_fields(
                result.docnum)["doc_date"])

            return_docs.append(a_doc)
        return return_docs
