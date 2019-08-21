try:
    import selectors
except:
    import selectors34 as selectors
import socket
import types

# This is a class that handles the whole message with parsing it, then the
# information will be processed and sent to the DAC inside parse class to adapt by DAC.
def serv_create(s, buffer=5):
    IP = "192.168.0.20"
    PORT = 5555
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IP, PORT))
    s.listen(buffer)
    print("Creation of server successful on", IP, PORT)
    # self.s.setblocking(False)


def server_handle(Message):
    # Function that will handle server requests, add selectors and allow multiple connections, to be seen how it works

    def accept_wrapper(socke, selector):
        connection, addr = socke.accept()  # Should be ready to read
        print('accepted connection from', addr)
        connection.setblocking(False)
        dat = addr
        event = selectors.EVENT_READ | selectors.EVENT_WRITE
        selector.register(connection, event, data=dat)

    terminator = '\n'

    sel = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_create(sock, 5)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, data=None)

    msg = ""
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj, sel)
                else:
                    temp_sock = key.fileobj
                    temp_data = key.data
                    if mask & selectors.EVENT_READ:
                        # we take the received data and send it to Message to execute it
                        print("Waiting for data to receive")
                        recv_data = temp_sock.recv(1024)  # Should be ready to read
                        if recv_data:
                            Message.take_msg(recv_data)
                        else:
                            print('closing connection to', temp_data.addr)
                            sel.unregister(sock)
                            temp_sock.close()
                    if mask & selectors.EVENT_WRITE:
                        next_message = Message.send_response()
                        if not next_message:
                            continue
                        else:
                            temp_sock.send(bytes(next_message + terminator))

    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
        Message.__del__()
