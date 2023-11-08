from arekit.common.experiment.cv.splitters.base import CrossValidationSplitter
from arekit.common.folding.base import BaseDataFolding


class TwoClassCVFolding(BaseDataFolding):
    """ Performs folding onto a pair of data_types,
        i.e. two-class cv-folding algorithm
    """

    def __init__(self, supported_data_types, doc_ids_to_fold, cv_count, splitter):
        assert(isinstance(splitter, CrossValidationSplitter))

        if len(supported_data_types) > 2:
            raise NotImplementedError("Experiments with such amount of data-types are not supported!")

        super(TwoClassCVFolding, self).__init__(doc_ids_to_fold=doc_ids_to_fold,
                                                supported_data_types=supported_data_types,
                                                states_count=cv_count)

        self.__cv_count = cv_count
        self.__splitter = splitter

    # region Properties

    @property
    def CVCount(self):
        return self.__cv_count

    @property
    def Name(self):
        return "cv{0}".format(self.__cv_count)

    # endregion

    # region BaseFolding

    def fold_doc_ids_set(self):

        # Access to protected fields
        data_types = self._supported_data_types
        doc_ids = self._doc_ids_to_fold_set

        if len(data_types) == 1:
            # By default we provide the same output since
            # there is no need to perform splitting onto single part
            return {
                data_types[0]: list(doc_ids)
            }

        if self.__splitter is None:
            raise NotImplementedError("Splitter has not been intialized!")

        it = self.__splitter.items_to_cv_pairs(doc_ids=set(doc_ids),
                                               cv_count=self.__cv_count)

        for index, pair in enumerate(it):
            large, small = pair
            if index == self._state_index:
                return {
                    data_types[0]: large,
                    data_types[1]: small
                }

    # endregion
