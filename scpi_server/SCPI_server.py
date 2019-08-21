import select


# This is a class that handles the whole message with parsing it, then the
# information will be processed and sent to the DAC inside parse class to adapt by DAC.
def server_handle(Message):
    # Function that will handle server requests, add selectors and allow multiple connections, to be seen how it works
    terminator = '\n'
    socket = Message.dac.s
    inputs = [socket]
    outputs = [socket]
    msg=""
    try:
        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, [])
            if len(readable) != 0:

                for s in readable:
                    if s is socket:  # we accept new connections if it is a server
                        conn, client_addr = s.accept()
                        print("Accepted connection from: ", client_addr)
                        inputs.append(conn)
                    else:
                        print("Waiting for data to receive")
                        data = s.recv(1024)  # we take data from client
                        if data:
                            Message.take_msg(data)
                            if s not in outputs:  # if it isn't in outputs add it
                                outputs.append(s)
                        else:  # else if nothing has been sent take connection down
                            if s in outputs:
                                outputs.remove(s)
                            inputs.remove(s)
            for s in writable:
                next_message = Message.send_response()
                if not next_message:
                    break
                else:
                    s.send(bytes(next_message + terminator))
            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
        Message.__del__()
