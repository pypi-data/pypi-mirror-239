import unittest

from arekit.common.entities.base import Entity
from arekit.common.news.parsed.base import ParsedNews
from arekit.contrib.experiment_rusentrel.labels.scalers.ruattitudes import ExperimentRuAttitudesLabelConverter
from arekit.contrib.experiment_rusentrel.synonyms.provider import RuSentRelSynonymsCollectionProvider
from arekit.contrib.source.ruattitudes.collection import RuAttitudesCollection
from arekit.contrib.source.ruattitudes.io_utils import RuAttitudesVersions
from arekit.contrib.source.ruattitudes.news.base import RuAttitudesNews
from arekit.contrib.source.ruattitudes.news.parse_options import RuAttitudesParseOptions
from arekit.contrib.source.rusentrel.io_utils import RuSentRelVersions
from arekit.contrib.source.rusentrel.news.base import RuSentRelNews
from arekit.contrib.source.rusentrel.news.parse_options import RuSentRelNewsParseOptions
from arekit.processing.lemmatization.mystem import MystemWrapper
from arekit.processing.text.parser import TextParser


class TestPartOfSpeech(unittest.TestCase):

    def test_ruattitudes_news_text_parsing(self):
        news_it = RuAttitudesCollection.iter_news(version=RuAttitudesVersions.Debug,
                                                  get_news_index_func=lambda _: 0,
                                                  label_convereter=ExperimentRuAttitudesLabelConverter(),
                                                  return_inds_only=False)

        for news in news_it:

            # Parse single sentence.
            assert(isinstance(news, RuAttitudesNews))
            parsed_text = news.parse_sentence(0)
            self.__print_parsed_text(parsed_text)

            # Parse news via external parser.
            stemmer = MystemWrapper()
            options = RuAttitudesParseOptions(stemmer=stemmer, frame_variants_collection=None)
            parsed_news = TextParser.parse_news(news=news, parse_options=options)
            assert(isinstance(parsed_news, ParsedNews))

    def test_rusentrel_news_text_parsing(self):
        stemmer = MystemWrapper()
        version = RuSentRelVersions.V11
        synonyms = RuSentRelSynonymsCollectionProvider.load_collection(stemmer=stemmer,
                                                                       version=version)
        news = RuSentRelNews.read_document(doc_id=1,
                                           synonyms=synonyms,
                                           version=version)

        assert(isinstance(news, RuSentRelNews))
        parsed_text = news.parse_sentence(8)
        self.__print_parsed_text(parsed_text)

        # Parse news via external parser.
        stemmer = MystemWrapper()
        options = RuSentRelNewsParseOptions(stemmer=stemmer, frame_variants_collection=None)
        parsed_news = TextParser.parse_news(news=news, parse_options=options)
        assert (isinstance(parsed_news, ParsedNews))

    def __print_parsed_text(self, parsed_text):
        assert(isinstance(parsed_text, list))
        print u"Length: {}".format(len(parsed_text))
        for t in parsed_text:
            if isinstance(t, Entity):
                print u"<{}>".format(t.Value),
            else:
                print u"'{}'".format(t),


if __name__ == '__main__':
    unittest.main()
