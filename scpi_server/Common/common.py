'''
This file contains all mandatory and non-mandatory common commands that the device needs. It is provided with a short
description of every function.



'''

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