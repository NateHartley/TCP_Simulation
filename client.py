import socket

client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# same as server_conn

client_conn.connect(("localhost", 23456))
# must be server hostname or ip and port
# using connect() rather than bind()

while True:

    usr_input = input("Speak to server: ")
    encoded_input = usr_input.encode("utf-8")

    client_conn.sendall(encoded_input)
    # sending data

    data = client_conn.recv(1024)
    # hopefully get same data back from server

    decoded_data = data.decode("utf-8")

    print(f"Data received: {decoded_data}")
