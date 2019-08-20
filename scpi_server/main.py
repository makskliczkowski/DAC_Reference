import SCPI_server
import DAC
import sys

dac = DAC()
dac.__init__()


try:
    server_handle(dac)
except:
    pass

