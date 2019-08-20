from DAC import DAC


class Message(object):
    from ._common import *
    from ._parse_msg import *
    from ._parser import *

    def __init__(self):
        self.dac = DAC()  # dac create

        self.msg_parse_info()  # Create every information to provide msg parsing
        self.parse_dict()  # Create parse dictionary
        self.common_dict() # create common dictionary

        self.response = None  # This will be the response to send to the client
        self.message = ""  # Message that server got

    def take_msg(self, data):
        self.message = data.decode("ascii")

    def send_response(self):
        return self.response

    def __del__(self):
        self.dac.__del__()
        pass
