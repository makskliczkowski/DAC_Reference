from scpi_server.SCPI_server import server_handle
from . import SCPI_server
from . import DAC
import sys

dac = DAC()

try:
    server_handle(dac)
except:
    pass

