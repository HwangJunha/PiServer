from bluetooth import *
def onLight(client_socket): #onLight
    print("onLIGHT")
    client_socket.send('1')
    client_socket.send('1')
    client_socket.send('1')
    client_socket.send('1')
    client_socket.send('1')
    client_socket.send('1')
    client_socket.send('1')
    client_socket.send('1')
    print("Finished")
    

def offLight(client_socket):# offLight
    print("offLIGHT")
    client_socket.send('2')
    client_socket.send('2')
    client_socket.send('2')
    client_socket.send('2')
    client_socket.send('2')
    client_socket.send('2')
    client_socket.send('2')
    client_socket.send('2')
    print("Finished")
    

def current(client_socket): #current state
    print("ModeCurrent")
    client_socket.send('3')
    msg=client_socket.recv(1024)
    print("Finished")
    return msg;
