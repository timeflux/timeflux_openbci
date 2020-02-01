import pandas as pd
from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
from timeflux.core.node import Node

class OpenBCI(Node):

    """OpenBCI driver.

    This driver provides a unified interface for all OpenBCI boards.

    Attributes:
        o (Port): Default output, provides DataFrame.

    Args:
        board (string): The OpenBCI board type.
            Allowed values: ``synthetic``, ``cyton``, ``ganglion``, ``cyton_daisy``,
            ``ganglion_wifi``, ``cyton_wifi``, ``cyton_daisy_wifi``
        channels (list): The EEG channel labels.
            If not set, incrementing numbers will be used.
        debug (boolean): Print debug messages.
        **kwargs: The parameters specific for each board.
            These include: ``serial_port``, ``mac_address``, ``ip_address``,
            ``ip_port``, ``ip_protocol``.

    Example:
        .. literalinclude:: /../../timeflux_openbci/test/graphs/synthetic.yaml
           :language: yaml
    """

    def __init__(self, board, channels=None, debug=False, **kwargs):

        # Get board id
        try:
            board_id = getattr(BoardIds, board.upper() + '_BOARD').value
        except AttributeError:
            raise ValueError(f'Invalid board name: `{board}`') from None

        # Enable or disable debug mode
        if debug:
            BoardShim.enable_dev_board_logger()
        else:
            BoardShim.disable_board_logger()

        # Set board parameters
        params = BrainFlowInputParams()
        for key, value in kwargs.items():
            setattr(params, key, value)

        # Set channel labels
        self._channels = list(range(0, BoardShim.get_num_rows(board_id)))
        num_channel = BoardShim.get_package_num_channel(board_id)
        timestamp_channel = BoardShim.get_timestamp_channel(board_id)
        eeg_channels = BoardShim.get_eeg_channels(board_id)
        accel_channels = BoardShim.get_accel_channels(board_id)
        analog_channels = BoardShim.get_analog_channels(board_id)
        other_channels = BoardShim.get_other_channels(board_id)
        if channels is not None:
            num_eeg_channels = len(eeg_channels)
            if not isinstance(channels, list) or len(channels) != num_eeg_channels:
                self.logger.warn(f'`channels` must contain {num_eeg_channels} elements')
                channels = None
        if channels is None:
            channels = [f'eeg_{channel}' for channel in range(1, len(eeg_channels) + 1)]
        for channel, label in zip(eeg_channels, channels):
            self._channels[channel] = label
        self._channels[num_channel] = 'num'
        self._channels[timestamp_channel] = 'timestamp'
        for channel, axis in zip(accel_channels, ('x', 'y', 'z')):
            self._channels[channel] = f'accel_{axis}'
        for index, channel in enumerate(analog_channels, start=1):
            self._channels[channel] = f'analog_{index}'
        for index, channel in enumerate(other_channels, start=1):
            self._channels[channel] = f'other_{index}'

        # Set private variables
        self._timestamp_channel = timestamp_channel
        self._meta = {'rate': BoardShim.get_sampling_rate(board_id)}

        # Initialize board and start streaming
        self._board = BoardShim(board_id, params)
        self._board.prepare_session()
        self._board.start_stream()


    def update(self):
        data = self._board.get_board_data()
        if data is not None:
            indices = pd.to_datetime(data[self._timestamp_channel], unit='s')
            self.o.set(data.T, indices, self._channels, self._meta)


    def terminate(self):
        self._board.stop_stream()
        self._board.release_session()
