import socket
import AirCleanerBluetooth
import SmartWindow
import MoodLightBluetoothRoom1 #room1 modeLight
import DoorLockBluetooth # doorLcok
import RBP_DL51_SURVEILLANCE_CAMERA
from AirCleanerBluetooth import*
from _thread import *


# 쓰레드에서 실행되는 코드입니다. 

# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다. 
def threaded(client_socket, addr):

    print('Connected by :', addr[0], ':', addr[1]) 
    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    while True: 

        try:

            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            data = client_socket.recv(1024)

            if not data: 
                print('Disconnected by ' + addr[0],':',addr[1])
                break

            print('Received from ' + addr[0],':',addr[1] , data.decode())
            #airCleaner
            if data.decode().split('/')[0]=='auto\n': #auto mode exec
                AirCleanerBluetooth.autoMode(client_socket_airCleaner)
            elif data.decode().split('/')[0]=='manual': #manual mode exec
                AirCleanerBluetooth.manualMode(data.decode().split('/')[1],client_socket_airCleaner)
            elif data.decode().split('/')[0]=='current\n':
                current=AirCleanerBluetooth.current(client_socket_airCleaner)
                client_socket.send(current)
            
            #doorLock
            if data.decode().split('/')[0]=='door': #auto mode exec
                if data.decode().split('/')[1]=='open\n':
                   DoorLockBluetooth.openDoorLock(client_socket_doorLock)
            
            #room1 sub moodLight, window
            if data.decode().split('/')[0]=='room1':
                if data.decode().split('/')[1]=='moodLight':
                    if data.decode().split('/')[2]=='on\n':
                        MoodLightBluetoothRoom1.onLight(client_socket_moodLight1)
                    elif data.decode().split('/')[2]=='off\n':
                        MoodLightBluetoothRoom1.offLight(client_socket_moodLight1)
                    elif data.decode().split('/')[2]=='current\n':
                        current=MoodLightBluetoothRoom1.current(client_socket_moodLight1)
                        client_socket.send(current)
                        
                elif data.decode().split('/')[1]=='window':
                    if data.decode().split('/')[2]=='open\n' :
                        SmartWindow.openWindow(client_socket_window)
                    elif data.decode().split('/')[2]=='close\n':
                        SmartWindow.closeWindow(client_socket_window)
                    elif data.decode().split('/')[2]=='aiMode\n':
                        SmartWindow.AIMode(client_socket_window)
                    elif data.decode().split('/')[2]=='manualMode\n':
                        SmartWindow.manualMode(client_socket_window)
                    elif data.decode().split('/')[2]=='current\n':
                        current=SmartWindow.currentState(client_socket_window)
                        print(current)
                        client_socket.send(current) #send homeServer
                        
                        
            client_socket.send(data)

        except ConnectionResetError as e:

            print('Disconnected by ' + addr[0],':',addr[1])
            break
             
    client_socket.close() 
def faceRecognition(client_socket_doorLock):
    print("StartFace")
    userState=RBP_DL51_SURVEILLANCE_CAMERA.faceReStart()
    if userState:
        DoorLockBluetooth.openDoorLock(client_socket_doorLock)
            

if __name__=="__main__":
    HOST = ''
    PORT = 9999
    
    userState=False
    camera_exec=True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    
    server_socket.listen()
    print('server start')
    """
    client_socket_window=BluetoothSocket(RFCOMM)
    client_socket_window.connect(("98:D3:71:FD:5D:14",1))
    print("smartwindow bluetooth connected!")

    client_socket_moodLight1=BluetoothSocket(RFCOMM)
    client_socket_moodLight1.connect(("98:D3:31:FD:5A:B6",1))
    print("moodLight1 bluetooth connected!")


    client_socket_airCleaner=BluetoothSocket(RFCOMM)
    check=client_socket_airCleaner.connect(("98:D3:51:FD:A0:AC",1))
    print("AirCleaner bluetooth connected!")
    """

    client_socket_doorLock=BluetoothSocket(RFCOMM)
    client_socket_doorLock.connect(("98:D3:11:FD:63:C5",1))
    print("DoorLock bluetooth connected!")
    # 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.

    # 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
    while True: 
        if camera_exec:
            start_new_thread(faceRecognition,(,))
            camera_exec=False
            
        print('wait')
        client_socket, addr = server_socket.accept() 
        start_new_thread(threaded, (client_socket, addr))
        
    server_socket.close()
    client_socket_moodLight1.close()
    client_socket_window.close()
    client_socket_airCleaner.close()
    client_socket_doorLock.close()
