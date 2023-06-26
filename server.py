import socket

# Create a socket object

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 3000
server = 'localhost'

try:
    s.bind((server, port))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])

# Define the port on which you want to connect


# connect to the server on local computer

s.listen(5)
print('Server listening....')

# receive data from the server

while True:
    c, addr = s.accept()
    print('Got connection from', addr)



