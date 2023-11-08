import logging

from arekit.common.experiment.formats.base import BaseExperiment
from arekit.contrib.experiment_rusentrel.common import entity_to_group_func
from arekit.contrib.experiment_rusentrel.exp_ds.documents import RuAttitudesDocumentOperations
from arekit.contrib.experiment_rusentrel.exp_ds.folding import create_ruattitudes_experiment_data_folding
from arekit.contrib.experiment_rusentrel.exp_ds.opinions import RuAttitudesOpinionOperations
from arekit.contrib.experiment_rusentrel.exp_ds.utils import read_ruattitudes_in_memory
from arekit.contrib.source.ruattitudes.io_utils import RuAttitudesVersions

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RuAttitudesExperiment(BaseExperiment):
    """ Application of distant supervision, especially for pretraining purposes.
        Suggested to utilize with a large RuAttitudes-format collections (v2.0-large).
    """

    def __init__(self, exp_data, experiment_io_type, version, load_docs, extra_name_suffix, do_log):
        assert(isinstance(version, RuAttitudesVersions))
        assert(isinstance(load_docs, bool))
        assert(isinstance(do_log, bool))

        # Setup logging option.
        self._init_log_flag(do_log)

        self.__version = version
        self.__extra_name_suffix = extra_name_suffix
        self.__do_log = do_log

        self.log_info(u"Init experiment io ...")
        experiment_io = experiment_io_type(self)

        self.log_info(u"Loading RuAttitudes collection optionally [{version}] ...".format(version=version))
        ru_attitudes = read_ruattitudes_in_memory(version=version,
                                                  used_doc_ids_set=None,
                                                  keep_doc_ids_only=not load_docs)

        folding = create_ruattitudes_experiment_data_folding(
            doc_ids_to_fold=list(ru_attitudes.iterkeys()))

        self.log_info(u"Create document operations ... ")
        doc_ops = RuAttitudesDocumentOperations(exp_data=exp_data,
                                                folding=folding,
                                                ru_attitudes=ru_attitudes)

        self.log_info(u"Create opinion operations ... ")
        opin_ops = RuAttitudesOpinionOperations(ru_attitudes=ru_attitudes)

        exp_name = u"ra-{ra_version}".format(ra_version=self.__version.value)

        super(RuAttitudesExperiment, self).__init__(exp_data=exp_data,
                                                    experiment_io=experiment_io,
                                                    opin_ops=opin_ops,
                                                    doc_ops=doc_ops,
                                                    name=exp_name,
                                                    extra_name_suffix=extra_name_suffix)

    def log_info(self, message, forced=False):
        assert (isinstance(message, unicode))
        if not self.__do_log and not forced:
            return
        logger.info(message)

    def entity_to_group(self, entity):
        return entity_to_group_func(entity, synonyms=None)
