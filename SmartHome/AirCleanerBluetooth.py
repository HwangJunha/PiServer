from bluetooth import *
def onMode(client_socket): #manualMode
    client_socket.send('1')
    print("Finished")
def offMode(client_socket): #manualMode
    client_socket.send('2')
    print("Finished")
    
def autoMode(client_socket):# auto mode
    client_socket.send('3')
    print("Finished")
    
def current(client_socket): #current state
    client_socket.send('4')
    msg=client_socket.recv(1024)
    print("Finished")
    return msg;
def test(code):
    print(code)