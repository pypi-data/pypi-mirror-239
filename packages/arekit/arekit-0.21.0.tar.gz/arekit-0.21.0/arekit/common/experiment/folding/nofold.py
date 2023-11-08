from arekit.common.experiment.folding.base import BaseExperimentDataFolding


class NoFolding(BaseExperimentDataFolding):
    """ The case of absent folding in experiment.
    """

    def __init__(self, doc_ids_to_fold, supported_data_types):
        if len(supported_data_types) > 1:
            raise NotImplementedError(u"Experiments with such amount of data-types are not supported!")

        super(NoFolding, self).__init__(doc_ids_to_fold=doc_ids_to_fold,
                                        supported_data_types=supported_data_types)

    @property
    def Name(self):
        return u"na"

    def fold_doc_ids_set(self):
        return {
            self._supported_data_types[0]: list(self._doc_ids_to_fold_set)
        }

    def get_current_state(self):
        """ Returns in order to be compatible with cv-based experiment format.
        """
        return u"0"
