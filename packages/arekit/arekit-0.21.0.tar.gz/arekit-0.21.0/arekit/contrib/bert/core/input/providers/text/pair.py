# -*- coding: utf-8 -*-
from arekit.common.experiment.input.providers.text.single import BaseSingleTextProvider
from arekit.common.entities.types import EntityType
from arekit.common.labels.base import Label
from arekit.common.labels.str_fmt import StringLabelsFormatter


class PairTextProvider(BaseSingleTextProvider):
    """
    Provides additionally text_b parameter

    Considered to utilize an inner part in context, between opinion participants.
    """

    TEXT_B = u"text_b"

    def __init__(self, text_b_template, labels_formatter, text_terms_mapper):
        """
        text_b_template: unicode
            assumes to include {subject}, {object}, and {context} in related template,
            and {label} (optional)
        labels_formatter: StringLabelsFormatter
        """
        assert(isinstance(text_b_template, unicode))
        assert(isinstance(labels_formatter, StringLabelsFormatter))
        super(PairTextProvider, self).__init__(text_terms_mapper=text_terms_mapper)
        self.__text_b_template = text_b_template
        self.__labels_formatter = labels_formatter

    def get_text_template(self):
        raise NotImplementedError()

    def iter_columns(self):
        for col_name in super(PairTextProvider, self).iter_columns():
            yield col_name
        yield self.TEXT_B

    def add_text_in_row(self, set_text_func, sentence_terms, s_ind, t_ind, expected_label):
        assert(callable(set_text_func))
        assert(isinstance(expected_label, Label))

        # We consider text_a as a default, i.e. the formatting provided by a base provider.
        super(PairTextProvider, self).add_text_in_row(set_text_func=set_text_func,
                                                      sentence_terms=sentence_terms,
                                                      s_ind=s_ind,
                                                      t_ind=t_ind,
                                                      expected_label=expected_label)

        # As for a source of the text_b, we consider an inner context of the attitude
        # mentioned in context. So we crop inner part of a context, including subject
        # and object of the opinion.
        first = min(s_ind, t_ind)
        last = max(s_ind, t_ind)
        inner_terms = sentence_terms[first:last + 1]
        self._mapper.set_s_ind(0)
        self._mapper.set_t_ind(len(inner_terms)-1)

        inner_context = self._handle_terms_and_compose_text(sentence_terms=inner_terms)

        value = self.__text_b_template.format(
            subject=self._mapper.StringEntitiesFormatter.to_string(None, EntityType.Subject),
            object=self._mapper.StringEntitiesFormatter.to_string(None, EntityType.Object),
            context=self._process_text(inner_context),
            label=self.__labels_formatter.label_to_str(expected_label))

        set_text_func(column=self.TEXT_B, value=value)