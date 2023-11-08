from arekit.common.folding.base import BaseDataFolding


class FixedFolding(BaseDataFolding):

    def __init__(self, doc_to_dtype_func, doc_ids_to_fold, supported_data_types, dup_count=1):
        assert(isinstance(dup_count, int) and dup_count > 0)
        assert(callable(doc_to_dtype_func))

        super(FixedFolding, self).__init__(doc_ids_to_fold=doc_ids_to_fold,
                                           supported_data_types=supported_data_types,
                                           states_count=dup_count)

        self.__doc_to_dtype_func = doc_to_dtype_func

    @property
    def Name(self):
        return "fixed"

    def fold_doc_ids_set(self):

        folded = {}
        for d_type in self._supported_data_types:
            folded[d_type] = []

        for doc_id in self._doc_ids_to_fold_set:
            d_type = self.__doc_to_dtype_func(doc_id)
            folded[d_type].append(doc_id)

        return folded
