from arekit.common.data import const
from arekit.common.data.storages.base import BaseRowsStorage
from arekit.common.data.views.linkages.multilabel import MultilableOpinionLinkagesView
from arekit.common.experiment.api.enums import BaseDocumentTag
from arekit.common.experiment.api.ops_doc import DocumentOperations
from arekit.common.experiment.api.ops_opin import OpinionOperations
from arekit.common.experiment.data_type import DataType
from arekit.common.experiment.handler import ExperimentIterationHandler
from arekit.common.experiment.pipelines.opinion_collections import output_to_opinion_collections_pipeline
from arekit.common.labels.scaler.base import BaseLabelScaler
from arekit.common.labels.str_fmt import StringLabelsFormatter
from arekit.common.model.labeling.modes import LabelCalculationMode
from arekit.common.pipeline.items.handle import HandleIterPipelineItem
from arekit.contrib.experiment_rusentrel.model_io.bert import RuSentRelExperimentBertIOUtils


class BaseOutputConverterIterationHandler(ExperimentIterationHandler):

    def __init__(self, exp_io, doc_ops, opin_ops, data_type, label_scaler, labels_formatter):
        assert(isinstance(exp_io, RuSentRelExperimentBertIOUtils))
        assert(isinstance(doc_ops, DocumentOperations))
        assert(isinstance(opin_ops, OpinionOperations))
        assert(isinstance(data_type, DataType))
        assert(isinstance(label_scaler, BaseLabelScaler))
        assert(isinstance(labels_formatter, StringLabelsFormatter))
        super(BaseOutputConverterIterationHandler, self).__init__(exp_io=exp_io,
                                                                  )
        self._data_type = data_type

        self.__exp_io = exp_io
        self.__doc_ops = doc_ops
        self.__opin_ops = opin_ops
        self.__labels_formatter = labels_formatter
        self.__label_scaler = label_scaler

    def __convert(self, output_storage, target_func):
        """ From `output_storage` to `target` conversion.
            output_storage: BaseRowsStorage
            target_func: func(doc_id) -- consdiered to provide a target for the particular document.
        """
        assert(isinstance(output_storage, BaseRowsStorage))
        assert(callable(target_func))

        cmp_doc_ids_set = set(self.__doc_ops.iter_tagget_doc_ids(BaseDocumentTag.Compare))

        # We utilize google bert format, where every row
        # consist of label probabilities per every class
        linkages_view = MultilableOpinionLinkagesView(labels_scaler=self.__label_scaler,
                                                      storage=output_storage)

        ppl = output_to_opinion_collections_pipeline(
            iter_opinion_linkages_func=lambda doc_id: linkages_view.iter_opinion_linkages(
                doc_id=doc_id,
                opinions_view=self.__exp_io.create_opinions_view(self._data_type)),
            doc_ids_set=cmp_doc_ids_set,
            create_opinion_collection_func=self.__opin_ops.create_opinion_collection,
            labels_scaler=self.__label_scaler,
            label_calc_mode=LabelCalculationMode.AVERAGE)

        # Writing opinion collection.
        save_item = HandleIterPipelineItem(
            lambda data:
            self.__exp_io.write_opinion_collection(collection=data[1],
                                                   labels_formatter=self.__labels_formatter,
                                                   target=target_func(data[0])))

        # Executing pipeline.
        ppl.append(save_item)

        input_data = set(output_storage.iter_column_values(column_name=const.DOC_ID))

        # iterate over the result.
        for _ in ppl.run(input_data):
            pass

    def _iter_output_and_target_pairs(self, iter_index):
        raise NotImplementedError()

    def on_iteration(self, iter_index):
        for output_storage, target in self._iter_output_and_target_pairs(iter_index):
            self.__convert(output_storage=output_storage, target_func=target)
