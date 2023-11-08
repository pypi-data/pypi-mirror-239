from arekit.common.experiment.cv.doc_stat.base import BaseDocumentStatGenerator
from arekit.common.news.base import News


class SentenceBasedDocumentStatGenerator(BaseDocumentStatGenerator):

    def __init__(self, doc_reader_func):
        super(SentenceBasedDocumentStatGenerator, self).__init__(doc_reader_func)

    def _calc(self, news):
        assert(isinstance(news, News))
        return news.SentencesCount
