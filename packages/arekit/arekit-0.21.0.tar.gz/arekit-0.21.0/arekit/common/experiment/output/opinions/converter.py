from arekit.common.experiment.extract.opinions import fill_opinion_collection
from arekit.common.experiment.input.readers.opinion import InputOpinionReader
from arekit.common.experiment.output.base import BaseOutput
from arekit.common.labels.scaler import BaseLabelScaler
from arekit.common.model.labeling.modes import LabelCalculationMode
from arekit.common.model.labeling.single import SingleLabelsHelper
from arekit.common.opinions.base import Opinion


class OutputToOpinionCollectionsConverter(object):

    @staticmethod
    def iter_opinion_collections(output_filepath,
                                 opinions_reader,
                                 labels_scaler,
                                 keep_doc_id_func,
                                 create_opinion_collection_func,
                                 label_calculation_mode,
                                 supported_labels,
                                 output):
        assert(callable(keep_doc_id_func))
        assert(isinstance(labels_scaler, BaseLabelScaler))
        assert(isinstance(output_filepath, unicode))
        assert(isinstance(opinions_reader, InputOpinionReader))
        assert(callable(create_opinion_collection_func))
        assert(isinstance(label_calculation_mode, LabelCalculationMode))
        assert(isinstance(supported_labels, set) or supported_labels is None)
        assert(isinstance(output, BaseOutput))

        output.init_from_tsv(filepath=output_filepath)

        labels_helper = SingleLabelsHelper(labels_scaler)

        for news_id in output.iter_news_ids():

            if not keep_doc_id_func(news_id):
                continue

            collection = create_opinion_collection_func()

            linked_iter = output.iter_linked_opinions(news_id=news_id,
                                                      opinions_reader=opinions_reader)

            fill_opinion_collection(
                collection=collection,
                linked_data_iter=linked_iter,
                labels_helper=labels_helper,
                to_opinion_func=OutputToOpinionCollectionsConverter.__to_label,
                label_calc_mode=label_calculation_mode,
                supported_labels=supported_labels)

            yield news_id, collection

    @staticmethod
    def __to_label(item, label):
        assert(isinstance(item, Opinion))
        return Opinion(source_value=item.SourceValue,
                       target_value=item.TargetValue,
                       sentiment=label)
