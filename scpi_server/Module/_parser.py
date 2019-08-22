import copy
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI
import Lib

__methods__ = []
register_method = Lib.register_method(__methods__)


@register_method
def parse_dict(self):
    # CURRENT DICTIONARY
    self.curr_dic_short = None
    self.curr_dic_long = None
    # !!!!!!!!!!!!!!! THIRD FLOOR !!!!!!!!!!!!!!!!!!!!!!!
    self.volt_short = {
        'RAW': self.volt_raw,
        'NORM': self.volt_norm
    }
    self.volt_long = {
        'RAW': self.volt_raw,
        'NORM': self.volt_norm
    }
    # !!!!!!!!!!!!!!!SECOND FLOOR !!!!!!!!!!!!!!!!!!!!!!!
    # SYST/CONTROL @@@@@@
    self.control_short = {
        'CLO': self.contr_clock,
        'CLO?': self.contr_what_clock,
        'RES': self.contr_res_button,
        'LDAC': self.conrt_ldac_button,
        'VOLT': self.contr_volt
    }
    self.control_long = {
        'CLOCK': self.contr_clock,
        'CLOCK?': self.contr_what_clock,
        'RESET': self.contr_res_button,
        'LDAC': self.conrt_ldac_button,
        'VOLTAGE': self.contr_volt
    }

    # STATUS/OPERATION @@@@@@
    self.operartion_short = {
        'EVEN?': self.oper_event,
        'COND?': self.oper_condition,
        'ENAB': self.oper_enable,
        'ENAB?': self.oper_is_enabled
    }
    self.operartion_long = {
        'EVENT?': self.oper_event,
        'CONDITION?': self.oper_condition,
        'ENABLE': self.oper_enable,
        'ENABLE?': self.oper_is_enabled
    }
    # STATUS/QUESTIONABLE @@@@@@
    self.questionable_short = {
        'EVEN?': self.quest_event,
        'COND?': self.quest_condition,
        'ENAB': self.quest_enable,
        'ENAB?': self.quest_is_enabled
    }
    self.questionable_long = {
        'EVENT?': self.quest_event,
        'CONDITION?': self.quest_condition,
        'ENABLE': self.quest_enable,
        'ENABLE?': self.quest_is_enabled
    }

    # !!!!!!!!!!!!!!!FIRST FLOOR !!!!!!!!!!!!!!!!!!!!!!!!
    # !!SYSTEM @@@@@@
    self.syst_short = {
        'ERR': self.syst_error,
        'VERS?': self.syst_version,
        'ADDR': self.syst_addr,  # sets DAC address
        'ADDR?': self.syst_what_addr,  # what DAC address we have?
        'BOAR': self.syst_board,  # DIRECTLY SETS BOARD NUMBER
        'BOAR?': self.syst_what_board,  # What is the board number
        'DAC': self.syst_dac,  # Directly sets dac number on the board
        'DAC?': self.syst_what_dac,  # What is the DAC number
        'CONT': self.syst_control,
        'ON': self.syst_on,
        'OFF': self.syst_off
    }
    self.syst_long = {
        'ERROR': self.syst_error,
        'VERSION?': self.syst_version,
        'ADDRESS': self.syst_addr,  # sets DAC address
        'ADDRESS?': self.syst_what_addr,  # what DAC address we have?
        'BOARD': self.syst_board,  # DIRECTLY SETS BOARD NUMBER
        'BOARD?': self.syst_what_board,  # What is the board number
        'DAC': self.syst_dac,  # Directly sets dac number on the board
        'DAC?': self.syst_what_dac,  # What is the DAC number
        'CONTROL': self.syst_control,
        'ON': self.syst_on,
        'OFF': self.syst_off
    }
    # !!STATUS @@@@@@@
    self.stat_short = {
        'OPER': self.stat_oper,
        'QUES': self.stat_questionable,
        'PRES': self.stat_preset
    }
    self.stat_long = {
        'OPERATION': self.stat_oper,
        'QUESTIONABLE': self.stat_questionable,
        'PRESET': self.stat_preset
    }
    # !!ROOT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    self.root_short = {
        "SYST": self.root_sys,
        "STAT": self.root_stat
    }
    self.root_long = {
        "SYSTEM": self.root_sys,
        "STATUS": self.root_stat
    }

    self.curr_dic_short = self.root_short
    self.curr_dic_long = self.root_long

# normal functions


# root functions-----------------------------------------------------------
# @staticmethod
@register_method
def root_sys(self):
    self.curr_dic_short = self.syst_short
    self.curr_dic_long = self.syst_long


# @staticmethod
@register_method
def root_stat(self):
    self.curr_dic_short = self.stat_short
    self.curr_dic_long = self.stat_long


# !!!!!!!!!!!!!!!!!!!!!!! ROOT LEVEL !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# system functions-----------------------------------------------------
@register_method
def syst_error(self):
    pass


@register_method
def syst_version(self):
    pass


@register_method
def syst_addr(self):  # function sets dac address - binary
    temp = self.request_val
    print("debug1")
    check0 = bool(int(temp[0]) == 0 or int(temp[0]) == 1)
    check1 = bool(int(temp[1]) == 0 or int(temp[1]) == 1)
    check2 = bool(int(temp[2]) == 0 or int(temp[2]) == 1)
    check3 = bool(int(temp[3]) == 0 or int(temp[3]) == 1)
    check4 = bool(int(temp[4]) == 0 or int(temp[4]) == 1)
    if check0 and check1 and check2 and check3 and check4:
        self.dac.dac_address = temp
        print("debug2", self.dac.dacAddress)
        GPIO.setup("P9_15", int(self.dac.dac_address[0]))  # P0
        GPIO.setup("P9_11", int(self.dac.dac_address[1]))  # P1
        GPIO.setup("P9_12", int(self.dac.dac_address[2]))  # P2
        GPIO.setup("P9_13", int(self.dac.dac_address[3]))  # P3
        GPIO.setup("P9_14", int(self.dac.dac_address[4]))  # P4
        self.dac.dac_address = temp
        temp_str = ''
        temp_str = temp_str.join(self.dac.dac_address)
        self.response += "The address is: [" + temp_str + "]\n"
    else:
        self.response += 'SOMETHING WENT WRONG, WRONG ADDRESS' + str(self.request_value)


@register_method
def syst_what_addr(self):
    self.response += "The address is: " + str(self.dac.dac_address)


@register_method
def syst_board(self):
    temp_str = ''
    temp_str = temp_str.join(self.request_val)
    board = int(temp_str)
    if board == 0:
        self.dac.dac_address[2] = 0
        self.dac.dac_address[3] = 0
        self.dac.dac_address[4] = 0
    elif board == 1:
        self.dac.dac_address[2] = 0
        self.dac.dac_address[3] = 0
        self.dac.dac_address[4] = 1
    elif board == 2:
        self.dac.dac_address[2] = 0
        self.dac.dac_address[3] = 1
        self.dac.dac_address[4] = 0
    elif board == 3:
        self.dac.dac_address[2] = 0
        self.dac.dac_address[3] = 1
        self.dac.dac_address[4] = 1
    else:
        print("WRONG NUMBER, SETTING 0")
        self.dac.dac_address[2] = 0
        self.dac.dac_address[3] = 0
        self.dac.dac_address[4] = 0

    GPIO.output("P9_12", int(self.dac.dac_address[2]))
    GPIO.output("P9_13", int(self.dac.dac_address[3]))
    GPIO.output("P9_14", int(self.dac.dac_address[4]))
    self.response += "The board number is: [" + str(board) + "]"


@register_method
def syst_what_board(self):
    temp_list = self.dac.dac_address[2:]
    temp_str = ''
    for i in temp_list:
        temp_str = temp_str + str(i)
    board = int(temp_str, 2)
    self.response += "The board number is: [" + str(board) + "]"


@register_method
def syst_dac(self):
    temp_str = ''
    temp_str = temp_str.join(self.request_val)
    board = int(temp_str)
    if board == 0:
        self.dac.dac_address[0] = 0
        self.dac.dac_address[1] = 0
    elif board == 1:
        self.dac.dac_address[0] = 0
        self.dac.dac_address[1] = 1
    elif board == 2:
        self.dac.dac_address[0] = 1
        self.dac.dac_address[1] = 0
    elif board == 3:
        self.dac.dac_address[0] = 1
        self.dac.dac_address[1] = 1
    else:
        print("WRONG NUMBER, SETTING 0")
        self.dac.dac_address[0] = 0
        self.dac.dac_address[1] = 0

    GPIO.output("P9_15", int(self.dac.dac_address[0]))
    GPIO.output("P9_11", int(self.dac.dac_address[1]))
    self.response += "The DAC number is: [" + str(board) + "]"


@register_method
def syst_what_dac(self):
    temp_list = self.dac.dac_address[0:2]
    temp_str = ''
    for i in temp_list:
        temp_str = temp_str + str(i)
    board = int(temp_str, 2)
    self.response += "The DAC number is: [" + str(board) + "]"


# @staticmethod
@register_method
def syst_control(self):
    self.curr_dic_short = self.control_short
    self.curr_dic_long = self.control_long


@register_method
def syst_on(self):
    self.dac.__init__()


@register_method
def syst_off(self):
    self.dac.__del__()


# status functions--------------------------------------------
@register_method
def stat_oper(self):
    pass


@register_method
def stat_questionable(self):
    pass


@register_method
def stat_preset(self):
    pass


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SECOND LEVEL !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# control functions
# @staticmethod
@register_method
def contr_volt(self):
    self.curr_dic_short = self.volt_short
    self.curr_dic_long = self.volt_long


@register_method
def conrt_ldac_button(self):
    temp_str = ''
    temp_str = temp_str.join(self.request_val)
    temp = bool(temp_str)
    self.dac.ldac = temp
    GPIO.output("P8_17", self.dac.ldac)
    self.response += "LDAC is set to: [" + str(temp) + "]"


@register_method
def contr_res_button(self):
    temp_str = ''
    temp_str = temp_str.join(self.request_val)
    temp = bool(temp_str)
    self.dac.reset = temp
    GPIO.output("P8_18", self.dac.reset)
    GPIO.output("P8_18", 0)  # returns it back to 0
    if temp == 1:
        self.response += "Reset correct"
    else:
        self.response += "Reset incorrect"


@register_method
def contr_what_clock(self):
    self.response += "CLOCK is set to: [" + str(self.dac.clock) + "]"


@register_method
def contr_clock(self):
    temp_str = ''
    temp_str = temp_str.join(self.request_val)
    clock = int(temp_str)
    if self.dac.MIN_CLOCK <= clock <= self.dac.MAX_CLOCK:
        self.dac.spi.msh(clock)
        self.dac.clock = clock
        self.response += "CLOCK is now set to: [" + str(self.dac.clock) + "]"
    else:
        self.response += "Something's wrong. CLOCK is set to: [" + str(self.dac.clock) + "}"


# operation functions -----------------------------------------------------
@register_method
def oper_event(self):
    pass


@register_method
def oper_condition(self):
    pass


@register_method
def oper_enable(self):
    pass


@register_method
def oper_is_enabled(self):
    pass


# questionable functions------------------------------------------
@register_method
def quest_event(self):
    pass


@register_method
def quest_condition(self):
    pass


@register_method
def quest_enable(self):
    pass


@register_method
def quest_is_enabled(self):
    pass


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! THIRD LEVEL !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# voltage
@register_method
def volt_raw(self):
    temp_str = ''
    temp_str = temp_str.join(self.request_val)
    raw = int(temp_str)
    if self.dac.MAX_POS >= raw >= self.dac.MAX_NEG:
        self.dac.act_val = raw
        self.response += "Actual value is: " + str(self.dac.act_val)
    else:
        self.dac.act_val = 0  # if we go out of range we get 0
        self.response += "Out of range[-1,1] or 0. Actual value is: " + str(self.dac.act_val)
    self.dac.registerValue()


@register_method
def volt_norm(self):
    norm = int(self.request_val[0])
    if 0 < norm <= 1:
        self.dac.act_val = int(self.dac.MAX_POS * norm)
        self.response += "Actual value is: " + str(self.dac.act_val)
    elif 0 > norm >= -1:
        self.dac.act_val = int(-self.dac.MAX_NEG * norm)
        self.response += "Actual value is: " + str(self.dac.act_val)
    else:
        self.dac.act_val = 0
        self.response += "Out of range[-1,1] or 0. Actual value is: " + str(self.dac.act_val)
    self.dac.registerValue()


@register_method
def __del__(self):
    self.dac.__del__()
