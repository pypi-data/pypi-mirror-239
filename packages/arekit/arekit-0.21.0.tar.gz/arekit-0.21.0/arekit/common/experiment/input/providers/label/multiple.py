from arekit.common.experiment.input.providers.label.base import LabelProvider


class MultipleLabelProvider(LabelProvider):

    def __init__(self, label_scaler):
        super(MultipleLabelProvider, self).__init__(label_scaler=label_scaler)

    def calculate_output_uint_label(self, expected_uint_label, etalon_uint_label):
        return expected_uint_label

    @property
    def OutputLabelsUint(self):
        return map(lambda label: self.LabelScaler.label_to_uint(label), self.SupportedLabels)

