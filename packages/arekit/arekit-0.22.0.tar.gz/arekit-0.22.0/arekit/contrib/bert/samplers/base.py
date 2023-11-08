from arekit.common.data.input.providers.label.multiple import MultipleLabelProvider
from arekit.common.data.input.providers.rows.samples import BaseSampleRowProvider
from arekit.common.data.input.providers.text.single import BaseSingleTextProvider
from arekit.common.data.input.terms_mapper import OpinionContainingTextTermsMapper


def create_simple_sample_provider(label_scaler, text_terms_mapper):
    assert(isinstance(text_terms_mapper, OpinionContainingTextTermsMapper))

    return BaseSampleRowProvider(
        label_provider=MultipleLabelProvider(label_scaler=label_scaler),
        text_provider=BaseSingleTextProvider(text_terms_mapper=text_terms_mapper))
