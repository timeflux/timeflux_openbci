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
        channels (list): The EEG channel labels.
            If not set, incrementing numbers will be used.
        debug (boolean): Print debug messages.
        **kwargs: The parameters specific for each board.
            Allowed arguments: ``serial_port``, ``mac_address``, ``ip_address``,
            ``ip_port``, ``ip_protocol``.

    Example:
        .. literalinclude:: /../../timeflux_openbci/test/graphs/synthetic.yaml
           :language: yaml
    """
