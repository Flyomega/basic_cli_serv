import socket

# Create a socket object

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 3000
server = 'localhost'

try:
    s.connect((server, port))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
