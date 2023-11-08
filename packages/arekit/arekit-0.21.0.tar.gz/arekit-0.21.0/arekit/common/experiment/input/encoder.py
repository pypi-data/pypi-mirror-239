from arekit.common.experiment.input.formatters.opinion import BaseOpinionsFormatter
from arekit.common.experiment.input.formatters.sample import BaseSampleFormatter
from arekit.common.experiment.input.providers.opinions import OpinionProvider
from arekit.common.utils import create_dir_if_not_exists


class BaseInputEncoder(object):

    @staticmethod
    def to_tsv(opinion_filepath, sample_filepath, opinion_provider,
               opinion_formatter, sample_formatter, write_sample_header):
        assert(isinstance(opinion_filepath, unicode))
        assert(isinstance(sample_filepath, unicode))
        assert(isinstance(opinion_formatter, BaseOpinionsFormatter))
        assert(isinstance(opinion_provider, OpinionProvider))
        assert(isinstance(sample_formatter, BaseSampleFormatter))
        assert(isinstance(write_sample_header, bool))

        # Create output directories
        create_dir_if_not_exists(opinion_filepath)
        create_dir_if_not_exists(sample_filepath)

        # Opinions
        opinion_formatter.format(opinion_provider)
        opinion_formatter.save(opinion_filepath)
        opinion_formatter.dispose_dataframe()

        # Samples
        sample_formatter.format(opinion_provider)
        sample_formatter.save(filepath=sample_filepath,
                              write_header=write_sample_header)
        sample_formatter.dispose_dataframe()
