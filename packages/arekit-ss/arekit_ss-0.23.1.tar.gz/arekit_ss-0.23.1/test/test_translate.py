import logging
import unittest

from arekit.common.data.input.providers.const import IDLE_MODE
from arekit.common.entities.base import Entity
from arekit.common.context.token import Token
from arekit.common.news.sentence import BaseNewsSentence
from arekit.common.news.base import News
from arekit.common.news.parser import NewsParser
from arekit.common.pipeline.context import PipelineContext
from arekit.contrib.utils.pipelines.items.text.tokenizer import DefaultTextTokenizer
from arekit.contrib.utils.pipelines.items.text.entities_default import TextEntitiesParser
from arekit.common.text.parser import BaseTextParser

from arekit_ss.text_parser.translator import TextAndEntitiesGoogleTranslator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class TestTestParser(unittest.TestCase):

    def test(self):
        text = "А контроль над этими провинциями — [США] , которая не пытается ввести санкции против."

        # Adopting translate pipeline item, based on google translator.
        text_parser = BaseTextParser(pipeline=[
            TextEntitiesParser(),
            TextAndEntitiesGoogleTranslator(src="ru", dest="en"),
            DefaultTextTokenizer(keep_tokens=True),
        ])

        news = News(doc_id=0, sentences=[BaseNewsSentence(text.split())])
        parsed_news = NewsParser.parse(news=news, text_parser=text_parser,
                                       parent_ppl_ctx=PipelineContext({IDLE_MODE: False}))
        self.debug_show_terms(parsed_news.iter_terms())

    @staticmethod
    def debug_show_terms(terms):
        for term in terms:
            if isinstance(term, str):
                print("Word:\t\t'{}'".format(term))
            elif isinstance(term, Token):
                print("Token:\t\t'{}' ('{}')".format(term.get_token_value(),
                                                            term.get_meta_value()))
            elif isinstance(term, Entity):
                print("Entity:\t\t'{}' ({})".format(term.Value, type(term)))
            else:
                raise Exception("unsupported type {}".format(term))


if __name__ == '__main__':
    unittest.main()