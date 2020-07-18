Timeflux OpenBCI plugin
=======================

This plugin provides a unified interface for all `OpenBCI <https://openbci.com>`__ boards.

Installation
------------

First, make sure that `Timeflux <https://github.com/timeflux/timeflux>`__ is installed.

You can then install this plugin in the `timeflux` environment:

::

    $ conda activate timeflux
    $ pip install timeflux_openbci

Troubleshooting
---------------

If the data looks choppy, it is very likely because of a latency issue with the FTDI driver. Hopefully, there is a fix both for `Windows <https://docs.openbci.com/docs/10Troubleshooting/OpenBCI_on_Windows>`__ and `MacOS <https://docs.openbci.com/docs/10Troubleshooting/FTDI_Fix_Mac>`__.