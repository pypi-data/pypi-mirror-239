# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath
import sys
import unittest


sys.path.append('../../')

from tests.contrib.bert.labels import TestThreeLabelScaler
from arekit.common.experiment.input.providers.row_ids.multiple import MultipleIDProvider
from arekit.common.experiment.input.readers.sample import InputSampleReader
from arekit.contrib.bert.output.google_bert import GoogleBertMulticlassOutput


class TestOutputFormatters(unittest.TestCase):

    __current_dir = dirname(__file__)
    __input_samples_filepath = join(__current_dir, u"data/test_sample_3l.tsv.gz")
    __google_bert_output_filepath_sample = join(__current_dir, u"data/test_google_bert_output_3l.tsv")

    def test_google_bert_output_formatter(self):
        row_ids_provider = MultipleIDProvider()

        samples_reader = InputSampleReader.from_tsv(filepath=self.__input_samples_filepath,
                                                    row_ids_provider=row_ids_provider)

        output = GoogleBertMulticlassOutput(samples_reader=samples_reader,
                                            labels_scaler=TestThreeLabelScaler(),
                                            has_output_header=False)

        output.init_from_tsv(self.__google_bert_output_filepath_sample)

        df = output._DataFrame

        print df.columns
        print df

        # Check that all columns has string type.
        for c in df.columns:
            self.assert_(isinstance(c, str))


if __name__ == '__main__':
    unittest.main()
