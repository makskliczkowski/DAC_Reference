import socket
import select
import selectors
import time
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI

class device:
    def __init__(self):
        # using two's complement
        self.DAC_SEND = "0001"  # value to be sending information to dac
        self.MAX_NEG = -pow(2,19)  # max neg value that can be achieved
        self.MAX_POS = int(0b01111111111111111111) # max pos value that can be achieved
        self.MAX_CLOCK = 35000000  # maximal clock value we can get in Hz

        self.actVal = 0  # actual value
        self.spi = None
        # Triggers for the DAC
        self.reset = None
        self.ldac = None
        GPIO.setup("P8_17", GPIO.OUT)  # LDAC
        GPIO.setup("P8_18", GPIO.OUT)  # RESET
        # Address for which DAC
        GPIO.setup("P9_15", GPIO.OUT)  # P0
        GPIO.setup("P9_11", GPIO.OUT)  # P1
        GPIO.setup("P9_12", GPIO.OUT)  # P2
        GPIO.setup("P9_13", GPIO.OUT)  # P3
        GPIO.setup("P9_14", GPIO.OUT)  # P4

        #server


