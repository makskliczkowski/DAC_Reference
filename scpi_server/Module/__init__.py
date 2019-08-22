from DAC import DAC
import Lib
import _common
import _parse_msg
import _parser


@Lib.add_methods_from(_common, _parser, _parse_msg)
class Message(object):

    def __init__(self):
        self.dac = DAC()  # dac create

        self.response = ''  # This will be the response to send to the client
        self.message = ''  # Message that server got

        self.msg_parse_info()  # Create every information to provide msg parsing
        self.parse_dict()  # Create parse dictionary
        self.common_dict()  # create common dictionary

    def take_msg(self, data):
        self.message = data.decode("ascii")
        print('This is the received message from the server: ', self.message)
        self.msg_handle(self.message)
        self.message = ""

    def send_response(self):
        print('Sending response: ', self.response)
        x = self.response
        self.response = ''
        return x

    def __del__(self):
        self.dac.__del__()
        pass
