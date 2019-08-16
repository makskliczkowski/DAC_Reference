'''
This file contains all mandatory and non-mandatory common commands that the device needs. It is provided with a short
description of every function.



'''


def clear_status():
    pass

def set_ese():
    pass

def reg_status:
    pass

def reg_status_clean():
    pass

def device_id():
    pass

def status():
    pass

def op_complete():
    pass
def is_op_complete():
    pass
def reset_tree():
    pass
def serv_enable():
    pass
def serv_query():
    pass
def status_byte():
    pass
def self_test():
    pass
def wait():
    pass

common = {
    '*CLS' : clear_status(),
    '*ESE' : set_ese(),
    '*ESE?' : reg_status(),
    '*ESR?' : reg_status_clean(),
    '*IDN?' : device_id(),
    '*IST?' : status(),
    '*OPC' : op_complete(),
    '*OPC?' : is_op_complete(),
    '*RST' : reset_tree(),
    '*SRE' : serv_enable(),
    '*SRE?' : serv_query(),
    '*STB?' : status_byte(),
    '*TST?' : self_test(),
    '*WAI' : wait()
}
