import logging

from arekit.common.experiment.api.ctx_base import ExperimentContext
from arekit.common.experiment.api.io_utils import BaseIOUtils
from arekit.common.experiment.api.ops_opin import OpinionOperations
from arekit.common.experiment.data_type import DataType
from arekit.common.opinions.collection import OpinionCollection
from arekit.contrib.experiment_rusentrel.labels.formatters.neut_label import ExperimentNeutralLabelsFormatter
from arekit.contrib.experiment_rusentrel.labels.formatters.rusentrel import RuSentRelExperimentLabelsFormatter
from arekit.contrib.source.rusentrel.io_utils import RuSentRelVersions
from arekit.contrib.source.rusentrel.opinions.collection import RuSentRelOpinionCollection


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RuSentrelOpinionOperations(OpinionOperations):

    def __init__(self, exp_ctx, exp_io, get_synonyms_func, version):
        assert(isinstance(exp_ctx, ExperimentContext))
        assert(isinstance(version, RuSentRelVersions))
        super(RuSentrelOpinionOperations, self).__init__()

        self.__get_synonyms_func = get_synonyms_func
        self.__version = version
        self.__exp_io = exp_io
        self.__result_labels_fmt = RuSentRelExperimentLabelsFormatter()
        self.__neutral_labels_fmt = ExperimentNeutralLabelsFormatter()

    @property
    def LabelsFormatter(self):
        return self.__neutral_labels_fmt

    # region CVBasedOperations

    def iter_opinions_for_extraction(self, doc_id, data_type):

        collections = []

        # Picking an annotated collection.
        target = self.__exp_io.create_opinion_collection_target(doc_id=doc_id, data_type=data_type)

        # Reading automatically annotated collection of neutral opinions.
        auto_neutral = self.__exp_io.read_opinion_collection(
            target=target,
            labels_formatter=self.__neutral_labels_fmt,
            create_collection_func=self.__create_collection)

        if data_type == DataType.Train:
            # Providing neutral and sentiment.
            if auto_neutral is not None:
                collections.append(auto_neutral)

            # Providing sentiment opinions.
            etalon = self.get_etalon_opinion_collection(doc_id=doc_id)
            collections.append(etalon)

        elif data_type == DataType.Test:
            # Providing neutrally labeled only
            collections.append(auto_neutral)

        for collection in collections:
            for opinion in collection:
                yield opinion

    def get_etalon_opinion_collection(self, doc_id):
        assert(isinstance(doc_id, int))
        opins_iter = RuSentRelOpinionCollection.iter_opinions_from_doc(
            doc_id=doc_id,
            labels_fmt=self.__result_labels_fmt,
            version=self.__version)
        return self.__create_collection(opins_iter)

    def create_opinion_collection(self, opinions):
        return self.__create_collection(opinions)

    def get_result_opinion_collection(self, doc_id, data_type, epoch_index):
        """ Since evaluation supported only for neural networks,
            we need to guarantee the presence of a function that returns filepath
            by using isinstance command.
        """
        assert(isinstance(self.__exp_io, BaseIOUtils))

        return self.__exp_io.read_opinion_collection(
            target=self.__exp_io.create_result_opinion_collection_target(
                doc_id=doc_id,
                data_type=data_type,
                epoch_index=epoch_index),
            labels_formatter=self.__result_labels_fmt,
            create_collection_func=lambda opinions: self.__create_collection(opinions))

    # endregion

    # region private provider methods

    def __create_collection(self, opinions=None):
        return OpinionCollection(opinions=[] if opinions is None else opinions,
                                 synonyms=self.__get_synonyms_func(),
                                 error_on_duplicates=True,
                                 error_on_synonym_end_missed=True)

    # endregion