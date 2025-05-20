import socket
import sys
import json
from packet import Packet

server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Server can be re-issued immediately
server_conn.bind(("127.0.0.1", 23456))
server_conn.listen()
conn, addr = server_conn.accept()

S_STATES = ["CLOSED", "LISTEN", "SYN-RECEIVED", "ESTABLISHED", "CLOSE-WAIT", "LAST-ACK"]
state = S_STATES[0]
s_packet = Packet()

with conn:
    print(f'Connection initiated with {addr}')
    state = S_STATES[1]

    while True:
        try:
            # Client data received
            data = conn.recv(1024).decode("utf-8")

            # Tries to deserialise the data
            try:
                c_packet = json.loads(data)
            except:
                print("ERROR: Data can't be deserialised.")

            # Breaks loop if data is empty
            if not data: 
                print("Client disconnected...")
                break

            # Send SYN-ACK to client
            if c_packet["flags"]["SYN"] == 1:
                state = S_STATES[2]
                print("\n--------- Establishing TCP connection ---------")
                print("[2] SYN-ACK: Server -> Client")
                s_packet.set_flag("SYN")
                s_packet.set_flag("ACK")
                flags_json = json.dumps(s_packet.to_dict())
                conn.send(bytes(flags_json, "utf-8"))
                s_packet.clear_flag("SYN")
                s_packet.clear_flag("ACK")
                print("Server waiting for ACK...")

            # Send ACK to establish connection with client
            if c_packet["flags"]["ACK"] == 1 and state == S_STATES[2]:
                state = S_STATES[3]
                print("\nTCP Connection Established! 🎉")
                print("-----------------------------------------------\n")
            
            # Server in established state, waiting for data from client
            if c_packet["flags"]["ACK"] == 1 and state == S_STATES[3]:
                if c_packet["data"] != "":
                    print("Received from client: ", c_packet["data"])

        except KeyboardInterrupt:
            print("\nERROR - Keyboard Interrupt")
            conn.shutdown(socket.SHUT_RDWR) # needs to be conn not server_conn
            conn.close()
            sys.exit(1)
            break

