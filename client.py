import socket
import sys
import json
from packet import Packet

client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_conn.connect(("localhost", 23456))

C_STATES = ["CLOSED", "SYN-SENT", "ESTABLISHED", "FIN-WAIT-1", "FIN-WAIT-2", "TIME-WAIT"]
state = C_STATES[0]
TCP_conn = False
c_packet = Packet()

while True:
    try:
        print("\nSelect an option: \n(1) - Establish TCP connection \n(2) - Send data \n(3) - Exit client")
        usr_input = input()

        if usr_input == "1":
            if not TCP_conn:
                state = C_STATES[1]

                # Send SYN to server
                print("\n--------- Establishing TCP connection ---------")
                print("[1] SYN: Client -> Server")
                c_packet.set_flag("SYN")
                p = json.dumps(c_packet.to_dict()) # Serialise data, turn dictionary into string
                client_conn.send(bytes(p, "utf-8"))
                c_packet.clear_flag("SYN")
                print("Client waiting for SYN-ACK...")

                # Server data received
                data = client_conn.recv(1024).decode("utf-8")

                # Tries to deserialise the data
                try:
                    s_packet = json.loads(data)
                except:
                    print("ERROR: Data can't be deserialised.")

                # Send ACK to establish connection with server
                if s_packet["flags"]["SYN"] == 1 and s_packet["flags"]["ACK"] == 1:
                    state = C_STATES[2]
                    print(f"\n[3] ACK: Client -> Server")
                    c_packet.set_flag("ACK")
                    p = json.dumps(c_packet.to_dict())
                    client_conn.send(bytes(p, "utf-8"))
                    c_packet.clear_flag("ACK")
                    print("\nTCP Connection Established! 🎉")
                    print("-----------------------------------------------\n")
                    TCP_conn = True
            
            else:
                print("\nTCP connection has already been established.")
        
        elif usr_input == "2":
            if TCP_conn == True:
                print("Send message to server. Type EXIT to exit.")
                while True:
                    message = input()
                    if message == "EXIT":
                        print("Exiting...")
                        break
                    c_packet.set_flag("ACK")
                    c_packet.data = message
                    p = json.dumps(c_packet.to_dict())
                    client_conn.send(bytes(p, "utf-8"))
            else:
                print("\nA TCP connection needs to be established before messages can be transmitted.")
        elif usr_input == "3":
            print("Closing connection...")
            break
        else:
            print("\nERROR - Invalid selection")

    except KeyboardInterrupt:
        print("\nERROR - Keyboard Interrupt")
        sys.exit(1)
        break