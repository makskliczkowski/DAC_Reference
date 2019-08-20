from .Module.__init__ import *
from .SCPI_server import *
import sys

Message = Message()

try:
    server_handle(Message)
except:
    pass

