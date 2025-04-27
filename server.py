import socket
import sys

server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Server can be re-issued immediately
server_conn.bind(("127.0.0.1", 23456))
server_conn.listen()
conn, addr = server_conn.accept()

with conn:
    print(f'Connection initiated with {addr}')

    while True:
        try:
            # Receive
            data = conn.recv(1024)
            data_dec = data.decode("utf-8")

            print(f"Server received data: {data_dec}")

            

            # breaks loop if data is empty
            if not data: 
                print("Client disconnected...")
                break

            # Send

            if data_dec == "SYN":
                print("\n[2] SYN: Server -> Client")
                conn.send(bytes("SYN-ACK", "utf-8"))
                print("Server waiting for ACK...")
            if data_dec == "ACK":
                print("\nTCP Connection initiated!")

            # print("Sending this back to the client..")
            # conn.sendall(data)

        except KeyboardInterrupt:
            print("\nERROR - Keyboard Interrupt")
            conn.shutdown(socket.SHUT_RDWR) # needs to be conn not server_conn
            conn.close()
            sys.exit(1)
            break

