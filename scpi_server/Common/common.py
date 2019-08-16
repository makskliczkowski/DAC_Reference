'''
This file contains all mandatory and non-mandatory common commands that the device needs. It is provided with a short
description of every function.



'''


def clear_status():


def set_ese():


def reg_status:

def reg_status_clean():
def device_id():


def status():


def op_complete():
def is_op_complete():

def reset_tree():

def serv_enable():

def serv_query():

def status_byte():

def self_test():

def wait():
common={
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
