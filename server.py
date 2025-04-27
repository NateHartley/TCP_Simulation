import socket
import sys

server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Server can be re-issued immediately
server_conn.bind(("127.0.0.1", 23456))
server_conn.listen()
conn, addr = server_conn.accept()

TCP_FLAG = ["SYN", "SYN-ACK", "ACK"]

with conn:
    print(f'Connection initiated with {addr}')

    while True:
        try:
            # Receive
            d = conn.recv(1024)
            data = d.decode("utf-8")

            # breaks loop if data is empty
            if not data: 
                print("Client disconnected...")
                break

            # Send
            if data == TCP_FLAG[0]:
                print(f"\n[2] {TCP_FLAG[1]}: Server -> Client")
                conn.send(bytes(TCP_FLAG[1], "utf-8"))
                print(f"Server waiting for {TCP_FLAG[2]}...")
            if data == TCP_FLAG[2]:
                print("\nTCP Connection Established! 🎉")

            print(f"DEBUG: Data received from client: {data}")

        except KeyboardInterrupt:
            print("\nERROR - Keyboard Interrupt")
            conn.shutdown(socket.SHUT_RDWR) # needs to be conn not server_conn
            conn.close()
            sys.exit(1)
            break

