import logging

from arekit.common.experiment.api.base import BaseExperiment
from arekit.common.experiment.api.io_utils import BaseIOUtils
from arekit.contrib.experiment_rusentrel.common import create_text_parser
from arekit.contrib.experiment_rusentrel.exp_ds.documents import RuAttitudesDocumentOperations
from arekit.contrib.experiment_rusentrel.exp_ds.opinions import RuAttitudesOpinionOperations
from arekit.contrib.experiment_rusentrel.exp_ds.utils import read_ruattitudes_in_memory
from arekit.contrib.source.ruattitudes.entity.parser import RuAttitudesTextEntitiesParser
from arekit.contrib.source.ruattitudes.io_utils import RuAttitudesVersions

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_ruattitudes_experiment(exp_ctx, exp_io, version, load_docs, ra_doc_ids_func, ppl_items):
    """ Application of distant supervision, especially for pretraining purposes.
        Suggested to utilize with a large RuAttitudes-format collections (v2.0-large).
    """
    assert(isinstance(version, RuAttitudesVersions))
    assert(isinstance(exp_io, BaseIOUtils))
    assert(isinstance(load_docs, bool))
    assert(isinstance(ppl_items, list) or ppl_items is None)

    ru_attitudes = read_ruattitudes_in_memory(version=version,
                                              doc_id_func=ra_doc_ids_func,
                                              keep_doc_ids_only=not load_docs)

    text_parser = create_text_parser(exp_ctx=exp_ctx,
                                     entities_parser=RuAttitudesTextEntitiesParser(),
                                     value_to_group_id_func=None,
                                     ppl_items=ppl_items)

    logger.info("Create document operations ...")
    doc_ops = RuAttitudesDocumentOperations(exp_ctx=exp_ctx,
                                            ru_attitudes=ru_attitudes,
                                            text_parser=text_parser)

    logger.info("Create opinion operations ...")
    opin_ops = RuAttitudesOpinionOperations(ru_attitudes=ru_attitudes)

    return BaseExperiment(exp_ctx=exp_ctx, exp_io=exp_io, opin_ops=opin_ops, doc_ops=doc_ops)