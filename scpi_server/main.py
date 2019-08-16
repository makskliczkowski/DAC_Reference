from .SCPI_server import *


dac = dac()
dac.__init__()

sel = selectors.DefaultSelector()
sel.register(dac.s, selectors.EVENT_READ, data=None)

