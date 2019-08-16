import socket
import select
import selectors
import time
import types
import sys
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI


def accept_client(sock, sel):
    conn, address = sock.accept()  # we accept new socket
    print("Accepted connection from", address)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=address, in_buffer=b'', out_buffer=b'')  # create info about client
    message = Message(sel, conn, address)
    sel.register(conn, selectors.EVENT_READ, data=message)




class dac:
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
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def serv_create(self, buffer=5):
        self.s.bind((self.IP, self.PORT))
        self.s.listen()
        print(f"Creation of server on {(self.IP, self.PORT)} successful")
        self.s.setblocking(False)

    # This is a class that handles the whole message before parsing it

 class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.received_buffer = b''
        self.send_buffer = b''
        self.response=None
        self.created_response=False
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
    def create_response(self,response):
        self.response = response
        self.send_buffer+= response
        self.created_response=True
    def process_message(self):
