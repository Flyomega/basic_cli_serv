import socket
import ctypes
import threading
from threading import Thread
import sys

# Create a socket object

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 3000
server = 'localhost'
form = 'utf-8'

    
listtaks = []

try:
    s.bind((server, port))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])


#function that uses the dynamic library of fibonacci and returns the result to the client

def fibonacci(n):
    lib = ctypes.CDLL('./fibo/libfibo.so')
    lib.fibo.restype = ctypes.c_int
    return lib.fibo(n)

def client_request(conn, addr):
    connected = True
    tochange = -1
    while connected:
        msg = conn.recv(1024).decode(form)
        if not msg:
            connected = False
        if(msg == "DISCONNECT"):
            connected = False
        else:
            if(msg.startswith('send')):
                msg = msg[5:]
                try:
                    msg = int(msg)
                    result = fibonacci(msg)
                    listtaks.append((msg, result))
                    tochange+=1
                    tosend = "[scheduled] fibo " + str(msg)
                    conn.send(tosend.encode(form))
                except ValueError:
                    conn.send('Please enter a number after the send'.encode(form))
            elif (msg == "list"):
                if(tochange == -1):
                    conn.send('There are no scheduled tasks'.encode(form))
                else:
                    for i in range(len(listtaks)):
                        if(i != len(listtaks) - 1 and listtaks[i][1] != None):
                            msg1 = "[done] fibo " + str(listtaks[i][0]) + " (result " + str(listtaks[i][1]) + ")" + "\n"
                            conn.send(msg1.encode(form))
                        else:
                            msg2 = "[scheduled] fibo " + str(listtaks[i][0])
                            conn.send(msg2.encode(form))
            else:
                conn.send('Please enter a valid command'.encode(form))
    conn.close()

# receive data from the server

def start():
    s.listen()
    print('Server listening....')
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        thread = threading.Thread(target=client_request, args=(c,addr))
        thread.start()
        if(threading.active_count() > 1):
            print('There are: ', threading.active_count() - 1, 'clients connected')
        else:
            print('There is: ', threading.active_count() - 1, 'client connected')


start()