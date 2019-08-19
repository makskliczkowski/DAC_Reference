'''
This file contains all mandatory and non-mandatory common commands that the device needs. It is provided with a short
description of every function.



'''
class Commons:

    def clear_status(self):
        pass


    def set_ese(self):
        pass


    def reg_status(self):
        pass


    def reg_status_clean(self):
        pass


    def device_id(self):
        pass


    def status(self):
        pass


    def op_complete(self):
        pass


    def is_op_complete(self):
        pass


    def reset_tree(self):
        pass


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


    common = {
        '*CLS': clear_status(),
        '*ESE': set_ese(),
        '*ESE?': reg_status(),
        '*ESR?': reg_status_clean(),
        '*IDN?': device_id(),
        '*IST?': status(),
        '*OPC': op_complete(),
        '*OPC?': is_op_complete(),
        '*RST': reset_tree(),
        '*SRE': serv_enable(),
        '*SRE?': serv_query(),
        '*STB?': status_byte(),
        '*TST?': self_test(),
        '*WAI': wait()
    }
