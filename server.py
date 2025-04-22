import socket

server_conn = socket.socket(socket.AF_INET, socket.SOCK_RAW)
# AF_INET is the Address Family (AF) for the socket, in this case it's ipv4 (INET)
# TODO: eventually I want to replace SOCK_STREAM with SOCK_RAW as this just sends the raw packet and it's my job to do the encapsulation

server_conn.bind("127.0.0.1", 23456)
# bind() used to associate a socket with a specific ip and port
# 127.0.0.1 just a standard loopback interface address (localhost)
# 23456 port number that hopefully isn't being used by any other service

server_conn.listen()