from typing import Dict


# root functions
def root_sys():
    pass


def root_stat():
    pass


# syst functions
def syst_error():
    pass


def syst_version():
    pass


# status functions
def stat_oper():
    pass


def stat_questionable():
    pass


def stat_preset():
    pass


root_short = {
    "SYST": root_sys(),
    "STAT": root_stat()
}

syst_short = {
    'ERR': syst_error(),
    'VERS?': syst_version()

}

stat_short = {
    'OPER': stat_oper(),
    'QUES': stat_questionable(),
    'PRES': stat_preset()
}


