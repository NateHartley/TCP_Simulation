import socket, sys, json, time
from packet import Packet
from state import ClientState

client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_conn.connect(("localhost", 23456))

state = ClientState.CLOSED.name
c_packet = Packet()

while True:
    try:
        print("\nSelect an option: \n(1) - Establish TCP connection \n(2) - Send data \n(3) - Terminate connection")
        usr_input = input()

        if usr_input == "1":
            if state == ClientState.CLOSED.name:

                # Send SYN to server
                print("\n--------- Establishing TCP connection ---------")
                print("[1] SYN: Client -> Server")
                c_packet.set_flag("SYN")
                packet_json = json.dumps(c_packet.to_dict()) # Serialise data, turn dictionary into string
                client_conn.send(bytes(packet_json, "utf-8"))
                c_packet.clear_flag("SYN")
                state = ClientState.SYNSENT.name
                print("Client waiting for SYN-ACK...")

                # Server data received
                data = client_conn.recv(1024).decode("utf-8")

                # Tries to deserialise the data
                try:
                    s_packet = json.loads(data)
                except:
                    print("ERROR: Data can't be deserialised.")

                # Send ACK to establish connection with server
                if s_packet["flags"]["SYN"] == 1 and s_packet["flags"]["ACK"] == 1 and state == ClientState.SYNSENT.name:
                    print(f"[3] ACK: Client -> Server")
                    c_packet.set_flag("ACK")
                    packet_json = json.dumps(c_packet.to_dict())
                    client_conn.send(bytes(packet_json, "utf-8"))
                    c_packet.clear_flag("ACK")
                    state = ClientState.ESTABLISHED.name
                    print("\nTCP Connection Established! 🎉")
                    print("-----------------------------------------------\n")
            
            else:
                print("\nTCP connection has already been established.")
        
        elif usr_input == "2":
            if state == ClientState.ESTABLISHED.name:
                print("Send message to server. Type EXIT to exit.")
                while True:
                    message = input()
                    if message == "EXIT":
                        print("Exiting...")
                        break
                    c_packet.set_flag("ACK")
                    c_packet.data = message
                    packet_json = json.dumps(c_packet.to_dict())
                    client_conn.send(bytes(packet_json, "utf-8"))
                    c_packet.clear_flag("ACK")
            else:
                print("\nA TCP connection needs to be established before messages can be transmitted.")

        elif usr_input == "3":
            while state == ClientState.ESTABLISHED.name or state == ClientState.FINWAIT1.name or state == ClientState.FINWAIT2.name:
            
                # Closing connection 1
                if state == ClientState.ESTABLISHED.name:
                    print("\n--------- Disconnecting TCP connection --------")
                    print("[1] FIN: Client -> Server")
                    c_packet.set_flag("FIN")
                    packet_json = json.dumps(c_packet.to_dict())
                    client_conn.send(bytes(packet_json, "utf-8"))
                    c_packet.clear_flag("FIN")
                    state = ClientState.FINWAIT1.name
                    print("Client waiting for ACK...")

                # Server data received
                data = client_conn.recv(1024).decode("utf-8")

                # Tries to deserialise the data
                try:
                    s_packet = json.loads(data)
                except:
                    print("ERROR: Data can't be deserialised.")

                # Closing connection 2
                if s_packet["flags"]["ACK"] and state == ClientState.FINWAIT1.name:
                    state = ClientState.FINWAIT2.name
                    print("Client waiting for FIN...")

                # Closing connection 3
                if s_packet["flags"]["FIN"] and state == ClientState.FINWAIT2.name:
                    print("[4] ACK: Client -> Server")
                    c_packet.set_flag("ACK")
                    packet_json = json.dumps(c_packet.to_dict())
                    client_conn.send(bytes(packet_json, "utf-8"))
                    c_packet.clear_flag("ACK")
                    state = ClientState.TIMEWAIT.name

                # Closing connection 4
                if state == ClientState.TIMEWAIT.name:
                    time.sleep(2) # Time delay to simulate client waiting for server to receive ACK flag
                    state = ClientState.CLOSED.name

                # Closing connection 5
                if state == ClientState.CLOSED.name:
                    print("\nClosing connection...")
                    print("-----------------------------------------------\n")
                    sys.exit(1)
                
            else:
                print("No connection established, client program quitting...")
                break
        else:
            print("\nERROR - Invalid selection")

    except KeyboardInterrupt:
        print("\nERROR - Keyboard Interrupt")
        sys.exit(1)
        break