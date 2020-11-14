import socket
import AirCleanerBluetooth
import SmartWindow
import MoodLightBluetoothRoom1 #room1 modeLight
import DoorLockBluetooth # doorLcok
from AirCleanerBluetooth import*
from _thread import *
import pymysql
import face_recognition
import HumidifierBluetooth
import FlowerpotBluetooth
# 쓰레드에서 실행되는 코드입니다. 

# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다. 
class Slave:
    def __init__(self,client_socket, addr, bluetoothDic):
        self.client_socket = client_socket
        self.addr = addr
        self.bluetoothDic=bluetoothDic
        
    def camera_face_start(client_socket_doorLock):
        face_recognition.faceReStart(client_socket_doorLock)
    
    def threaded(self,client_socket,data):
        
        print('Connected by :', self.addr[0], ':', self.addr[1]) 
        # 클라이언트가 접속을 끊을 때 까지 반복합니다.
        
        while True: 
            try:
                # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
               
                if not data: 
                    print('Disconnected by ' + self.addr[0],':',self.addr[1])
                    break
                
                print('Received from ' + self.addr[0],':',self.addr[1] , data.decode())
                #airCleaner
                for key, value in self.bluetoothDic.items():
                    if data.decode().split('/')[0]==key:
                        A, B=key.split("-")
                        if A == 'ACL':
                            if data.decode().split('/')[1]=='on\n':
                                AirCleanerBluetooth.onMode(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='off\n':
                                AirCleanerBluetooth.offMode(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='auto\n':
                                AirCleanerBluetooth.autoMode(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='current\n':
                                current=AirCleanerBluetooth.current(self.bluetoothDic[key])
                                print(current)
                                client_socket.send(current)  
                        elif A == 'DL':
                            if data.decode().split('/')[1]=='open\n':
                                DoorLockBluetooth.openDoorLock(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='reset\n':
                                DoorLockBluetooth.selectKey(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='insert\n':
                                DoorLockBluetooth.insertKey(self.bluetoothDic[key])
                            
                        elif A == 'SW':
                            if data.decode().split('/')[1]=='open\n' :
                                SmartWindow.openWindow(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='close\n':
                                SmartWindow.closeWindow(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='aiMode\n':
                                SmartWindow.AIMode(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='manualMode\n':
                                SmartWindow.manualMode(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='current\n':
                                current=SmartWindow.currentState(self.bluetoothDic[key])
                                print(current)
                                client_socket.send(current)
                                
                        elif A == 'ML':
                            if data.decode().split('/')[1]=='on\n':
                                MoodLightBluetoothRoom1.onLight(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='off\n':
                                MoodLightBluetoothRoom1.offLight(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='current\n':
                                current=MoodLightBluetoothRoom1.current(self.bluetoothDic[key])
                                print(current)
                                client_socket.send(current)
                        elif A == 'HF':
                            if data.decode().split('/')[1]=='on\n':
                                HumidifierBluetooth.onMode(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='off\n':
                                HumidifierBluetooth.offMode(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='auto\n':
                                HumidifierBluetooth.autoMode(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='current\n':
                                current=HumidifierBluetooth.current(self.bluetoothDic[key])
                                print(current)
                                client_socket.send(current)
                        elif A == 'FP':
                            if data.decode().split('/')[1]=='on\n':
                                FlowerpotBluetooth.onMode(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='off\n':
                                FlowerpotBluetooth.offMode(self.bluetoothDic[key])
                            elif data.decode().split('/')[1]=='current\n':
                                current=FlowerpotBluetooth.current(self.bluetoothDic[key])
                                print(current)
                                client_socket.send(current)
                                
                client_socket.send(data)
                data = client_socket.recv(1024)
            except ConnectionResetError as e:
    
                print('Disconnected by ' + self.addr[0],':',self.addr[1])
                break
        client_socket.close()
            
            