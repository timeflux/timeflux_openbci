import numpy as np
import pandas as pd
from time import time
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
        channels (list): The channel labels.
            If not set, incrementing numbers will be used.
        **kwargs: The parameters specific for each board.
            These include: ``serial_port``, ``mac_address``, ``ip_address``,
            ``ip_port``, ``ip_protocol``.

    Example:
        .. literalinclude:: /../../timeflux_openbci/test/graphs/synthetic.yaml
           :language: yaml
    """

    def __init__(self, board, channels=None, **kwargs):
        try:
            board_id = getattr(BoardIds, board.upper() + '_BOARD').value
        except AttributeError:
            raise ValueError(f'Invalid board name: `{board}`') from None
        BoardShim.disable_board_logger()
        params = BrainFlowInputParams()
        for key, value in kwargs.items():
            setattr(params, key, value)
        if channels is not None:
            num_channels = BoardShim.get_num_rows(board_id)
            if not isinstance(channels, list) or len(channels) != num_channels:
                self.logger.warn(f'`channels` must contain {num_channels} elements')
                channels = None
        self._channels = channels
        self._meta = {'rate': BoardShim.get_sampling_rate(board_id)}
        self._timestamp_channel = BoardShim.get_timestamp_channel(board_id)
        self._offset = None
        self._board = BoardShim(board_id, params)
        self._board.prepare_session()
        self._board.start_stream()

    def update(self):
        data = self._board.get_board_data()
        if data is not None:
            if self._offset is None:
                self._offset = time() - data[self._timestamp_channel][-1]
            indices = pd.to_datetime(data[self._timestamp_channel] + self._offset, unit='s')
            self.o.set(data.T, indices, self._channels, self._meta)

    def terminate(self):
        self._board.stop_stream()
        self._board.release_session()
