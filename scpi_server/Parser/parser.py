from typing import Dict
from ..SCPI_server import *


class CommandTree:

    # root functions-----------------------------------------------------------
    def root_sys(self):
        pass

    def root_stat(self):
        pass

    root_short = {
        "SYST": root_sys(),
        "STAT": root_stat()
    }

    # syst functions-----------------------------------------------------
    def syst_error(self):
        pass

    def syst_version(self):
        pass

    syst_short = {
        'ERR': syst_error(),
        'VERS?': syst_version()

    }

    # status functions--------------------------------------------
    def stat_oper(self):
        pass

    def stat_questionable(self):
        pass

    def stat_preset(self):
        pass

    stat_short = {
        'OPER': stat_oper(),
        'QUES': stat_questionable(),
        'PRES': stat_preset()
    }

    # operation functions -----------------------------------------------------
    def oper_event(self):
        pass

    def oper_condition(self):
        pass

    def oper_enable(self):
        pass

    def oper_is_enable(self):
        pass

    operartion_short = {
        'EVEN?': oper_event(),
        'COND?': oper_condition(),
        'ENAB': oper_enable(),
        'ENAB?': oper_is_enable()
    }

    # questionable functions------------------------------------------
    def quest_event(self):
        pass

    def quest_condition(self):
        pass

    def quest_enable(self):
        pass

    def quest_is_enable(self):
        pass

    questionable_short = {
        'EVEN?': quest_event(),
        'COND?': quest_condition(),
        'ENAB': quest_enable(),
        'ENAB?': quest_is_enable()
    }
