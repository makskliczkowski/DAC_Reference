try:
    import socket
    import selectors
except:
    import selectors34 as selectors
import types

IP = '192.168.0.20'
PORT = 5555
terminator = '\n'
sel = selectors.DefaultSelector()


def service_connection(key, mask, sel):
    temp_sock = key.fileobj
    temp_data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = temp_sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('from connection', temp_data.connid)
            print(" received message, decoding...\n")
            print(recv_data.decode("ascii") + '\n')
        else:
            print("No msg or finished\n")
            print('closing connection', temp_data.connid)
            sel.unregister(temp_sock)
            temp_sock.close()
    if mask & selectors.EVENT_WRITE:
        print("Now I may send some")
        msg = input("Please send message to the DAC or press enter: ")
        if msg != 0:
            sent = temp_sock.send(bytes(msg + terminator))
            print("Sent: ", sent.decode("ascii"))


def start_connections(IP, PORT, sel):
    connid = 0
    while True:
        connid += 1
        server_addr = (IP, PORT)
        print('starting connection ', connid, 'to', server_addr)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(False)
        s.connect_ex((IP, PORT))
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = input("Please tell the message")
        data = types.SimpleNamespace(connid=connid,
                                     message=message,
                                     outb=b'',
                                     inb=b'')
        sel.register(s, events, data=data)


start_connections(IP, PORT, sel)
try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask, sel)
            # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
