from timeflux_brainflow.nodes.driver import BrainFlow


class OpenBCI(BrainFlow):

    """OpenBCI driver.

    This plugin provides a unified interface for all OpenBCI boards.

    Attributes:
        o (Port): Default output, provides DataFrame.

    Args:
        board (string): The OpenBCI board type.
            Allowed values: ``synthetic``, ``cyton``, ``ganglion``, ``cyton_daisy``,
            ``ganglion_wifi``, ``cyton_wifi``, ``cyton_daisy_wifi``
        channels (list of string): The EEG channel labels.
            If not set, incrementing numbers will be used.
        gain (int): The amplifier gain. Only for Cyton-based boards.
            Possible values: 1, 2, 4, 6, 8, 12, 24.
            Default: 24.
        disable (list of int): Disable given channels. Only for Cyton-based boards.
            Default: None
        debug (boolean): Print debug messages.
        **kwargs: The parameters specific for each board.
            Allowed arguments: ``serial_port``, ``mac_address``, ``ip_address``,
            ``ip_port``, ``ip_protocol``.

    Example:
        .. literalinclude:: /../examples/synthetic.yaml
           :language: yaml
    """

    def __init__(
        self, board, channels=None, gain=24, disable=None, debug=False, **kwargs
    ):

        # Prepare command
        command = None
        if board.startswith("cyton"):
            gains = {1: 0, 2: 1, 4: 2, 6: 3, 8: 4, 12: 5, 24: 6}
            if "daisy" in board:
                chans = "12345678QWERTYUI"
            else:
                chans = "12345678"
            if not isinstance(disable, list):
                disable = []
            if gain in gains:
                command = ""
                for chan_num, chan_id in enumerate(chans, start=1):
                    enable = 1 if chan_num in disable else 0
                    command += f"x{chan_id}{enable}{gains[gain]}0110X"
            else:
                self.logger.warn("Invalid gain")

        # Initialize
        super().__init__(board, channels, command, debug, **kwargs)
