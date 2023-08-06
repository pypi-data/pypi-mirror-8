"""A virtual serial port data source."""
from __future__ import absolute_import

import logging

from .base import BytestreamDataSource, DataSourceError

LOG = logging.getLogger(__name__)

try:
    import serial
except ImportError:
    LOG.debug("serial library not installed, can't use serial interface")
    serial = None


class SerialDataSource(BytestreamDataSource):
    """A data source reading from a serial port, which could be implemented
    with a USB to Serial or Bluetooth adapter.
    """
    DEFAULT_PORT = "/dev/ttyUSB0"
    DEFAULT_BAUDRATE = 230400

    def __init__(self, port=None, baudrate=None, **kwargs):
        """Initialize a connection to the serial device.

        Kwargs:
            port - optionally override the default virtual COM port
            baudrate - optionally override the default baudrate

        Raises:
            DataSourceError if the serial device cannot be opened.
        """
        super(SerialDataSource, self).__init__(**kwargs)
        port = port or self.DEFAULT_PORT
        baudrate = baudrate or self.DEFAULT_BAUDRATE

        if serial is None:
            raise DataSourceError("pyserial library is not available")

        try:
            self.device = serial.Serial(port, baudrate, rtscts=True)
        except (OSError, serial.SerialException) as e:
            raise DataSourceError("Unable to open serial device at port "
                    "%s: %s" % (port, e))
        else:
            LOG.debug("Opened serial device at %s", port)

    def read(self):
        return self.device.read()
