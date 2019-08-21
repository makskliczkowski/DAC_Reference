import socket
import select
IP = '192.168.0.20'
PORT = 5555
terminator = '\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
print("connected to", IP, ":", PORT)
#s.setblocking(False)
#s.connect_ex((IP, PORT))

inputs = [s]
outputs = [s]

while True:
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
