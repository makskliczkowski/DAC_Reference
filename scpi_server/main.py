import SCPI_server
from DAC import *
import sys

dac = DAC()

try:
    server_handle(dac)
except:
    pass

