from Adafruit_BBIO.SPI import SPI
import time
import Adafruit_BBIO.GPIO as GPIO


def convertComplement_DAC(value, width=20):
    #    """
    #        Return the binary representation of the input number as a string.
    #        If width is not given it is assumed to be 20. If width is given, the two's complement of the number is
    #        returned, with respect to that width.
    #        In a two's-complement system negative numbers are represented by the two's
    #        complement of the absolute value. This is the most common method of
    #        representing signed integers on computers. A N-bit two's-complement
    #        system can represent every integer in the range [-2^(N-1),2^(N-1)-1]
    #    """
    def warning(width, width_bin):  # function returns good value
        if width != 20 and (width <= 0 or width < width_bin):
            print("Bad width, returning default\n")
            return width_bin
        elif width == 20 and width < width_bin:
            return width_bin
        else:
            return width

    if value > 0:
        binary = bin(int(value))[2:]
        real_width = warning(width, len(binary))
        if real_width > len(binary):
            for x in range(0, real_width - len(binary)):
                binary = "0" + binary
        return binary
    elif value == 0:
        binary = ""
        for x in range(0, width):
            binary = "0" + binary
    elif value < 0:
        binary = bin(abs(int(value)))[2:]  # because of the minus sign at the beginning
        real_width = warning(width, len(binary))
        if abs(value) == pow(2, real_width - 1):
            return binary
        if real_width > len(binary):  # with bigger length we have to add zeros at the beginning
            for x in range(0, real_width - len(binary)):
                binary = "0" + binary
        string = ""
        for x in range(0, real_width):
            if int(binary[x]) == 1:
                temp = 0  # negating
            else:
                temp = 1
            string = string + str(temp)
        temp_add = int(string, 2)
        temp_add = temp_add + 1
        string = bin(temp_add)[2:]
        binar = string
        return binar


class DACRef:

    def __init__(self, maxClock=33000000):
        # using two's complement
        self.dacSend = "0001"
        self.max_raw_minus = -pow(2, 19)  # maximal value that can be achieved
        self.max_raw_plus = int(0b01111111111111111111)
        self.actVal = 0  # actual value
        # SPI
        self.spi = SPI(1, 0)  # choose SPI device
        self.spi.mode = 0b00
        if maxClock > 10000:
            self.spi.msh = maxClock
        else:
            self.spi.msh = 33000000
            print("Minumum clock speed is 10000, setting default 33Mhz")
        # Start values
        self.reset = 0
        self.ldac = 0  # in the beggining the device is not ready(remember they are inverted)

        # P8
        GPIO.setup("P8_17", GPIO.OUT)  # LDAC
        GPIO.output("P8_17", self.ldac)
        GPIO.setup("P8_18", GPIO.OUT)  # RESET
        GPIO.output("P8_18", self.reset)

        # GPIO.setup("P8_15", GPIO.OUT) #ext rsten
        # GPIO.setup("P8_14", GPIO.OUT) # PLL LOCK
        # GPIO.setup("P8_16", GPIO.OUT) # ext Ioupden
        # NOT USED

        # P9 (addresses)
        self.dacAddress = [0, 0, 0, 0, 0]  # default
        GPIO.setup("P9_11", GPIO.OUT)  # P1
        GPIO.setup("P9_12", GPIO.OUT)  # P2
        GPIO.setup("P9_13", GPIO.OUT)  # P3
        GPIO.setup("P9_14", GPIO.OUT)  # P4
        GPIO.setup("P9_15", GPIO.OUT)  # P0

    def setDACAddress(self, list):
        self.dacAddress = list
        GPIO.setup("P9_15", self.dacAddress[0])  # P0
        GPIO.setup("P9_11", self.dacAddress[1])  # P1
        GPIO.setup("P9_12", self.dacAddress[2])  # P2
        GPIO.setup("P9_13", self.dacAddress[3])  # P3
        GPIO.setup("P9_14", self.dacAddress[4])  # P4

    def chooseDAC(self, dacNum=0, board=0):

        if board == 0:
            p2 = 0
            p3 = 0
            p4 = 0
        elif board == 1:
            p2 = 0
            p3 = 0
            p4 = 1
        elif board == 2:
            p2 = 0
            p3 = 1
            p4 = 0
        elif board == 3:
            p2 = 0
            p3 = 1
            p4 = 1
        else:
            print("WRONG NUMBER, SETTING 0")
            p2 = 0
            p3 = 0
            p4 = 0

        GPIO.output("P9_12", p2)
        GPIO.output("P9_13", p3)
        GPIO.output("P9_14", p4)

        if dacNum == 0:
            p0 = 0
            p1 = 0
        elif dacNum == 1:
            p0 = 0
            p1 = 1
        elif dacNum == 2:
            p0 = 1
            p1 = 0
        elif dacNum == 3:
            p0 = 1
            p1 = 1
        GPIO.output("P9_15", p0)
        GPIO.output("P9_11", p1)
        self.dacAddress = [p0, p1, p2, p3, p4]

    def setLDAC(self, ldac):
        self.ldac = ldac
        GPIO.output("P8_17", self.ldac)

    def resetDAC(self):
        self.reset = 1
        GPIO.output("P8_18", self.reset)
        GPIO.output("P8_18", 0)  # returns it back to 0

    def setValueRaw(self, raw):
        if self.max_raw_plus >= int(raw) >= self.max_raw_minus:
            self.actVal = int(raw)
            print("Actual value is: " + str(self.actVal))
        else:
            self.actVal = 0  # if we go out of range we get 0
            print("Out of range[-1,1] or 0.")
            print("Actual value is: " + str(self.actVal))
        self.registerValue()

    def setValueNorm(self, norm):
        if 0 < norm <= 1:
            self.actVal = int(self.max_raw_plus * norm)
            print("Actual value is: " + str(self.actVal))
        elif 0 > norm >= -1:
            self.actVal = int(-self.max_raw_minus * norm)
            print("Actual value is: " + str(self.actVal))
        else:
            self.actVal = 0
            print("Out of range[-1,1] or 0.")
            print("Actual value is: " + str(self.actVal))
        self.registerValue()

    def setValHelp(self, address):
        val = input("Write the value from [-524288,524287]: ")
        if val <= self.max_raw_plus and val >= self.max_raw_minus:
            self.setDACAddress(address)
            self.setValueNorm(int(val))
        else:
            print("Wrong number, doing nothing")
            return

    def initializeDAC(self):  # we can always change the initialize and make it more flexible
        GPIO.output("P8_17", GPIO.HIGH)
        self.spi.writebytes([0b00100000, 0b00000000, 0b00100010])
        GPIO.output("P8_17", GPIO.LOW)

    def registerValue(self):

        self.initializeDAC()
        if self.actVal != 0:
            temp = convertComplement_DAC(self.actVal, 20)
            string1 = self.dacSend + temp[0:4]
            string2 = temp[4:12]
            string3 = temp[12:]
            GPIO.output("P8_17", GPIO.HIGH)
            self.spi.writebytes([int(string1, 2), int(string2, 2), int(string3, 2)])
            GPIO.output("P8_17", GPIO.LOW)
        else:
            self.resetDAC()

    def __del__(self):
        self.resetDAC()
        self.spi.close()
