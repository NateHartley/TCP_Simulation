import socket
import sys
import json

server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Server can be re-issued immediately
server_conn.bind(("127.0.0.1", 23456))
server_conn.listen()
conn, addr = server_conn.accept()

S_FLAGS = {"CWR":0, "ECE":0, "URG":0, "ACK":0, "PSH":0, "RST":0, "SYN":0, "FIN":0}

with conn:
    print(f'Connection initiated with {addr}')

    while True:
        try:
            # Receive
            d = conn.recv(1024)
            data = d.decode("utf-8")

            try:
                client_flags = json.loads(data)
            except:
                print("Data can't be deserialised.")

            # breaks loop if data is empty
            if not data: 
                print("Client disconnected...")
                break

            # Send
            if client_flags["SYN"] == 1:
                print("\n--------- Establishing TCP connection ---------")

                print("[2] SYN-ACK: Server -> Client")
                S_FLAGS.update({"SYN":1})
                S_FLAGS.update({"ACK":1})
                flags_json = json.dumps(S_FLAGS)
                conn.send(bytes(flags_json, "utf-8"))
                S_FLAGS.update({"SYN":0})
                S_FLAGS.update({"ACK":0})
                print("Server waiting for ACK...")
                client_flags["SYN"] = 0 # reset it otherwise it will keep triggering this when client sending messages bc this var doesn't get nulled
            if client_flags["ACK"] == 1:
                print("\nTCP Connection Established! 🎉")
                print("-----------------------------------------------\n")
                client_flags["ACK"] = 0

            print(f"DEBUG: Data received from client: {data}")

        except KeyboardInterrupt:
            print("\nERROR - Keyboard Interrupt")
            conn.shutdown(socket.SHUT_RDWR) # needs to be conn not server_conn
            conn.close()
            sys.exit(1)
            break

