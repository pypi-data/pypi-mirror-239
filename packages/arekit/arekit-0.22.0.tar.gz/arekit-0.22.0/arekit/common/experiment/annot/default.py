import logging

from arekit.common.experiment.annot.algo.base import BaseAnnotationAlgorithm
from arekit.common.experiment.annot.base import BaseAnnotator
from arekit.common.experiment.api.ops_opin import OpinionOperations
from arekit.common.experiment.data_type import DataType
from arekit.common.news.parsed.base import ParsedNews
from arekit.common.opinions.collection import OpinionCollection

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DefaultAnnotator(BaseAnnotator):
    """ Algorithm-based annotator
    """

    def __init__(self, annot_algo):
        super(DefaultAnnotator, self).__init__()
        assert(isinstance(annot_algo, BaseAnnotationAlgorithm))
        self.__annot_algo = annot_algo

    # region private methods

    def _annot_collection_core(self, parsed_news, data_type, opin_ops):
        assert(isinstance(parsed_news, ParsedNews))
        assert(isinstance(data_type, DataType))
        assert(isinstance(opin_ops, OpinionOperations))

        opinions = opin_ops.get_etalon_opinion_collection(doc_id=parsed_news.RelatedDocID)

        annotated_opins_it = self.__annot_algo.iter_opinions(
            parsed_news=parsed_news,
            existed_opinions=opinions if data_type == DataType.Train else None)

        collection = opin_ops.create_opinion_collection(None)
        assert(isinstance(collection, OpinionCollection))

        # Filling. Keep all the opinions without duplications.
        for opinion in annotated_opins_it:
            if collection.has_synonymous_opinion(opinion):
                continue
            collection.add_opinion(opinion)

        return collection

    # endregion

