from bluetooth import *
def openWindow(client_socket): #manualMode
    
    client_socket.send('1')
    print("Finished")

def closeWindow(client_socket):# auto mode
    
    client_socket.send('2')
    print("Finished")

def AIMode(client_socket): #current state
    
    client_socket.send('3')
    print("Finished")

def manualMode(client_socket):
    
    client_socket.send('0')
    print("Finished")
    
def currentState(client_socket):
    client_socket.send('4')
    msg=client_socket.recv(1024)
    print("Finished")
    return msg
