from bluetooth import *
def onMode(client_socket): #onMode
    client_socket.send('1')
    print("Finished")
def offMode(client_socket): #offMode
    client_socket.send('2')
    print("Finished")
def current(client_socket): #current state
    client_socket.send('3')
    msg=client_socket.recv(1024)
    print("Finished")
    return msg;