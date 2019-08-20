import socket
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI

from scpi_server.Common.common import Commons
from scpi_server.Parser.parser import CommandTree


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

    def __init__(self, dictionary):
        # create outer classes with ability to change inner parameters

        # using two's complement
        # CONSTS
        self.dictionary = dictionary
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
        self.dictionary.contr_res_button()  # reset voltage
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
            self.dictionary.contr_res_button()

    # A class that will parse information, contain current path, include message to be sent back, request will
    # be proceeded after receiving value that user wants from us. The message will be provided in ASCI format.


