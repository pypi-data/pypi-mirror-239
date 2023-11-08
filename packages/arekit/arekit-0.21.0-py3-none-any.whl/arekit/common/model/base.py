from arekit.common.experiment.data_type import DataType
from arekit.common.model.model_io import BaseModelIO


class BaseModel(object):
    """
    Base Model
    """

    def __init__(self, io):
        assert(isinstance(io, BaseModelIO))
        self.__io = io

    @property
    def IO(self):
        return self.__io

    def run_training(self, model_params, seed):
        raise NotImplementedError()

    def predict(self, data_type=DataType.Test):
        raise NotImplementedError()
