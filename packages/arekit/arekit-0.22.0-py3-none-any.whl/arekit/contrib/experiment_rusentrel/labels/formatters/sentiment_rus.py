from arekit.common.labels.str_fmt import StringLabelsFormatter
from arekit.contrib.experiment_rusentrel.labels.types import ExperimentNegativeLabel, ExperimentPositiveLabel, \
    ExperimentNeutralLabel


class RussianThreeScaleRussianLabelsFormatter(StringLabelsFormatter):
    """ NOTE:
        This class founds its application in language models, in NLI task.
        Therefore, this class is related to this experiment.
    """

    def __init__(self):

        stol = {'негативно': ExperimentNegativeLabel,
                'позитивно': ExperimentPositiveLabel,
                'нейтрально': ExperimentNeutralLabel}

        super(RussianThreeScaleRussianLabelsFormatter, self).__init__(stol=stol)