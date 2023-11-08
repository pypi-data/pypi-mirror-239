# -*- coding: utf-8 -*-
from arekit.common.experiment.data_type import DataType
from arekit.contrib.bert.core.input.providers.text.pair import PairTextProvider
from arekit.common.experiment.input.formatters.sample import BaseSampleFormatter
from arekit.common.experiment.input.providers.label.multiple import MultipleLabelProvider
from arekit.common.experiment.input.terms_mapper import OpinionContainingTextTermsMapper
from arekit.common.labels.str_fmt import StringLabelsFormatter


class QaMultipleSampleFormatter(BaseSampleFormatter):
    """
    Default, based on COLA, but includes an extra text_b.
        text_b: Question w/o S.P (S.P -- sentiment polarity)

    Multilabel variant

    Notation were taken from paper:
    https://www.aclweb.org/anthology/N19-1035.pdf
    """

    def __init__(self, data_type, label_scaler, labels_formatter, text_terms_mapper, balance):
        assert(isinstance(labels_formatter, StringLabelsFormatter))
        assert(isinstance(text_terms_mapper, OpinionContainingTextTermsMapper))

        text_b_template = u'Что вы думаете по поводу отношения {subject} к {object} в контексте : << {context} >> ?'
        super(QaMultipleSampleFormatter, self).__init__(
            data_type=data_type,
            text_provider=PairTextProvider(
                text_b_template=text_b_template,
                labels_formatter=labels_formatter,
                text_terms_mapper=text_terms_mapper),
            label_provider=MultipleLabelProvider(label_scaler=label_scaler),
            balance=data_type == DataType.Train and balance)
