from arekit.common.experiment.data.serializing import SerializationData
from arekit.common.experiment.engine.cv_based import ExperimentEngine
from arekit.contrib.networks.core.data_handling.data import HandledData


class NetworksExperimentInputSerializer(ExperimentEngine):

    def __init__(self, experiment, force_serialize, balance, skip_folder_if_exists):
        assert(isinstance(force_serialize, bool))
        assert(isinstance(balance, bool))

        super(NetworksExperimentInputSerializer, self).__init__(experiment)

        self.__force_serialize = force_serialize
        self.__skip_folder_if_exists = skip_folder_if_exists
        self.__balance = balance

    # region protected methods

    def _handle_iteration(self, it_index):
        assert(isinstance(self._experiment.DataIO, SerializationData))

        # Performing data serialization.
        if HandledData.check_files_existed(self._experiment) and not self.__force_serialize:
            return

        # Perform data serialization.
        HandledData.serialize_from_experiment(experiment=self._experiment,
                                              terms_per_context=self._experiment.DataIO.TermsPerContext,
                                              balance=self.__balance)

    def _before_running(self):
        self._logger.info("Perform annotation ...")
        for data_type in self._experiment.DocumentOperations.DataFolding.iter_supported_data_types():
            self._experiment.DataIO.Annotator.serialize_missed_collections(
                data_type=data_type,
                opin_ops=self._experiment.OpinionOperations,
                doc_ops=self._experiment.DocumentOperations)

    # endregion
