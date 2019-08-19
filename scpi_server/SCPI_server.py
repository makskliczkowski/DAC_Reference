import selectors


# This is a class that handles the whole message with parsing it, then the
# information will be processed and sent to the DAC inside parse class to adapt by DAC.

def accept_client(sock, sel):
    conn, address = sock.accept()  # we accept new socket
    print("Accepted connection from", address)
    conn.setblocking(False)
    message = Message(sel, conn, address)
    sel.register(conn, selectors.EVENT_READ, data=message)


def server_handle(dac):
    # Function that will handle server requests, add selectors and allow multiple connections, to be seen how it works
    sel = selectors.DefaultSelector()
    sel.register(dac.s, selectors.EVENT_READ, data=None)
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                # if there is no data we should accept new client
                if key.data is None:
                    accept_client(key.fileobj)
                # else we have to take message
                else:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        # we need to add every exeption we can get, for later
                        message.close()
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()


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
