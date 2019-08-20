import select
from . import DAC


# This is a class that handles the whole message with parsing it, then the
# information will be processed and sent to the DAC inside parse class to adapt by DAC.
def server_handle(dac):
    # Function that will handle server requests, add selectors and allow multiple connections, to be seen how it works
    terminator = '\n'
    inputs = [dac.s]
    outputs = []

    while inputs:
        try:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for s in readable:
                if s is dac.s:  # we accept new connections if it is a server
                    conn, client_addr = s.accept()
                    conn.setblocking(0)
                    inputs.append(conn)
                else:
                    data = s.receive(1024)  # we take data from client
                    if data:
                        dac.msg_parse.take_msg(data)
                        if s not in outputs:  # if it isn't in outputs add it
                            outputs.append(s)
                    else:  # else if nothing has been sent take connection down
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
            for s in writable:
                next_message = dac.msg_parse.send_response()
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
        except:
            pass
        finally:
            dac.__del__()
