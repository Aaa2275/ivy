"""
Collection of Ivy neural network layers as stateful classes.
"""

# local
import ivy
from ivy.neural_net_stateful.module import Module


# Linear #
# -------#

class Linear(Module):

    def __init__(self, input_channels, output_channels, dev_str='cpu', v=None):
        """
        Linear layer, also referred to as dense or fully connected. The layer receives tensors with input_channels last
        dimension and returns a new tensor with output_channels last dimension, following matrix multiplication with the
        weight matrix and addition with the bias vector.

        :param input_channels: Number of input channels for the layer.
        :type input_channels: int
        :param output_channels: Number of output channels for the layer.
        :type output_channels: int
        :param dev_str: device on which to create the layer's variables 'cuda:0', 'cuda:1', 'cpu' etc. Default is cpu.
        :type dev_str: str, optional
        :param v: the variables for each of the linear layer, as a container, constructed internally by default.
        :type v: ivy container of variables, optional
        """
        self._input_channels = input_channels
        self._output_channels = output_channels
        Module.__init__(self, dev_str, v)

    def _create_variables(self, dev_str):
        """
        Create internal variables for the Linear layer
        """
        # ToDo: support other initialization mechanisms, via class constructor options
        # ToDo: tidy the construction of these variables, with helper functions
        wlim = (6 / (self._output_channels + self._input_channels)) ** 0.5
        w = ivy.variable(ivy.random_uniform(-wlim, wlim, (self._output_channels, self._input_channels),
                                            dev_str=dev_str))
        b = ivy.variable(ivy.zeros([self._output_channels], dev_str=dev_str))
        return {'w': w, 'b': b}

    def _forward(self, inputs):
        """
        Perform forward pass of the Linear layer.

        :param inputs: Inputs to process *[batch_shape, in]*.
        :type inputs: array
        :return: The outputs following the linear operation and bias addition *[batch_shape, out]*
        """
        return ivy.linear(inputs, self.v.w, self.v.b)


# Convolutions #
# -------------#

class Conv1D(Module):

    def __init__(self, input_channels, output_channels, filter_size, strides, padding, data_format='NWC', dilations=1,
                 dev_str='cpu', v=None):
        """
        1D convolutional layer.

        :param input_channels: Number of input channels for the layer.
        :type input_channels: int
        :param output_channels: Number of output channels for the layer.
        :type output_channels: int
        :param filter_size: Size of the convolutional filter.
        :type filter_size: int
        :param strides: The stride of the sliding window for each dimension of input.
        :type strides: int or sequence of ints
        :param padding: "SAME" or "VALID" indicating the algorithm, or list indicating the per-dimension paddings.
        :type padding: string or sequence of ints
        :param data_format: "NWC" or "NCW". Defaults to "NWC".
        :type data_format: string
        :param dilations: The dilation factor for each dimension of input.
        :type dilations: int or sequence of ints
        :param dev_str: device on which to create the layer's variables 'cuda:0', 'cuda:1', 'cpu' etc. Default is cpu.
        :type dev_str: str, optional
        :param v: the variables for each of the linear layer, as a container, constructed internally by default.
        :type v: ivy container of variables, optional
        """
        self._input_channels = input_channels
        self._output_channels = output_channels
        self._filter_size = filter_size
        self._strides = strides
        self._padding = padding
        self._data_format = data_format
        self._dilations = dilations
        Module.__init__(self, dev_str, v)

    def _create_variables(self, dev_str):
        """
        Create internal variables for the Conv1D layer
        """
        # ToDo: support other initialization mechanisms, via class constructor options
        # ToDo: tidy the construction of these variables, with helper functions
        wlim = (6 / (self._output_channels + self._input_channels)) ** 0.5
        w_shape = (self._filter_size, self._output_channels, self._input_channels) if self._data_format == 'NWC'\
            else (self._output_channels, self._input_channels, self._filter_size)
        w = ivy.variable(ivy.random_uniform(-wlim, wlim, w_shape, dev_str=dev_str))
        b = ivy.variable(ivy.zeros([1, 1, self._output_channels], dev_str=dev_str))
        return {'w': w, 'b': b}

    def _forward(self, inputs):
        """
        Perform forward pass of the Conv1D layer.

        :param inputs: Inputs to process *[batch_size,w,d_in]*
        :type inputs: array
        :return: The outputs following the conv1d layer *[batch_size,new_w,d_out]*
        """
        return ivy.conv1d(inputs, self.v.w, self._strides, self._padding, self._data_format, self._dilations) + self.v.b


class Conv1DTranspose(Module):

    def __init__(self, input_channels, output_channels, filter_size, strides, padding, output_shape=None,
                 data_format='NWC', dilations=1, dev_str='cpu', v=None):
        """
        1D transpose convolutional layer.

        :param input_channels: Number of input channels for the layer.
        :type input_channels: int
        :param output_channels: Number of output channels for the layer.
        :type output_channels: int
        :param filter_size: Size of the convolutional filter.
        :type filter_size: int
        :param strides: The stride of the sliding window for each dimension of input.
        :type strides: int or sequence of ints
        :param padding: "SAME" or "VALID" indicating the algorithm, or list indicating the per-dimension paddings.
        :type padding: string or sequence of ints
        :param output_shape: Shape of the output
        :type output_shape: sequence of ints, needed for TensorFlow
        :param data_format: "NWC" or "NCW". Defaults to "NWC".
        :type data_format: string
        :param dilations: The dilation factor for each dimension of input.
        :type dilations: int or sequence of ints
        :param dev_str: device on which to create the layer's variables 'cuda:0', 'cuda:1', 'cpu' etc. Default is cpu.
        :type dev_str: str, optional
        :param v: the variables for each of the linear layer, as a container, constructed internally by default.
        :type v: ivy container of variables, optional
        """
        self._input_channels = input_channels
        self._output_channels = output_channels
        self._filter_size = filter_size
        self._strides = strides
        self._padding = padding
        self._output_shape = output_shape
        self._data_format = data_format
        self._dilations = dilations
        Module.__init__(self, dev_str, v)

    def _create_variables(self, dev_str):
        """
        Create internal variables for the Conv1DTranspose layer
        """
        # ToDo: support other initialization mechanisms, via class constructor options
        # ToDo: tidy the construction of these variables, with helper functions
        wlim = (6 / (self._output_channels + self._input_channels)) ** 0.5
        w_shape = (self._filter_size, self._output_channels, self._input_channels) if self._data_format == 'NWC'\
            else (self._output_channels, self._input_channels, self._filter_size)
        w = ivy.variable(ivy.random_uniform(-wlim, wlim, w_shape, dev_str=dev_str))
        b = ivy.variable(ivy.zeros([1, 1, self._output_channels], dev_str=dev_str))
        return {'w': w, 'b': b}

    def _forward(self, inputs):
        """
        Perform forward pass of the Conv1DTranspose layer.

        :param inputs: Inputs to process *[batch_size,w,d_in]*
        :type inputs: array
        :return: The outputs following the conv1d layer *[batch_size,new_w,d_out]*
        """
        return ivy.conv1d_transpose(inputs, self.v.w, self._strides, self._padding, self._output_shape,
                                    self._data_format, self._dilations) + self.v.b


class Conv2D(Module):

    def __init__(self, input_channels, output_channels, filter_shape, strides, padding, data_format='NHWC', dilations=1,
                 dev_str='cpu', v=None):
        """
        2D convolutional layer.

        :param input_channels: Number of input channels for the layer.
        :type input_channels: int
        :param output_channels: Number of output channels for the layer.
        :type output_channels: int
        :param filter_shape: Shape of the convolutional filter.
        :type filter_shape: sequence of ints
        :param strides: The stride of the sliding window for each dimension of input.
        :type strides: int or sequence of ints
        :param padding: "SAME" or "VALID" indicating the algorithm, or list indicating the per-dimension paddings.
        :type padding: string or sequence of ints
        :param data_format: "NHWC" or "NCHW". Defaults to "NHWC".
        :type data_format: string
        :param dilations: The dilation factor for each dimension of input.
        :type dilations: int or sequence of ints
        :param dev_str: device on which to create the layer's variables 'cuda:0', 'cuda:1', 'cpu' etc. Default is cpu.
        :type dev_str: str, optional
        :param v: the variables for each of the linear layer, as a container, constructed internally by default.
        :type v: ivy container of variables, optional
        """
        self._input_channels = input_channels
        self._output_channels = output_channels
        self._filter_shape = filter_shape
        self._strides = strides
        self._padding = padding
        self._data_format = data_format
        self._dilations = dilations
        Module.__init__(self, dev_str, v)

    def _create_variables(self, dev_str):
        """
        Create internal variables for the Conv2D layer
        """
        # ToDo: support other initialization mechanisms, via class constructor options
        # ToDo: tidy the construction of these variables, with helper functions
        wlim = (6 / (self._output_channels + self._input_channels)) ** 0.5
        w_shape = self._filter_shape + [self._output_channels, self._input_channels] if self._data_format == 'NHWC'\
            else [self._output_channels, self._input_channels] + self._filter_shape
        w = ivy.variable(ivy.random_uniform(-wlim, wlim, w_shape, dev_str=dev_str))
        b = ivy.variable(ivy.zeros([1, 1, 1, self._output_channels], dev_str=dev_str))
        return {'w': w, 'b': b}

    def _forward(self, inputs):
        """
        Perform forward pass of the Conv2D layer.

        :param inputs: Inputs to process *[batch_size,h,w,d_in]*.
        :type inputs: array
        :return: The outputs following the conv1d layer *[batch_size,new_h,new_w,d_out]*
        """
        return ivy.conv2d(inputs, self.v.w, self._strides, self._padding, self._data_format, self._dilations) + self.v.b


class Conv2DTranspose(Module):

    def __init__(self, input_channels, output_channels, filter_shape, strides, padding, output_shape=None,
                 data_format='NHWC', dilations=1, dev_str='cpu', v=None):
        """
        2D convolutional transpose layer.

        :param input_channels: Number of input channels for the layer.
        :type input_channels: int
        :param output_channels: Number of output channels for the layer.
        :type output_channels: int
        :param filter_shape: Shape of the convolutional filter.
        :type filter_shape: sequence of ints
        :param strides: The stride of the sliding window for each dimension of input.
        :type strides: int or sequence of ints
        :param padding: "SAME" or "VALID" indicating the algorithm, or list indicating the per-dimension paddings.
        :type padding: string or sequence of ints
        :param output_shape: Shape of the output
        :type output_shape: sequence of ints, needed for TensorFlow
        :param data_format: "NHWC" or "NCHW". Defaults to "NHWC".
        :type data_format: string
        :param dilations: The dilation factor for each dimension of input.
        :type dilations: int or sequence of ints
        :param dev_str: device on which to create the layer's variables 'cuda:0', 'cuda:1', 'cpu' etc. Default is cpu.
        :type dev_str: str, optional
        :param v: the variables for each of the linear layer, as a container, constructed internally by default.
        :type v: ivy container of variables, optional
        """
        self._input_channels = input_channels
        self._output_channels = output_channels
        self._filter_shape = filter_shape
        self._strides = strides
        self._padding = padding
        self._output_shape = output_shape
        self._data_format = data_format
        self._dilations = dilations
        Module.__init__(self, dev_str, v)

    def _create_variables(self, dev_str):
        """
        Create internal variables for the Conv2DTranspose layer
        """
        # ToDo: support other initialization mechanisms, via class constructor options
        # ToDo: tidy the construction of these variables, with helper functions
        wlim = (6 / (self._output_channels + self._input_channels)) ** 0.5
        w_shape = self._filter_shape + [self._output_channels, self._input_channels] if self._data_format == 'NHWC'\
            else [self._output_channels, self._input_channels] + self._filter_shape
        w = ivy.variable(ivy.random_uniform(-wlim, wlim, w_shape, dev_str=dev_str))
        b = ivy.variable(ivy.zeros([1, 1, 1, self._output_channels], dev_str=dev_str))
        return {'w': w, 'b': b}

    def _forward(self, inputs):
        """
        Perform forward pass of the Conv2DTranspose layer.

        :param inputs: Inputs to process *[batch_size,h,w,d_in]*.
        :type inputs: array
        :return: The outputs following the conv1d layer *[batch_size,new_h,new_w,d_out]*
        """
        return ivy.conv2d_transpose(inputs, self.v.w, self._strides, self._padding, self._output_shape,
                                    self._data_format, self._dilations) + self.v.b


# LSTM #
# -----#

class LSTM(Module):

    def __init__(self, input_channels, output_channels, num_layers=1, return_sequence=True, return_state=True,
                 dev_str='cpu', v=None):
        """
        LSTM layer, which is a set of stacked lstm cells.

        :param input_channels: Number of input channels for the layer
        :type input_channels: int
        :param output_channels: Number of output channels for the layer
        :type output_channels: int
        :param num_layers: Number of lstm cells in the lstm layer, default is 1.
        :type num_layers: int, optional
        :param return_sequence: Whether or not to return the entire output sequence, or just the latest timestep.
                                Default is True.
        :type return_sequence: bool, optional
        :param return_state: Whether or not to return the latest hidden and cell states. Default is True.
        :type return_state: bool, optional
        :param dev_str: device on which to create the layer's variables 'cuda:0', 'cuda:1', 'cpu' etc. Default is cpu.
        :type dev_str: str, optional
        :param v: the variables for each of the lstm cells, as a container, constructed internally by default.
        :type v: ivy container of parameter arrays, optional
        """
        self._input_channels = input_channels
        self._output_channels = output_channels
        self._num_layers = num_layers
        self._return_sequence = return_sequence
        self._return_state = return_state
        Module.__init__(self, dev_str, v)

    # Public #

    def get_initial_state(self, batch_shape):
        """
        Get the initial state of the hidden and cell states, if not provided explicitly
        """
        batch_shape = list(batch_shape)
        return ([ivy.zeros((batch_shape + [self._output_channels])) for i in range(self._num_layers)],
                [ivy.zeros((batch_shape + [self._output_channels])) for i in range(self._num_layers)])

    # Overridden

    def _create_variables(self, dev_str):
        """
        Create internal variables for the LSTM layer
        """
        # ToDo: support other initialization mechanisms, via class constructor options
        # ToDo: tidy the construction of these variables, with helper functions
        wlim = (6 / (self._output_channels + self._input_channels)) ** 0.5
        input_weights = dict(zip(
            ['layer_' + str(i) for i in range(self._num_layers)],
            [{'w': ivy.variable(
                ivy.random_uniform(-wlim, wlim, (self._input_channels if i == 0 else self._output_channels,
                                                 4 * self._output_channels), dev_str=dev_str))}
                for i in range(self._num_layers)]))
        wlim = (6 / (self._output_channels + self._output_channels)) ** 0.5
        recurrent_weights = dict(zip(
            ['layer_' + str(i) for i in range(self._num_layers)],
            [{'w': ivy.variable(
                ivy.random_uniform(-wlim, wlim, (self._output_channels, 4 * self._output_channels), dev_str=dev_str))}
             for i in range(self._num_layers)]))
        return {'input': input_weights, 'recurrent': recurrent_weights}

    def _forward(self, inputs, initial_state=None):
        """
        Perform forward pass of the LSTM layer.

        :param inputs: Inputs to process *[batch_shape, t, in]*.
        :type inputs: array
        :param initial_state: 2-tuple of lists of the hidden states h and c for each layer, each of dimension *[batch_shape,out]*.
                        Created internally if None.
        :type initial_state: tuple of list of arrays, optional
        :return: The outputs of the final lstm layer *[batch_shape, t, out]* and the hidden state tuple of lists,
                each of dimension *[batch_shape, out]*
        """
        if initial_state is None:
            initial_state = self.get_initial_state(inputs.shape[:-2])
        h_n_list = list()
        c_n_list = list()
        h_t = inputs
        for h_0, c_0, (_, lstm_input_var), (_, lstm_recurrent_var) in zip(
                initial_state[0], initial_state[1], self.v.input.items(), self.v.recurrent.items()):
            h_t, c_n = ivy.lstm_update(h_t, h_0, c_0, lstm_input_var.w, lstm_recurrent_var.w)
            h_n_list.append(h_t[..., -1, :])
            c_n_list.append(c_n)
        if not self._return_sequence:
            h_t = h_t[..., -1, :]
        if not self._return_state:
            return h_t
        return h_t, (h_n_list, c_n_list)
