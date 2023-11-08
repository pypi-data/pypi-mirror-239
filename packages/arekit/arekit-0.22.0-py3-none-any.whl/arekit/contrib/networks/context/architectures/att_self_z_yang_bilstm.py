from arekit.contrib.networks.attention.architectures.self_z_yang import self_attention_by_z_yang
from arekit.contrib.networks.context.architectures.base.att_self_bilstm_base import AttentionSelfBiLSTMBase
from arekit.contrib.networks.context.configurations.att_self_z_yang_bilstm import AttentionSelfZYangBiLSTMConfig


class AttentionSelfZYangBiLSTM(AttentionSelfBiLSTMBase):

    def get_attention_output_with_alphas(self, rnn_outputs):
        assert(isinstance(self.Config, AttentionSelfZYangBiLSTMConfig))
        return self_attention_by_z_yang(inputs=rnn_outputs,
                                        attention_size=self.Config.AttentionSize,
                                        return_alphas=True)
