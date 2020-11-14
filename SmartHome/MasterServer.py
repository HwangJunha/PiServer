import SlaveServer
import socket
import AirCleanerBluetooth
import SmartWindow
from AirCleanerBluetooth import*
from _thread import *
import DoorLockBluetooth
import DoorLockRFID
import pymysql
import MoodLightBluetoothRoom1 #room1 modeLight
import Schedule
import FlowerpotBluetooth



import threading
from threading import Thread
import sys
from queue import Queue

t= None

def ModeSelect():
    conn = pymysql.connect(host='ip', user='root', password='pwd', db='dbname', charset='utf8')
    curs=conn.cursor(pymysql.cursors.DictCursor)
    sql = "select model,bluetoothKey from deviceList where model = 'DL-01'"
    curs.execute(sql)
    rows = curs.fetchall()
    key={}
    print(rows)
    
    for row in rows:
        print(row['model'])
        print(row['bluetoothKey'])
        key[row['model']]=[row['bluetoothKey']]
    
    conn.close()
    print("Finished")
    print(key)

    return key

def main_thread(q):
    print('check')
    schedule = Schedule.UserAI(bluetoothDic) #userAIserver     
    user_AI_thread = threading.Thread(target=schedule.AIStart())
    user_AI_thread.daemon = True
    user_AI_thread.start()
    if msg == 0:
        sys.exit()

def start():
    global q, t
    q= Queue()
    t=Thread(target=main_thread, args=(q,))
    t.start()
def kill():
    global q, t
    q.put(0)

if __name__=="__main__":
    HOST = 'ip'
    PORT = 9999
    camera=True
    isAi=True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    
    server_socket.listen()
    print('server start')

    #tempValue
    dic=ModeSelect()
    bluetoothDic={}
    
    for key, value in dic.items():
        try:
            A, B=key.split("-")
            if A == 'SS':
                continue
            else:
                client_socket_bluetooth=BluetoothSocket(RFCOMM)
                bluetoothKey="".join(value)
                client_socket_bluetooth.connect((bluetoothKey,1))
                bluetoothDic[key] = client_socket_bluetooth
                print(bluetoothDic)
        except:
            print('Exception!')
    # 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.
    # 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
    
    while True: 
        
        for key, value in dic.items():
            A, B=key.split("-")
            if A == 'DL':
                if camera:
                    DoorLockBluetooth.selectKey(bluetoothDic[key])
                    start_new_thread(SlaveServer.Slave.camera_face_start,(bluetoothDic[key],))
                    camera=False
                    
        if isAi:
            start()
            isAi=False
            
        
        print('wait')
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024)
        if data.decode().split('/')[0] == 'newAI\n':
            kill()
            start()
            client_socket.send(data)
        else:
            print(data.decode())
            slaves = SlaveServer.Slave(client_socket, addr, bluetoothDic) #slave Server
            start_new_thread(slaves.threaded,(client_socket,data,))
        
        
        
    server_socket.close()
    """
    client_socket_moodLight1.close()
    client_socket_window.close()
    client_socket_airCleaner.close()
    client_socket_doorLock.close()
    """
    
