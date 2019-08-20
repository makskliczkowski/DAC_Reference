'''
This file contains all mandatory and non-mandatory common commands that the device needs. It is provided with a short
description of every function.



'''
from scpi_server.DAC import DAC


class Commons(DAC):
    def __init__(self):
        self.common = {
            '*CLS': self.clear_status(),
            '*ESE': self.set_ese(),
            '*ESE?': self.reg_status(),
            '*ESR?': self.reg_status_clean(),
            '*IDN?': self.device_id(),
            '*IST?': self.status(),
            '*OPC': self.op_complete(),
            '*OPC?': self.is_op_complete(),
            '*RST': self.reset_tree(),
            '*SRE': self.serv_enable(),
            '*SRE?': self.serv_query(),
            '*STB?': self.status_byte(),
            '*TST?': self.self_test(),
            '*WAI': self.wait()
        }

    def clear_status(self):
        pass

    def set_ese(self):
        pass

    def reg_status(self):
        pass

    def reg_status_clean(self):
        pass

    def device_id(self):
        self.ParseMessage.response = "The device is created for the request of precise voltage controlling using " \
                                     "boards with DAC chips. Implementation project for MPQ by Maksymilian " \
                                     "Kliczkowski\n "

    def status(self):
        pass

    def op_complete(self):
        pass

    def is_op_complete(self):
        pass

    def reset_tree(self):
        self.ParseMessage.clear_path()

    def serv_enable(self):
        pass

    def serv_query(self):
        pass

    def status_byte(self):
        pass

    def self_test(self):
        pass

    def wait(self):
        pass
