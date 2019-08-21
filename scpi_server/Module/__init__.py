from DAC import DAC
import Lib
import _common
import _parse_msg
import _parser


@Lib.add_methods_from(_common, _parser, _parse_msg)
class Message(object):

    def __init__(self):
        self.dac = DAC()  # dac create

        self.msg_parse_info()  # Create every information to provide msg parsing
        self.parse_dict()  # Create parse dictionary
        self.common_dict()  # create common dictionary

        self.response = None  # This will be the response to send to the client
        self.message = ""  # Message that server got

    def take_msg(self, data):
        self.message = data.decode("ascii")

    def send_response(self):
        return self.response

    def __del__(self):
        self.dac.__del__()
        pass
