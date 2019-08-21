import socket
import selectors
import types
IP = '192.168.0.20'
PORT = 5555
terminator = '\n'


connid = 0
while True:
    sel = selectors.DefaultSelector()
    connid += 1
    server_addr = (IP, PORT)
    print('starting connection ', connid, 'to', server_addr)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(False)
    s.connect_ex((IP, PORT))
    events = selectors.EVENT_READ|selectors.EVENT_WRITE
    message = input("Please tell the message")
    data = types.SimpleNamespace(connid=connid,
                                 message = message,
                                 outb=b'',
                                 inb=b'')
    sel.register(s, events, data = data)

    def service_connection(key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print('from connection', data.connid)
                print(" received message, decoding...")
                print(rec.decode("ascii") + '\n')
                data.recv_total += len(recv_data)

print("connected to", IP, ":", PORT)
#


inputs = [s]
outputs = [s]


    try:
        readable, writable, exceptional = select.select(inputs, outputs, [])
        if len(inputs) != 0:
            print("Waiting for rec msg")
            rec = s.recv(1024)
            if len(rec) != 0:
                print("recieved, decoding...")
                print(rec.decode("ascii")+'\n')
            else:
                print("No msg")
        if len(outputs) != 0:
            print("Now I may send some")
            msg = input("Please send message to the DAC or press enter: ")
            if msg != 0:
                s.send(bytes(msg + terminator))
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
        s.close()
