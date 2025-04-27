import socket
import sys

client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_conn.connect(("localhost", 23456))

while True:
    print("\nSelect an option: \n[1] - Establish TCP connection \n[2] - Send data")

    try:
        usr_input = input()

        if usr_input == "1":
            # Send
            print("\n[1] SYN: Client -> Server")
            client_conn.send(bytes("SYN", "utf-8"))
            print("Client waiting for SYN-ACK...")

            # Receive
            data = client_conn.recv(1024)
            decoded_data = data.decode("utf-8")

            if decoded_data == "SYN-ACK":
                print("\n3] SYN: Client -> Server")
                client_conn.send(bytes("ACK", "utf-8"))

                
            # need to add in sequence numbers here or something and add if statements for those otherwise i dont think things are gonna work

            print(f"Data received from server: {decoded_data}")
        elif usr_input == "2":
            print("Send message to server")
            while True:
                message = input()
                client_conn.send(bytes(message, "utf-8"))
        else:
            print("\nERROR - Invalid selection")

    except KeyboardInterrupt:
        print("\nERROR - Keyboard Interrupt")
        # dont need this, only in server
        # client_conn.shutdown(socket.SHUT_RDWR)
        # client_conn.close()
        sys.exit(1)
        break