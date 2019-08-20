from .SCPI_server import *
from .DAC import *
import sys

dac = DAC()
dac.__init__()


try:
    server_handle(dac)
except:
    pass

