from concurrent.futures import ThreadPoolExecutor
import socket
import ctypes
import threading
import os

# Create a socket object

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 3000
server = 'localhost'
form = 'utf-8'


thread_list = list()

try:
    s.bind((server, port))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])


pool = ThreadPoolExecutor(max_workers=4)
#function that uses the dynamic library of fibonacci and returns the result to the client

def fibonacci(n):
    lib = ctypes.CDLL('./fibo/libfibo.so')
    lib.fibo.restype = ctypes.c_int
    return lib.fibo(n)

def client_request(conn, addr):
    connected = True
    isempty = True
    while connected:
        msg = conn.recv(4096).decode(form)
        if not msg:
            connected = False
        if(msg == "DISCONNECT"):
            connected = False
        else:
            if(msg.startswith('send')):
                msg = msg[5:]
                try:
                    msg = int(msg)
                    #check if the library exists
                    if(os.path.exists('./fibo/libfibo.so') == False):
                        conn.send('The fibonacci library does not exist'.encode(form))
                        continue
                    t = pool.submit(fibonacci, msg)
                    thread_list.append((t,msg))
                    isempty = False
                except ValueError:
                    conn.send('Please enter a number after the send'.encode(form))
            elif (msg == "list"):
                if(isempty):
                    conn.send('There are no scheduled tasks'.encode(form))
                else:
                    res = ""
                    for process,msg in thread_list:
                        if(process.running()):
                            msg2 = "[scheduled] fibo " + str(msg)
                            res+=msg2
                        else:
                            result = process.result()
                            msg1 = "[done] fibo " + str(msg) + " (result " + str(result) + ")"
                            res+=msg1
                        if(process != thread_list[len(thread_list) - 1][0]):
                            res+="\n"
                    conn.send(res.encode(form))
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