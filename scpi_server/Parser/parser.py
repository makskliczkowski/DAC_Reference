from typing import Dict


# root functions-----------------------------------------------------------
def root_sys():
    pass


def root_stat():
    pass


root_short = {
    "SYST": root_sys(),
    "STAT": root_stat()
}


# syst functions-----------------------------------------------------
def syst_error():
    pass


def syst_version():
    pass


syst_short = {
    'ERR': syst_error(),
    'VERS?': syst_version()

}


# status functions--------------------------------------------
def stat_oper():
    pass


def stat_questionable():
    pass


def stat_preset():
    pass


stat_short = {
    'OPER': stat_oper(),
    'QUES': stat_questionable(),
    'PRES': stat_preset()
}


# operation functions -----------------------------------------------------
def oper_event():
    pass


def oper_condition():
    pass


def oper_enable():
    pass


def oper_is_enable():
    pass


operartion_short = {
    'EVEN?': oper_event(),
    'COND?': oper_condition(),
    'ENAB': oper_enable(),
    'ENAB?': oper_is_enable()
}


# questionable functions------------------------------------------
def quest_event():
    pass


def quest_condition():
    pass


def quest_enable():
    pass


def quest_is_enable():
    pass


questionable_short = {
    'EVEN?': quest_event(),
    'COND?': quest_condition(),
    'ENAB': quest_enable(),
    'ENAB?': quest_is_enable()
}
