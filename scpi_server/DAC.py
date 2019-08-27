import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI


# ADD ERRORS CLASSES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class DAC:

    def __init__(self):
        # create outer classes with ability to change inner parameters

        # using two's complement
        # CONSTS
        self.DAC_SEND = "0001"  # value to be sending information to dac
        self.MAX_NEG = -pow(2, 19)  # max neg value that can be achieved
        self.MAX_POS = int(0b01111111111111111111)  # max pos value that can be achieved
        self.MAX_CLOCK = 3400000  # maximal clock value we can get in Hz
        self.MIN_CLOCK = 500000  # minimal clock value we can get in Hz
        self.IP = '192.168.0.20'
        self.PORT = 5555

        self.act_val = 0  # actual value
        self.clock = self.MIN_CLOCK  # begin with min value

        self.spi = SPI(1, 0)  # spi for our communication
        self.spi.mode = 0b00
        self.spi.msh = self.clock

        # Triggers for the DAC
        self.reset = False
        self.ldac = True
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
        GPIO.output("P9_15", GPIO.LOW)  # P0
        GPIO.output("P9_11", GPIO.LOW)  # P1
        GPIO.output("P9_12", GPIO.LOW)  # P2
        GPIO.output("P9_13", GPIO.LOW)  # P3
        GPIO.output("P9_14", GPIO.LOW)  # P4
        self.initializeDAC()
        # server

    @staticmethod
    def reset_dac():
        GPIO.output("P8_18", 1)
        print('Reseting DAC')
        GPIO.output("P8_18", 0)  # returns it back to 0

    def __del__(self):
        self.reset_dac()  # reset voltage
        self.spi.close()  # spi close

    def initializeDAC(self):  # we can always change the initialize and make it more flexible
        GPIO.output("P8_17", GPIO.HIGH)
        self.spi.writebytes([0b00100000, 0b00000000, 0b00100010])
        GPIO.output("P8_17", GPIO.LOW)

    def registerValue(self):
        if self.act_val != 0:
            temp = self.convertComplement_DAC(self.act_val, 20)
            string1 = self.DAC_SEND + temp[0:4]
            string2 = temp[4:12]
            string3 = temp[12:]
            GPIO.output("P8_17", GPIO.HIGH)
            self.spi.writebytes([int(string1, 2), int(string2, 2), int(string3, 2)])
            print('Sending to the DAC: ', string1 + string2 + string3)
            GPIO.output("P8_17", GPIO.LOW)
        else:
            return
            #self.reset_dac()

    @staticmethod
    def convertComplement_DAC(value, width=20):
        #        Return the binary representation of the input number as a string.
        #        If width is not given it is assumed to be 20. If width is given, the two's complement of the number is
        #        returned, with respect to that width.
        #        In a two's-complement system negative numbers are represented by the two's
        #        complement of the absolute value. This is the most common method of
        #        representing signed integers on computers. A N-bit two's-complement
        #        system can represent every integer in the range [-2^(N-1),2^(N-1)-1]

        def warning(widt, width_bin):

            # the function checks if the width is a good value for input number, if not (f.e smaller) returning
            # default 20

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
            binar = bin(temp_add)[2:]
            return binar
