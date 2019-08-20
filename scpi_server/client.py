import socket
import select
IP = '192.168.0.20'
PORT = 5555
terminator = '\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
print(f"connected to {IP}:{PORT}")
s.setblocking(False)
s.connect_ex((IP, PORT))

inputs = [s]
outputs = [s]

while True:
    try:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        if len(inputs) != 0:
            rec = s.recv(1024)
            if len(rec) != 0:
                print(rec.decode("ascii")+'\n')
        if len(outputs) != 0:
            msg = input("Please send message to the DAC: ")
            if msg != 0:
                s.send(bytes(msg + terminator))
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    except:
        pass
    finally:
        s.close()