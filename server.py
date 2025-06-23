import socket, sys, json, time
from packet import Packet
from state import ServerState

server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Server can be re-issued immediately
server_conn.bind(("127.0.0.1", 23456))
server_conn.listen()
conn, addr = server_conn.accept()

state = ServerState.CLOSED.name
s_packet = Packet()

with conn:
    print(f'Connection initiated with {addr}')
    state = ServerState.LISTEN.name

    while True:
        try:
            # Client data received
            data = conn.recv(1024).decode("utf-8")

            # Breaks loop if data is empty
            if not data: 
                print("Client disconnected...")
                break

            # Tries to deserialise the data
            try:
                c_packet = json.loads(data)
            except:
                print("ERROR: Data can't be deserialised.")

            # Send SYN-ACK to client
            if c_packet["flags"]["SYN"] == 1:
                print("\n--------- Establishing TCP connection ---------")
                print("[2] SYN-ACK: Server -> Client")
                s_packet.set_flag("SYN")
                s_packet.set_flag("ACK")
                packet_json = json.dumps(s_packet.to_dict())
                conn.send(bytes(packet_json, "utf-8"))
                s_packet.clear_flag("SYN")
                s_packet.clear_flag("ACK")
                state = ServerState.SYNRECEIVED.name
                print("Server waiting for ACK...")

            # Send ACK to establish connection with client
            if c_packet["flags"]["ACK"] == 1 and state == ServerState.SYNRECEIVED.name:
                state = ServerState.ESTABLISHED.name
                print("\nTCP Connection Established! 🎉")
                print("-----------------------------------------------\n")
            
            # Server in established state, waiting for data from client
            if c_packet["flags"]["ACK"] == 1 and state == ServerState.ESTABLISHED.name:
                if c_packet["data"] != "":
                    print("Received from client: ", c_packet["data"])

            # Closing connection 1
            if c_packet["flags"]["FIN"] == 1 and state == ServerState.ESTABLISHED.name:
                print("\n--------- Disconnecting TCP connection --------")
                print("[2] ACK: Server -> Client")
                s_packet.set_flag("ACK")
                packet_json = json.dumps(s_packet.to_dict())
                conn.send(bytes(packet_json, "utf-8"))
                s_packet.clear_flag("ACK")
                state = ServerState.CLOSEWAIT.name
                time.sleep(0.1) # Small delay to prevent data being sent here and in Closing connection 2 to merge together on the client side
            
            # Closing connection 2
            if state == ServerState.CLOSEWAIT.name:
                print("[3] FIN: Server -> Client")
                s_packet.set_flag("FIN")
                packet_json = json.dumps(s_packet.to_dict())
                conn.send(bytes(packet_json, "utf-8"))
                s_packet.clear_flag("FIN")
                state = ServerState.LASTACK.name
                print("Server waiting for ACK...")

            # Closing connection 3
            if c_packet["flags"]["ACK"] and state == ServerState.LASTACK.name:
                state = ServerState.CLOSED.name

            # Closing connection 4
            if state == ServerState.CLOSED.name:
                print("\nClosing connection...")
                print("-----------------------------------------------\n")
                break

        except KeyboardInterrupt:
            print("\nERROR - Keyboard Interrupt")
            conn.shutdown(socket.SHUT_RDWR) # needs to be conn not server_conn
            conn.close()
            sys.exit(1)
            break

