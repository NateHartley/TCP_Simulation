import socket

server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET is the Address Family (AF) for the socket, in this case it's ipv4 (INET)
# TODO: eventually I want to replace SOCK_STREAM with SOCK_RAW as this just sends the raw packet and it's my job to do the encapsulation

server_conn.bind(("", 23456))
# bind() takes in a tuple and is used to associate a socket with a specific ip and port
# 127.0.0.1 just a standard loopback interface address (localhost)
# 23456 port number that hopefully isn't being used by any other service

server_conn.listen()
# listen() takes an integer that is the number of unaccepted connections that the system will allow before refusing new connections

conn, addr = server_conn.accept()
# accept() blocks execution and waits for incoming connection. Once it receives a socket object, it assigns it to the connection to conn and host+port to addr
# this is the socket used to talk to the client

with conn:
    # with automatically closes the connection once we're done so no need to specify closing the connection
    
    print(f'Connection initiated with {addr}')

    # infinite while loop, so the server is always going to echo back whatever the client sends
    while True:
        data = conn.recv(1024)
        # recv() is a blocking method, it blocks everything else whilst it waits for data from the Standard Input (I/O)
        # its waiting to receive data from the client
        # recv() takes in a buffer size which we've set to be 1024 bytes (?)

        if not data: break
        conn.sendall(data)
        # echo the data it just received
