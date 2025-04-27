import socket
import sys

client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_conn.connect(("localhost", 23456))

TCP_FLAG = ["SYN", "SYN-ACK", "ACK"]
FLAGS = {"CWR":0, "ECE":0, "URG":0, "ACK":0, "PSH":0, "RST":0, "SYN":0, "FIN":0}
TCP_conn = False

while True:
    try:
        print("\nSelect an option: \n(1) - Establish TCP connection \n(2) - Send data")
        usr_input = input()

        if usr_input == "1":
            # Send
            print(f"\n[1] {TCP_FLAG[0]}: Client -> Server")
            FLAGS.update({"ACK":1})
            client_conn.send(bytes(TCP_FLAG[1], "utf-8"))
            # TODO: pass dictionary of flags to server via send() but need to serialise data first with json library
            print(f"Client waiting for {TCP_FLAG[1]}...")

            # Receive
            d = client_conn.recv(1024)
            data = d.decode("utf-8")

            if data == TCP_FLAG[1]:
                print(f"\n[3] {TCP_FLAG[2]}: Client -> Server")
                client_conn.send(bytes(TCP_FLAG[2], "utf-8"))
                print("\nTCP Connection Established! 🎉")
                TCP_conn = True

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