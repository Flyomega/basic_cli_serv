import socket

# Create a socket object

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 3000
server = 'localhost'

client.connect((server, port))


def send(msg):
    message = msg.encode('utf-8')
    client.send(message)


#function that retreive an input from the user and send it to the server

def start():
    while True:
        msg = input('my_client ')
        send(msg)
        if(msg.startswith('send')):
            continue
        print(client.recv(4096).decode('utf-8'))


start()