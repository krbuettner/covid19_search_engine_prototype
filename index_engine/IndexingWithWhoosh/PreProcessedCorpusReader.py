from datetime import date
import Classes.Path as Path

class PreprocessedCorpusReader:

    corpus = 0

    def __init__(self, type):
        self.corpus = open(Path.ResultHM1, "r", encoding="utf8")

    def nextDocument(self):
        docNo = self.corpus.readline().strip()
        if docNo == "":
            self.corpus.close()
            return
        date = self.corpus.readline().strip()
        content = self.corpus.readline().strip()
        return [docNo, date, content]
