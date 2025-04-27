import socket
import sys
import json

client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_conn.connect(("localhost", 23456))

C_FLAGS = {"CWR":0, "ECE":0, "URG":0, "ACK":0, "PSH":0, "RST":0, "SYN":0, "FIN":0}
TCP_conn = False

while True:
    try:
        print("\nSelect an option: \n(1) - Establish TCP connection \n(2) - Send data")
        usr_input = input()

        if usr_input == "1":
            if TCP_conn == True:
                print("\nTCP connection has already been established.")
            else:
                print("\n--------- Establishing TCP connection ---------")

                # Send
                print("[1] SYN: Client -> Server")
                C_FLAGS.update({"SYN":1})
                flags_json = json.dumps(C_FLAGS) # Serialise data, turn dictionary into string
                client_conn.send(bytes(flags_json, "utf-8"))
                C_FLAGS.update({"SYN":0})
                print("Client waiting for SYN-ACK...")

                # Receive
                d = client_conn.recv(1024)
                data = d.decode("utf-8")
                server_flags = json.loads(data)

                if server_flags["SYN"] == 1 and server_flags["ACK"] == 1:
                    print(f"\n[3] ACK: Client -> Server")
                    C_FLAGS.update({"ACK":1})
                    flags_json = json.dumps(C_FLAGS)
                    client_conn.send(bytes(flags_json, "utf-8"))
                    C_FLAGS.update({"ACK":0})
                    print("\nTCP Connection Established! 🎉")
                    TCP_conn = True
                    print("-----------------------------------------------\n")

            print(f"DEBUG: Data received from server: {data}")
        
        elif usr_input == "2":
            if TCP_conn == True:
                print("Send message to server. Type EXIT to exit.")
                while True:
                    message = input()
                    if message == "EXIT":
                        print("Exiting...")
                        break
                    client_conn.send(bytes(message, "utf-8"))
            else:
                print("\nA TCP connection needs to be established before messages can be transmitted.")
        else:
            print("\nERROR - Invalid selection")

    except KeyboardInterrupt:
        print("\nERROR - Keyboard Interrupt")
        sys.exit(1)
        break