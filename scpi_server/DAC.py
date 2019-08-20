from .Common.common import *
from .Parser.parser import *

import socket
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI


def convertComplement_DAC(value, width=20):
    #        Return the binary representation of the input number as a string.
    #        If width is not given it is assumed to be 20. If width is given, the two's complement of the number is
    #        returned, with respect to that width.
    #        In a two's-complement system negative numbers are represented by the two's
    #        complement of the absolute value. This is the most common method of
    #        representing signed integers on computers. A N-bit two's-complement
    #        system can represent every integer in the range [-2^(N-1),2^(N-1)-1]

    def warning(widt, width_bin):

        # the function checks if the width is a good value for input number, if not (f.e smaller) returning default 20

        if widt != 20 and (widt <= 0 or width < width_bin):
            print("Bad width, returning default\n")
            return width_bin
        elif widt == 20 and widt < width_bin:
            return width_bin
        else:
            return widt

    if value > 0:
        binar = bin(int(value))[2:]  # take binary representation of input value
        real_width = warning(width, len(binar))  # check width
        if real_width > len(binar):  # add zeros if width is bigger that binary length
            for x1 in range(0, real_width - len(binar)):
                binar = "0" + binar
        return binar

    elif value == 0:  # all zeros
        binar = ""
        for x2 in range(0, width):
            binar = "0" + binar

    elif value < 0:
        binar = bin(abs(int(value)))[2:]  # because of the minus sign at the beginning we take absolute value
        real_width = warning(width, len(binar))
        if abs(value) == pow(2, real_width - 1):
            return binar
        if real_width > len(binar):  # with bigger length we have to add zeros at the beginning
            for x3 in range(0, real_width - len(binar)):
                binar = "0" + binar
        strin = ""  # empty temporary string
        for x in range(0, real_width):
            if int(binar[x]) == 1:
                temp = 0  # negating for the 2's complement
            else:
                temp = 1
            strin = strin + str(temp)
        temp_add = int(strin, 2)
        temp_add = temp_add + 1
        string = bin(temp_add)[2:]
        for x in range(0, real_width - len(binar)):
            binar = "0" + binar
        return binar


# ADD ERRORS CLASSES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class DAC:

    def __init__(self):
        # create outer classes with ability to change inner parameters
        self.commons = Commons(self)
        self.parser = CommandTree(self)
        self.msg_parse = self.ParseMessage(self)

        self.commons.__init__(self)
        self.parser.__init__(self)
        self.msg_parse.__init__(self)
        # using two's complement
        # CONSTS
        self.DAC_SEND = "0001"  # value to be sending information to dac
        self.MAX_NEG = -pow(2, 19)  # max neg value that can be achieved
        self.MAX_POS = int(0b01111111111111111111)  # max pos value that can be achieved
        self.MAX_CLOCK = 35000000  # maximal clock value we can get in Hz
        self.MIN_CLOCK = 10000  # minimal clock value we can get in Hz
        self.IP = '192.168.0.20'
        self.PORT = 5555

        self.act_val = 0  # actual value
        self.clock = self.MIN_CLOCK  # begin with min value

        self.spi = SPI(1, 0)  # spi for our communication
        self.spi.msh = self.clock

        # Triggers for the DAC
        self.reset = False
        self.ldac = False
        GPIO.setup("P8_17", GPIO.OUT)  # LDAC
        GPIO.setup("P8_18", GPIO.OUT)  # RESET
        GPIO.output("P8_18", self.reset)
        GPIO.output("P8_17", self.ldac)

        # Address for which DAC
        self.dac_address = list()
        self.dac_address = [0, 0, 0, 0, 0]  # default
        GPIO.setup("P9_15", GPIO.OUT)  # P0
        GPIO.setup("P9_11", GPIO.OUT)  # P1
        GPIO.setup("P9_12", GPIO.OUT)  # P2
        GPIO.setup("P9_13", GPIO.OUT)  # P3
        GPIO.setup("P9_14", GPIO.OUT)  # P4

        # server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.parser.contr_res_button()  # reset voltage
        self.spi.close()  # spi close
        self.s.close()  # server close

    def serv_create(self, buffer=5):
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.IP, self.PORT))
        self.s.listen(buffer)
        print("Creation of server successful on", self.IP, self.PORT)
        self.s.setblocking(False)

    def initializeDAC(self):  # we can always change the initialize and make it more flexible
        GPIO.output("P8_17", GPIO.HIGH)
        self.spi.writebytes([0b00100000, 0b00000000, 0b00100010])
        GPIO.output("P8_17", GPIO.LOW)

    def registerValue(self):

        self.initializeDAC()
        if self.act_val != 0:
            temp = convertComplement_DAC(self.act_val, 20)
            string1 = self.DAC_SEND + temp[0:4]
            string2 = temp[4:12]
            string3 = temp[12:]
            GPIO.output("P8_17", GPIO.HIGH)
            self.spi.writebytes([int(string1, 2), int(string2, 2), int(string3, 2)])
            GPIO.output("P8_17", GPIO.LOW)
        else:
            self.parser.contr_res_button()

    # A class that will parse information, contain current path, include message to be sent back, request will
    # be proceeded after receiving value that user wants from us. The message will be provided in ASCI format.
    class ParseMessage:
        def __init__(self, dac):
            # to allow memory of current path we will save a string path and every time when we go to other path we
            # wil change the dictionary with inner functions from common or parser, thanks to that we don't need to
            # worry about getting in other dictionaries!
            self.current_branch = ""
            self.curr_dic_short = dac.parser.root_short
            self.curr_dic_long = dac.parser.root_long
            self.request = None  # current request
            self.request_val = None  # current request value
            self.response = None  # This will be the response to send to the client
            self.message = ""  # Message that server got
            self.expect_request = False  # we will make functions in dictionary expect request

            self.terminator = '\n'
            self.command_separator = ';'
            # A semicolon separates two commands in the same message without changing
            # the current path.
            self.path_separator = ':'
            # When a colon is between two command keywords, it moves the current path down
            # one level in the command tree.
            self.parameters_separator = ','
            self.query = '?'

            self.dac = dac

        def take_msg(self, data):
            self.message = data.decode("ascii")

        def send_response(self):
            return self.response

        def clear_path(self):
            self.current_branch = ""
            self.curr_dic_short = self.dac.parser.root_short
            self.curr_dic_long = self.dac.parser.root_long
            self.message = ""

        def find_path(self, path_temp):
            # we now check for instance of the path in the dictionary
            err_short = self.curr_dic_short(str(path_temp).upper())
            err_long = self.curr_dic_long(str(path_temp).upper())
            # ADD ERRRRORRORORORORR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            error = err_long == -1 and err_short == -1
            if error:
                self.response = "Wrong path, problem with: (No such directory) - " + str(path_temp) + "Try again\n"
                self.message = ""
            return error

        def find_in_common(self, path_temp):
            error = self.dac.commons.common(str(path_temp).upper())
            if not error:
                self.response = "Wrong path, problem with: (No such directory) - " + str(path_temp) + "Try again\n"
                self.message = ""
            return error

        # we define request sending function as it may be finishing command
        def request_sending(self, path_temp):
            self.request_val = path_temp
            self.space_handle()
            error = self.find_path(self.request)  # now we can execute function from request
            self.request_val = ""
            self.request = ""
            if not error:
                self.response = "Wrong path, problem with: (No such directory) - " + str(path_temp) + "Try again\n"
                self.message = ""
            return error

        # three finishing commands are possible
        #   -change the path
        #   -request handle
        #   -common request
        def msg_handle(self, msg):
            self.message = msg
            temp = list(self.message)
            if temp[0] == self.path_separator and self.current_branch == "":
                del temp[0]
                # we are at the root branch
            elif temp[0] == self.path_separator and not self.current_branch == "":
                self.response = "Can't access you path " + msg + ". Can't use : at the beginning. Try again\n"
                self.message = ""
                return
                # Later add error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # now we iterate on requested path
            path_temp = list()
            # our possibilities are:
            #   -terminator - finishes sentence and clears path
            #   -finish of temp - finishes sentence and leaves path
            #   -white space - can be omitted after : or ; or can mean that we wait for the request
            #   -: - we know that we need to change path
            #   -; - we start a new command either by resetting path with ;: or in the same directory
            for i in temp:
                path_temp.append(temp[i])
                # terminator clears the path!
                if temp[i] == self.terminator:
                    if self.expect_request:
                        error = self.request_sending(path_temp)
                        if error == -1:
                            return -1
                    else:
                        error = self.find_in_common(path_temp)
                        if error == -1:
                            return -1
                    error = 0
                    return error  # 0 is returned when no error occurred!
                # if we get ; we pop it back, check for request and if no request needed then check in common
                # as it hasn't been already executed before, we just check if it's a command without parameters
                if temp[i] == self.command_separator:
                    path_temp.pop()
                    if self.expect_request:
                        error = self.request_sending(path_temp)
                        if error == -1:
                            return -1
                    else:
                        error = self.find_in_common(path_temp)
                        if error == -1:
                            return -1
                    path_temp = []
                    continue
                # if we get :
                if temp[i] == self.path_separator:
                    if temp[i - 1] == self.command_separator:
                        # if we have combination ;: we need to clear path
                        self.clear_path()
                        path_temp = []
                        continue
                    path_temp.pop()  # remove : from the end
                    error = self.find_path(path_temp)
                    if error == -1:
                        return -1
                    self.current_branch = self.current_branch + ":" + str(path_temp)
                    path_temp = []
                    continue
                # <WSP> handling and request processing
                if temp[i] == " " and (temp[i - 1] == self.path_separator or temp[i - 1] == self.command_separator):
                    # ignore whitespaces after : or ;
                    path_temp.pop()
                    continue
                if temp[i] == " " and (temp[i - 1] != self.path_separator or temp[i - 1] != self.command_separator):
                    # whitespace after command makes expecting response
                    path_temp.pop()
                    error = self.request = path_temp  # we are waiting for request value before getting it done
                    if error == -1:
                        return -1
                    path_temp = []
                    continue

        def space_handle(self):
            temp = list(self.request_val)
            for i in temp:
                if temp[i] == " ":
                    del temp[i]
            self.request_val = temp
            return
