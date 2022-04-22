import Classes.Path as Path
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, DATETIME
from whoosh.analysis import RegexTokenizer

class MyIndexWriter:

    writer = []

    def __init__(self, type):
        path_dir = Path.IndexTextDir
        schema = Schema(doc_no=ID(stored=True), doc_date=DATETIME(stored=True, sortable=True),                  # we care about doc_no, doc_date, doc_content
                        doc_content=TEXT(analyzer=RegexTokenizer(), stored=True))
        indexing = index.create_in(path_dir, schema)
        self.writer = indexing.writer()

    def index(self, docNo, docDate, content):
        self.writer.add_document(doc_no=docNo, doc_date=docDate, doc_content=content)

    def close(self):
        self.writer.commit()
