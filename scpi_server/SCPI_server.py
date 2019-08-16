import socket
import select
import selectors
import time
import types
import sys
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI


def accept_client(sock,sel):
    conn, address = sock.accept()  # we accept new socket
    print("Accepted connection from", address)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=address, in_buffer=b'', out_buffer=b'')  # create info about client
    events = selectors.EVENT_READ|selectors.EVENT_WRITE
    sel.register(conn,e)

class DAC:
    def __init__(self):
        # using two's complement
        # CONSTS
        self.DAC_SEND = "0001"  # value to be sending information to dac
        self.MAX_NEG = -pow(2, 19)  # max neg value that can be achieved
        self.MAX_POS = int(0b01111111111111111111)  # max pos value that can be achieved
        self.MAX_CLOCK = 35000000  # maximal clock value we can get in Hz
        self.IP = '192.168.0.20'
        self.PORT = 5555

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

        # server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def serv_create(self, buffer=5):
        self.s.bind((self.IP, self.PORT))
        self.s.listen()
        print(f"Creation of server on {(self.IP, self.PORT)} successful")
        self.s.setblocking(False)

