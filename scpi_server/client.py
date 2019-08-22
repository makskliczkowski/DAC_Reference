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
    if mask & selectors.EVENT_WRITE:
        msg = input('Please send message to the DAC or press enter: ')
        if msg != 0:
            print('Sending: ', msg)
            temp_sock.send((msg + terminator).encode("ascii"))
    if mask & selectors.EVENT_READ:
        recv_data = temp_sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('from connection', temp_data, 'received: ')
            print(recv_data.decode("ascii"))
        else:
            print('No msg or finished')
            print('Closing connection to: ', temp_data)
            sel.unregister(temp_sock)
            temp_sock.close()



def start_connection(IP, PORT, sel, connid):
    server_addr = (IP, PORT)
    print('starting connection ', connid, 'to', server_addr)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(False)
    s.connect_ex((IP, PORT))
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = connid
    sel.register(s, events, data=data)


connid = 0
try:
    while True:
        start_connection(IP, PORT, sel, connid)
        connid += 1
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
