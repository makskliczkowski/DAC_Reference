import socket
import select
import selectors
import time
import types
import sys
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


class DAC:
    def __init__(self):
        # using two's complement
        # CONSTS
        self.DAC_SEND = "0001"  # value to be sending information to dac
        self.MAX_NEG = -pow(2, 19)  # max neg value that can be achieved
        self.MAX_POS = int(0b01111111111111111111)  # max pos value that can be achieved
        self.MAX_CLOCK = 35000000  # maximal clock value we can get in Hz
        self.MIN_CLOCK = 10000  # minimal clock value we can get in Hz
        self.IP = '192.168.0.20'
        self.PORT = 5555

        self.actVal = 0  # actual value
        # self.spi = None

        # Triggers for the DAC
        self.reset = False
        self.ldac = False
        GPIO.setup("P8_17", GPIO.OUT)  # LDAC
        GPIO.setup("P8_18", GPIO.OUT)  # RESET
        GPIO.output("P8_18", self.reset)
        GPIO.output("P8_17", self.ldac)

        # Address for which DAC
        self.dacAddress = [0, 0, 0, 0, 0]  # default
        GPIO.setup("P9_15", GPIO.OUT)  # P0
        GPIO.setup("P9_11", GPIO.OUT)  # P1
        GPIO.setup("P9_12", GPIO.OUT)  # P2
        GPIO.setup("P9_13", GPIO.OUT)  # P3
        GPIO.setup("P9_14", GPIO.OUT)  # P4

        # server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def serv_create(self, buffer=5):
        self.s.bind((self.IP, self.PORT))
        self.s.listen(buffer)
        print(f"Creation of server on {(self.IP, self.PORT)} successful")
        self.s.setblocking(False)


# This is a class that handles the whole message with parsing it, then the
# information will be processed by inside parse class and sent to the DAC class.

def accept_client(sock, sel):
    conn, address = sock.accept()  # we accept new socket
    print("Accepted connection from", address)
    conn.setblocking(False)
    message = Message(sel, conn, address)
    sel.register(conn, selectors.EVENT_READ, data=message)


class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.received_buffer = b''
        self.send_buffer = b''
        self.response = None
        self.created_response = False
        # we can add headers and so on, depends on the needs

    def set_mode(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self.received_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self.send_buffer:
            print("sending", repr(self.send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self.send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self.send_buffer = self.send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self.send_buffer:
                    self.close()

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self._read()
        if mask & selectors.EVENT_WRITE:
            self._write()

    def close(self):
        print("closing connection to", self.addr)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                f"error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def create_response(self, response):
        self.response = response
        self.send_buffer += response
        self.created_response = True

    class ParseMessage:
        pass
